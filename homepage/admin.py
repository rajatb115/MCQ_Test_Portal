from django.contrib import admin

# Register your models here.
from .models import question,student,stu_solution,teacher,paper_list,desc

admin.site.register(question),
admin.site.register(student),
admin.site.register(stu_solution),
admin.site.register(teacher),
admin.site.register(paper_list),
admin.site.register(desc)