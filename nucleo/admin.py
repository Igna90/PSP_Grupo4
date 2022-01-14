from django.contrib import admin
from nucleo.models import User,Category,Project,Participate


class ProjectInLine(admin.StackedInline):
    model=Project

class CategoryAdmin(admin.ModelAdmin):
    list_filters=['name']
    ordering=['name']
    list_per_page=5 
    inlines=[ProjectInLine,]
    
    

admin.site.register(User)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Project)
admin.site.register(Participate)
