from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_age', 'current_follows_count')
    search_fields = ('user__username',)


admin.site.register(Profile, ProfileAdmin)
