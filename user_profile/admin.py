from typing import Any, Dict
from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Profile
# Register your models here.

class ProfileForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = None
        if 'instance' in kwargs:
            user = kwargs['instance']
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['follows'].queryset = Profile.objects.all().exclude(id=user.id)
    
    class Meta:
        model = Profile
        fields = '__all__'
        
    def clean(self) -> Dict[str, Any]:
        user = self.cleaned_data['user']
        if user.profile in self.cleaned_data['follows']:
            raise ValidationError(
                {
                    'follows': f'{user} не может подписаться на самого себя!'
                }
            )
        return super().clean()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_age', 'current_follows_count')
    search_fields = ('user__username',)
    form = ProfileForm

admin.site.register(Profile, ProfileAdmin)
