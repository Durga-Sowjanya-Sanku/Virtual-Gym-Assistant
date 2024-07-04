from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import user_details,exercise_detail
from django.contrib import messages 

#libraries for voice assisstant 
import datetime
import pythoncom
import app.scripts.voice_assisstant as va


# Initialize the COM environment
pythoncom.CoInitialize()

#libraries for exercise detection
import numpy as np
from app.scripts.body_part_angle import BodyPartAngle
from app.scripts.utils import *
from app.scripts.execution import TypeOfExercise
import app.scripts.main
import app.scripts.start
from datetime import datetime, timedelta 

user=user_details.objects.all().first()
user_name=user.user_name
# to render the main login page 
def members(request):
    return render(request,'main.html')

# to render signup page for new users
def signup(request):
    return render(request,'signup.html')

# to create an account for the new user
def create_acc(request):
    if request.method == 'POST':   
        data=request.POST
        height= 0 if data.get('height')=='' else data.get('height')
        age= 0 if data.get('age')=='' else data.get('age')
        weight= 0 if data.get('weight')=='' else data.get('weight')
        mb=0 if data.get('mobile_number')=='' else data.get('mobile_number')
        f=user_details(user_name=data.get('user_name'),age=age,gender=data.get('gender'),
                   height=height,weight=weight,email=data.get('email'),
                   mobile_number=mb,password=data.get('password'))
        f=f.save()
        messages.info(request,'Account created')
        return render(request,'main.html')
    else:
        return render(request,'signup.html')

# to render the dashboard if the login details match
def login(request):
    user=request.GET['username']
    pswd=request.GET['password']
    global user_name
    user_name=user 
    user_det=user_details.objects.filter(user_name=user,password=pswd)
    if user_det.exists():
        va.speak("welcome"+user)
        user_name=user
        template=loader.get_template('dashboard.html')
        context={
        'user_det' : user_det,
    }
        return HttpResponse(template.render(context,request))
        #return render(request,'dashboard.html',{'user_det':user_det})
    else:
        messages.info(request,'Data did not match')
        return render(request,'main.html')
    
#to render dashboard
def dashboard(request):
    user_det=user_details.objects.filter(user_name=user_name)
    #return render(request,'dashboard.html')
    template=loader.get_template('dashboard.html')
    context={
        'user_det': user_det,
    }
    return HttpResponse(template.render(context,request))

# to render the page to show past insights
def past_data(request):
    user_data=user_details.objects.all()
    fit_act=exercise_detail.objects.filter(user_name=user)
    template=loader.get_template('past_data.html')
    context={
        'user_det' : user_data,
        'fitness_activities' : fit_act,
    }
    return HttpResponse(template.render(context,request))

# to load the page for exercises
def exercises(request):
    return render(request,'exercises.html')
 
# dummy code
def start_exercise(request):
    #run python script and go back to exercises page
    exercise_name = request.GET.get('button_name', '')
    result= app.scripts.start.exercise(exercise_name)
    st=result[1]
    en=result[2]
    dur=(en-st).total_seconds()
    f=exercise_detail(activity_id=result[0],date_time=result[1],user_name_id=user_name,duration=dur//60,repetitions=result[3],
    calories_burned=result[4])
    f=f.save()
    return render(request,'exercises.html')
  