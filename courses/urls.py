from django.urls import path,re_path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('online-editor/',views.run,name='run'),
    path('validate/',views.validate,name="validate"),
    path('login/',views.login_view,name='login'),
    path('register/',views.register_user, name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_user,name='logout'),
    path('quiz_submit/',views.quiz_submit,name='quiz_submit'),
    path('problem_submit',views.problem_submit,name='problem_submit'),
    path('rearrange_submit',views.rearrange_submit,name='rearrange_submit'),
    path('problem_submissions',views.problem_submissions,name='problem_submissions'),
    re_path(r'^courses/(?P<course_code>[^/]+)',include([
        re_path(r'/overview',views.course_overview,name='course_overview'),
        re_path(r'/module/(?P<module_code>[^/]+)',include([
            re_path(r'/quiz/(?P<quiz_code>[\w-]*)$',views.quiz_view,name='quiz'),
            re_path(r'/problems/(?P<problem_code>[\w-]*)$',views.problem_view,name='handson'),
            re_path(r'/rearrange/(?P<problem_code>[\w-]*)$',views.rearrange_view,name='rearrange'),
            re_path(r'/assessment',include([
                re_path(r'/$',views.assessment_view,name='assessment'),
                re_path(r'/start$',views.assessment_start,name='assessment_start'),
                re_path(r'/end$',views.assessment_end,name='assessment_end'),
                re_path(r'/problems$',views.assessment_problem_view,name='assessment_problems')
            ])),
        ]))
    ])),
    path('save_code',views.save_code,name='save_code'),
    path('assessment_save_code',views.assessment_save_code,name='assessment_save_code'),
    path('assessment_previous_code',views.assessment_previous_code,name='assessment_previous_code'),
    path('questions_completed',views.questions_completed,name='questions_completed'),
]