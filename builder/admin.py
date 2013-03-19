from django.contrib import admin
from builder.models import UserProfile, Project, WorkExperience, VolunteerExperience

class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    
class WorkExperienceInline(admin.StackedInline):
    model = WorkExperience
    extra = 1

class VolunteerExperienceInline(admin.StackedInline):
    model = VolunteerExperience
    extra = 0

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email')
    search_fields = ('firstName', 'lastName')
    list_filter = ('school', 'degree')
    fieldsets = (
        (None,              {'fields': ('user', 'image', 'firstName', 'lastName')}),
        ('Contact Info',    {'fields': ('email', 'phone', 'altPhone', 'url')}),
        ('Education',       {'fields': ('school', 'degree', 'altDegree')}),
        ('Other',              {'fields': ('altInfo', 'hobbies', 'clients', 'interests')})
    )
    inlines = [ProjectInline, WorkExperienceInline, VolunteerExperienceInline]

admin.site.register(UserProfile, UserProfileAdmin)
