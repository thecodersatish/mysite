from random import random
import re
import requests
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import base64
from django.contrib.auth import login,authenticate,logout
from .forms import LoginForm,SignUpForm
from django.contrib.auth.decorators import login_required
from .models import *
import json
import random
from django.db.models import F,Q,FilteredRelation
from django.core import serializers
from django.forms.models import model_to_dict
from django.db import connection
from json import dumps
import datetime


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or '/')
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            rememberme = form.cleaned_data.get("rememberme")
            print(rememberme)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next') or '/')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "registration/login.html", {"form": form, "msg": msg})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

def index(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,'index.html')


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'dashboard.html',{'profile':profile})

@login_required
def course_overview(request,course_code):
    try:
        course = Course.objects.get(code=course_code)
        modules= Module.objects.all().filter(course=course)
        return render(request,'course-overview.html',{'course':course,'modules':modules})
    except Course.DoesNotExist:
        return render(request,"page-404.html",{})

@login_required
def quiz_view(request,course_code,module_code,quiz_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    questions = []
    for i in Quiz.objects.all().filter(module=module):
        d=model_to_dict(i)
        questions.append(d)
        try:
            obj = Quiz_Submission.objects.get(quiz=i,user=request.user)
            d['status'] = obj.status
        except:
            pass
    if quiz_code=="":
        question = Quiz.objects.all().filter(course=course,module=module)[0]
    else:
        question = Quiz.objects.get(course=course,module=module,code=quiz_code)
    context=model_to_dict(question)
    if context['has_script']:
        context['script']=base64.b64decode(context['script']).decode()
    try:
        obj = Quiz_Submission.objects.get(quiz=question,user=request.user)
        context['status'] = obj.status
        context['option_selected']=obj.option_selected
    except:
        pass
    return render(request,'quiz.html',{'questions':questions,'question':context,'data':dumps(context)})


@csrf_exempt
@login_required
def quiz_submit(request):
    if request.method=="POST":
        answer=request.POST.get('answer')
        quiz = Quiz.objects.get(code=request.POST.get('code'))
        correct = quiz.correct_choice==answer
        obj = Quiz_Submission.objects.get_or_create(quiz=quiz,user=request.user)[0]
        if(not obj.status):
            updated = Quiz_Submission.objects.filter(quiz=quiz,user=request.user,version=obj.version).update(status=correct,option_selected=answer,version=obj.version+1)
        else:
            return JsonResponse({'accepted':True,'answer':quiz.correct_choice})
        return JsonResponse({'updated':updated==0,'status':correct})


def problem_view(request,course_code,module_code,problem_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    questions = []
    for i in Problem.objects.all().filter(module=module):
        d={'code':i.code,'title':i.title}
        if Problem_Submission.objects.filter(problem=i,user=request.user,status=3).exists():
            d['status'] = True
        elif Problem_Submission.objects.filter(problem=i,user=request.user).exists():
            d['status'] = False
        questions.append(d)
    if problem_code=="":
        question = Problem.objects.all().filter(course=course,module=module)[0]
    else:
        question = Problem.objects.get(course=course,module=module,code=problem_code)
    context=model_to_dict(question)
    if Previous_Code.objects.filter(user=request.user,problem=question).exists():
        prev_code=Previous_Code.objects.get(user=request.user,problem=question)
        context['source']=prev_code.source
    else:
        context['source']=context['default_code']
    return render(request,'coding-problem.html',{'questions':questions,'question':context})



@csrf_exempt
def run(request):
    if request.method=="POST":
        url = "https://judge0-ce.p.rapidapi.com/submissions"
        input=request.POST.get('input')
        with open("courses/temp/python.zip", "rb") as f:
            bytes = f.read()
            encode_string = base64.b64encode(bytes)
        data = "{\"language_id\": "+str(89)+",\"additional_files\": \""+str(encode_string)[2:-1]+"\",\"stdin\": \""+input+"\"}"
        querystring = {"base64_encoded":"true","fields":"*","redirect_stderr_to_stdout":"true","cpu_time_limit":1.0,"wall_time_limit":1.0,"stack_limit":1024.0}
        headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
        'x-rapidapi-key': "513e11481bmshd740ecb0d4d638ap1d286cjsn0f35f7d4e420"
        }
        response = requests.request("POST", url, data=data, headers=headers, params=querystring)
        print(response)
        url = "https://judge0-ce.p.rapidapi.com/submissions/"+response.json()["token"]
        querystring = {"base64_encoded":"true","fields":"*","redirect_stderr_to_stdout":"true"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        d=response.json()
        return HttpResponse(
            JsonResponse(d),
            content_type="application/json"
        )
    else:
        return render(request,'run.html')

@csrf_exempt
@login_required
def validate(request):
    if request.method=="POST":
        try:
            problem = Problem.objects.get(code=request.POST.get('problem_code'))
        except:
            problem = Assessment_Problem.objects.get(code=request.POST.get('problem_code'))
        url = "https://judge0-ce.p.rapidapi.com/submissions/batch"
        data = "{\"submissions\": ["
        f=open("courses/testcases/"+problem.course.code+"/"+problem.module.code+"/"+problem.code+".inout","r")
        for i in range(2):
            data += "{\"language_id\": "+str(request.POST.get('language_code'))+",\"source_code\": \""+request.POST.get('source')+"\",\"stdin\": \""+f.readline().strip()+"\",\"cpu_time_limit\":1.0,\"wall_time_limit\":1.0,\"redirect_stderr_to_stdout\":true,\"expected_output\":\""+f.readline().strip()+"\"}"
            if i!=1:
                data += ","
        data += "]}"
        f.close()
        querystring = {"base64_encoded":"true","fields":"*","cpu_time_limit":1.0,"wall_time_limit":1.0,"stack_limit":1024.0}
        headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
        'x-rapidapi-key': "513e11481bmshd740ecb0d4d638ap1d286cjsn0f35f7d4e420"
        }
        response = requests.request("POST", url, data=data, headers=headers, params=querystring)
        tokens=response.json()
        print(tokens)
        querystring = {"base64_encoded":"true","fields":"*"}
        d={}
        for i in range(2):
            url = "https://judge0-ce.p.rapidapi.com/submissions/"+tokens[i]["token"]
            response = requests.request("GET", url, headers=headers, params=querystring)
            while response.json()["status_id"]<=2:
                response = requests.request("GET", url, headers=headers, params=querystring)
            d[i]=response.json()
        return JsonResponse(d)

@csrf_exempt
@login_required
def problem_submit(request):
    if request.method=="POST":
        problem = Problem.objects.get(code=request.POST.get('problem_code'))
        if Problem_Submission.objects.filter(problem=problem,user=request.user,status=3).exists():
            return JsonResponse({"status_id":1})
        d = datetime.datetime.now()
        source = str(request.POST.get('source'))
        obj,submission_created = Problem_Submission.objects.get_or_create(problem=problem,user=request.user,status=-1)
        if not submission_created:
            return JsonResponse({"status_id":-1})
        if Problem_Submission.objects.filter(problem=problem,user=request.user,status=3).exists():
            obj.delete()
            return JsonResponse({"status_id":1})
        data = "{\"submissions\": ["
        f=open("courses/testcases/"+problem.course.code+"/"+problem.module.code+"/"+problem.code+".inout","r")
        l = f.readlines()
        for i in range(2,7):
            data += "{\"language_id\": "+str(request.POST.get('language_code'))+",\"source_code\": \""+source+"\",\"stdin\": \""+l[i].strip()+"\",\"cpu_time_limit\":1.0,\"wall_time_limit\":1.0,\"redirect_stderr_to_stdout\":true,\"expected_output\":\""+l[i+1].strip()+"\"}"
            if i!=6:
                data += ","
        data += "]}"
        f.close()
        url = "https://judge0-ce.p.rapidapi.com/submissions/batch"
        querystring = {"base64_encoded":"true","fields":"*","cpu_time_limit":1.0,"wall_time_limit":1.0,"stack_limit":1024.0}
        headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
        'x-rapidapi-key': "513e11481bmshd740ecb0d4d638ap1d286cjsn0f35f7d4e420"
        }
        response = requests.request("POST", url, data=data, headers=headers, params=querystring)
        tokens=response.json()
        c=0
        for i in range(5):
            url = "https://judge0-ce.p.rapidapi.com/submissions/"+tokens[i]["token"]
            response = requests.request("GET", url, headers=headers, params=querystring)
            while response.json()["status_id"]<=2:
                response = requests.request("GET", url, headers=headers, params=querystring)
            if response.json()["status_id"]!=3:
                break
            c+=1
        obj.date = d
        obj.source = source
        obj.status=response.json()['status_id']
        obj.testcases_passed=c
        obj.save()
        return JsonResponse({"status_id":response.json()['status_id']})


