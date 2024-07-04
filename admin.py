from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import user_details,exercise_detail
# Register your models here.
admin.site.register(user_details)
admin.site.register(exercise_detail)
 