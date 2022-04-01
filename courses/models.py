from xml.etree.ElementInclude import default_loader
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.templatetags.static import static


class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]
    related_name='profile'
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')
    
    @property
    def get_phone(self):
        print(self.phone)
        return '{}'.format(self.phone)

class Course(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    img_url = models.CharField(max_length=50,null=False,blank=False)
    code = models.CharField(max_length=20,null=False,blank=False,primary_key = True)

class Course_Registration(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mode = models.CharField(max_length=250,null=False,blank=False)
    no_of_questions_completed = models.IntegerField(default=0)

class Module(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=False,blank=False)
    code = models.CharField(max_length=20,null=False,blank=False,primary_key = True)

class Quiz(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    code = models.CharField(max_length=20,null=False,blank=False,primary_key = True)
    question = models.CharField(max_length=250,null=False,blank=False)
    has_script = models.BooleanField()
    type = models.IntegerField(default=0)
    script = models.CharField(max_length = 1000,blank=True,null=True)
    choice1 = models.CharField(max_length = 1000,null=False,blank=False)
    choice2 = models.CharField(max_length = 1000,null=False,blank=False)
    choice3 = models.CharField(max_length = 1000,null=False,blank=False)
    choice4 = models.CharField(max_length = 1000,null=False,blank=False)
    correct_choice = models.CharField(max_length = 1000,null=False,blank=False)

class Quiz_Submission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    status = models.BooleanField()
    option_selected = models.CharField(max_length = 1000,blank=False,null=False)


class Problem(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    code = models.CharField(max_length=20,null=False,blank=False,primary_key = True)
    title = models.CharField(max_length = 50,blank=False,null=False)
    description = models.CharField(max_length = 8000,null=False,blank=False)
    default_code=models.TextField(max_length=10000,default="")
    input_format = models.CharField(max_length = 2000,null=False,blank=False)
    output_format = models.CharField(max_length = 2000,null=False,blank=False)
    input1 = models.CharField(max_length = 500,null=False,blank=False)
    output1 = models.CharField(max_length = 500,null=False,blank=False)
    input2 = models.CharField(max_length = 500,null=False,blank=False)
    output2 = models.CharField(max_length = 500,null=False,blank=False)

class Previous_Code(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    source=models.TextField(max_length=20000)

class Problem_Submission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    status = models.IntegerField()
    source = source=models.TextField(max_length=20000,default="")
    date = models.DateTimeField()
    testcases_passed = models.IntegerField(default=0)

class Rearrange_Problem(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    code = models.CharField(max_length=20,null=False,blank=False,primary_key = True)
    title = models.CharField(max_length = 50,blank=False,null=False)
    description = models.CharField(max_length = 8000,null=False,blank=False)
    input_format = models.CharField(max_length = 2000,null=False,blank=False)
    output_format = models.CharField(max_length = 2000,null=False,blank=False)
    input1 = models.CharField(max_length = 500,null=False,blank=False)
    output1 = models.CharField(max_length = 500,null=False,blank=False)
    input2 = models.CharField(max_length = 500,null=False,blank=False)
    output2 = models.CharField(max_length = 500,null=False,blank=False)

class Rearrange_Problem_Submission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    problem = models.ForeignKey(Rearrange_Problem,on_delete=models.CASCADE)
    status = models.BooleanField()

class Statement(models.Model):
    problem = models.ForeignKey(Rearrange_Problem,on_delete=models.CASCADE)
    statement = models.CharField(max_length=500)

class Assignment(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_time = models.DateField()
    questions_accepted = models.IntegerField(default=0)

class Assignment_Problem(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    code = models.CharField(max_length=20,null=False,blank=False,primary_key = True)
    title = models.CharField(max_length = 50,blank=False,null=False)
    description = models.CharField(max_length = 8000,null=False,blank=False)
    default_code=models.TextField(max_length=10000,default="")
    input_format = models.CharField(max_length = 2000,null=False,blank=False)
    output_format = models.CharField(max_length = 2000,null=False,blank=False)
    input1 = models.CharField(max_length = 500,null=False,blank=False)
    output1 = models.CharField(max_length = 500,null=False,blank=False)
    input2 = models.CharField(max_length = 500,null=False,blank=False)
    output2 = models.CharField(max_length = 500,null=False,blank=False)