@csrf_exempt
@login_required
def problem_submissions(request):
    if request.method=="GET":
        problem = Problem.objects.get(code=request.GET.get('problem_code'))
        submissions = [model_to_dict(i) for i in Problem_Submission.objects.all().filter(user=request.user,problem=problem)]
        return JsonResponse({"submissions":submissions})

@csrf_exempt
@login_required
def questions_completed(request):
    if request.method=="POST":
        print(request.POST.get('course'))
        course = Course.objects.get(code=request.POST.get('course'))
        cr=Course_Registration.objects.get(course=course,user=request.user)
        return JsonResponse({'questions_completed':cr.no_of_questions_completed})

@login_required
def rearrange_view(request,course_code,module_code,problem_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    questions = []
    for i in Rearrange_Problem.objects.all().filter(module=module):
        d={'code':i.code,'title':i.title}
        if Rearrange_Problem_Submission.objects.filter(problem=i,user=request.user,status=1).exists():
            d['status'] = True
        elif Rearrange_Problem_Submission.objects.filter(problem=i,user=request.user,status=0).exists():
            d['status'] = False
        questions.append(d)
    if problem_code=="":
        question = Rearrange_Problem.objects.filter(course=course,module=module)[0]
    else:
        question = Rearrange_Problem.objects.get(course=course,module=module,code=problem_code)
    statements = [model_to_dict(i) for i in Statement.objects.filter(problem=question)]
    if not Rearrange_Problem_Submission.objects.filter(problem=question,user=request.user,status=1).exists():
        random.shuffle(statements)
        context = model_to_dict(question)
        context['status'] = False
    else:
        context = model_to_dict(question)
        context['status'] = True
    return render(request,'rearrange.html',{'questions':questions,'question':context,'statements':json.dumps(statements)})

@csrf_exempt
@login_required
def rearrange_submit(request):
    if request.method=="POST":
        problem = Rearrange_Problem.objects.get(code=request.POST.get('problem_code'))
        if Rearrange_Problem_Submission.objects.filter(problem=problem,user=request.user,status=1).exists():
            return JsonResponse({'accepted':True})
        obj = Rearrange_Problem_Submission.objects.get_or_create(problem=problem,user=request.user)[0]
        url = "https://judge0-ce.p.rapidapi.com/submissions/batch"
        data = "{\"submissions\": ["
        f=open("courses/testcases/"+problem.course.code+"/"+problem.module.code+"/"+problem.code+".inout","r")
        for i in range(2):
            data += "{\"language_id\": "+str(request.POST.get('language_code'))+",\"source_code\": \""+request.POST.get('source')+"\",\"stdin\": \""+f.readline().strip()+"\",\"cpu_time_limit\":1.0,\"wall_time_limit\":1.0,\"redirect_stderr_to_stdout\":true,\"expected_output\":\""+f.readline().strip()+"\"}"
            if i!=1:
                data += ","
        data += "]}"
        f.close()
        querystring = {"base64_encoded":"true","fields":"*","cpu_time_limit":1.0,"wall_time_limit":1.0,"stack_limit":1024.0}
        headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
        'x-rapidapi-key': "513e11481bmshd740ecb0d4d638ap1d286cjsn0f35f7d4e420"
        }
        response = requests.request("POST", url, data=data, headers=headers, params=querystring)
        tokens=response.json()
        querystring = {"base64_encoded":"true","fields":"*"}
        d={}
        for i in range(2):
            url = "https://judge0-ce.p.rapidapi.com/submissions/"+tokens[i]["token"]
            response = requests.request("GET", url, headers=headers, params=querystring)
            while response.json()["status_id"]<=2:
                response = requests.request("GET", url, headers=headers, params=querystring)
            d[i]=response.json()
        status = 0
        if d[0]['status_id']==3 and d[1]['status_id']==3:
            status = 1
        if(not obj.status):
            updated = Rearrange_Problem_Submission.objects.filter(user=request.user,problem=problem,version = obj.version).update(status=status,version = obj.version)
        else:
            return JsonResponse({'accepted':True})
        d["updated"]=updated
        return JsonResponse(d)

