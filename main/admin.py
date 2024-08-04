from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Faculty)
admin.site.register(Review)
admin.site.register(Department)
admin.site.register(Opinions)