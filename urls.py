from django.urls import path
from . import views
from . import scripts
urlpatterns =[
    path('app/',views.members,name='members'),
    path('app/login',views.login,name='login'),
    path('app/signup',views.signup,name='signup'),
    path('app/create_acc',views.create_acc,name='create_acc'),
    path('app/dashboard',views.dashboard,name='dashboard'),
    path('app/past_data',views.past_data,name='past_data'),
    path('app/exercises',views.exercises,name='exercises'),
    path('app/start_exercise',views.start_exercise,name="start_exercise"),
]