@login_required
def assessment_view(request,course_code,module_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    if Assessment.objects.filter(module=module,user=request.user).exists():
        assessment = Assessment.objects.get(module=module,user=request.user)
        score= str(assessment.questions_accepted*50)+"%"
        d=assessment.start_time
        d = d.replace(tzinfo=None)
        if((datetime.datetime.now()-d)>datetime.timedelta(hours=1) or assessment.endedByUser):
            msg = "You have already taken the assessment."
            status = 3
        else:
            msg = "You are already started the assessment. Click continue to continue the asessment."
            status = 2
    else:
        score = "N/A"
        msg = "Click start button to start the assessment."
        status = 1
    return render(request,'assessment-landing.html',{'msg':msg,'status':status,'score':score,'course':course_code})

@login_required
def assessment_start(request,course_code,module_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    if Assessment.objects.filter(module=module,user=request.user).exists():
        assessment = Assessment.objects.get(module=module,user=request.user)
        d=assessment.start_time
        d = d.replace(tzinfo=None)
        if((datetime.datetime.now()-d)>datetime.timedelta(hours=1)):
            return redirect(assessment_view,course_code,module_code)
        else:
            return redirect(assessment_problem_view,course_code,module_code)
    else:
        assessment = Assessment(course=course,module=module,user=request.user,start_time=datetime.datetime.now())
        assessment.save()
    return redirect(assessment_problem_view,course_code,module_code)

@login_required
def assessment_end(request,course_code,module_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    if Assessment.objects.filter(module=module,user=request.user).exists():
        assessment = Assessment.objects.get(module=module,user=request.user)
        assessment.endedByUser = True
        assessment.save()
    return redirect(assessment_problem_view,course_code,module_code)

@login_required
def assessment_problem_view(request,course_code,module_code):
    course = Course.objects.get(code=course_code)
    module= Module.objects.get(course=course,code=module_code)
    if Assessment.objects.filter(module=module,user=request.user).exists():
        assessment = Assessment.objects.get(module=module,user=request.user)
        d=assessment.start_time
        d = d.replace(tzinfo=None)
        if((datetime.datetime.now()-d)>datetime.timedelta(hours=1) or assessment.endedByUser):
            return redirect(assessment_view,course_code,module_code)
    else:
        return redirect(assessment_view,course_code,module_code)
    assessment.start_time += datetime.timedelta(hours = 6.5)
    formatedDate = assessment.start_time.strftime("%Y-%m-%d %H:%M:%S")
    questions = []
    for i in Assessment_Problem.objects.all().filter(module=module):
        d=model_to_dict(i)
        if Assessment_Problem_Submission.objects.filter(problem=i,user=request.user,status=3).exists():
            d['status'] = True
        elif Assessment_Problem_Submission.objects.filter(problem=i,user=request.user).exists():
            d['status'] = False
        if Assessment_Previous_Code.objects.filter(problem=i,user=request.user).exists():
            obj = Assessment_Previous_Code.objects.get(problem=i,user=request.user)
            d['default_code'] = obj.source
        questions.append(d)
    return render(request,'assessment-problems.html',{'start_time':formatedDate,'question1':questions[0],'question2':questions[1],'assessment':model_to_dict(assessment)})

@csrf_exempt
@login_required
def save_code(request):
    if request.method=="POST":
        problem=Problem.objects.get(code=request.POST.get('problem_code'))
        code=request.POST.get('source')
        try:
            obj=Previous_Code.objects.get(user=request.user,problem=problem)
            obj.source=code
        except:
            obj=Previous_Code(user=request.user,problem=problem,source=code)
        obj.save()
        return JsonResponse({'status':'saved'})

@csrf_exempt
@login_required
def assessment_save_code(request):
    if request.method=="POST":
        problem=Assessment_Problem.objects.get(code=request.POST.get('problem_code'))
        code=request.POST.get('source')
        try:
            obj=Assessment_Previous_Code.objects.get(user=request.user,problem=problem)
            obj.source=code
        except:
            obj=Assessment_Previous_Code(user=request.user,problem=problem,source=code)
        obj.save()
        return JsonResponse({'status':'saved'})

@csrf_exempt
@login_required
def assessment_previous_code(request):
    if request.method=="GET":
        print(request.GET.get('problem_code'))
        problem=Assessment_Problem.objects.get(code=request.GET.get('problem_code'))
        try:
            obj=Assessment_Previous_Code.objects.get(user=request.user,problem=problem)
            source = obj.source
        except:
            source = problem.default_code
        return JsonResponse({'source':source})