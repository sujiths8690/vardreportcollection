from django.db import models
from django.contrib import admin

class UserModel(models.Model):
    user_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id}-{self.username}"

    class Meta:
        db_table='userTable'


#creating table for constituency
class Constituency(models.Model):
    const_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


    class Meta:
        verbose_name = "Mandalam"
        verbose_name_plural = "Mandalams"

    def __str__(self):
        return self.name


#creating table for LocalBody
class LocalBody(models.Model):
    Local_body_id=models.AutoField(primary_key=True)
    constituency=models.ForeignKey(Constituency,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    type=models.CharField(max_length=20, choices=[('Panchayath','Panchayath'),('Municipality','Municipality')])
    old_ward_count=models.IntegerField()
    new_ward_count=models.IntegerField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table='localbody'

#creating table for meeting report
class MeetingReport(models.Model):
    meeting_report_id=models.AutoField(primary_key=True)
    constituency=models.ForeignKey(Constituency,on_delete=models.CASCADE)
    local_body=models.ForeignKey(LocalBody,on_delete=models.CASCADE)
    ward_number = models.IntegerField(null=True)
    ward_incharge=models.CharField(max_length=200,null=True)
    office_bearer_name=models.CharField(max_length=90)
    mobile_number=models.IntegerField()
    meeting_date=models.DateField()
    number_of_attendees=models.IntegerField()
    image1=models.ImageField(upload_to='photos/')
    image2=models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"{self.constituency.name} - {self.local_body.name} - {self.meeting_date}"

    class Meta:
        db_table='meeting_report'


class MeetingReportAdmin(admin.ModelAdmin):
    list_display = ('meeting_date', 'constituency', 'local_body', 'ward_number', 'ward_incharge', 'office_bearer_name')
    list_filter = ('meeting_date', 'constituency', 'local_body')
    search_fields = ('ward_incharge', 'office_bearer_name')