from django.contrib import admin

# Local model imports
from teacher.models import Course, Report, Report_student, Subject, meetings

# Register subject, report, report_student, and meeting models directly
admin.site.register(Subject)
admin.site.register(Report)
admin.site.register(Report_student)
admin.site.register(meetings)

# Custom admin configuration for Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")  # Show these fields in admin list view
    prepopulated_fields = {"slug": ("name",)}  # Autofill slug based on course name
