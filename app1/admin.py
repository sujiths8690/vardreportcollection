from django.contrib import admin
from app1.models import UserModel,Constituency,LocalBody,MeetingReport,MeetingReportAdmin

# Register your models here.
admin.site.register(UserModel)
admin.site.register(Constituency)
admin.site.register(LocalBody)
admin.site.register(MeetingReport, MeetingReportAdmin)