from django.contrib import admin
from courses.models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(Quiz_Submission)
admin.site.register(Course_Registration)
admin.site.register(Problem)
admin.site.register(Previous_Code)
admin.site.register(Problem_Submission)
admin.site.register(Rearrange_Problem)
admin.site.register(Rearrange_Problem_Submission)