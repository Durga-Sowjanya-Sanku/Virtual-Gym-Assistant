from django.db import models

# Create your models here.

class user_details(models.Model):
    user_name=models.CharField(max_length=30, primary_key=True)
    age=models.IntegerField(default=0)
    gender=models.CharField(max_length=15,null=True)
    height=models.IntegerField(default=0)
    weight=models.IntegerField(default=0)
    email=models.CharField(max_length=30,null=True)
    mobile_number=models.CharField(max_length=10,null=True)
    password=models.CharField(max_length=15)

class exercise_detail(models.Model):
    activity_id=models.CharField(max_length=30)
    date_time=models.DateTimeField()
    user_name=models.ForeignKey(user_details,on_delete=models.CASCADE)
    duration=models.IntegerField()
    repetitions=models.IntegerField()
    calories_burned=models.IntegerField()



