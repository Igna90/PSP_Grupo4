from django.contrib import admin
from nucleo.models import User,Category,Project,Participate

admin.site.register(User)
# admin.site.register(Client)
# admin.site.register(Employees)
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Participate)
# Register your models here.
