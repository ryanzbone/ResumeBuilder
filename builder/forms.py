from django import forms
from builder.models import UserProfile, WorkExperience, VolunteerExperience, Project, CodeSnippet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	email = forms.EmailField(required=False)
	message = forms.CharField(widget=forms.Textarea)

	def clean_message(self):
		message = self.cleaned_data['message']
		num_words = len(message.split())
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message

class WorkExperienceForm(forms.ModelForm):
	class Meta:
		model = WorkExperience
		exclude = ('user',)

class VolunteerExperienceForm(forms.ModelForm):
	class Meta:
		model = VolunteerExperience
		exclude = ('user',)


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('user',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('firstName', 'lastName', 'user')

class CodeSnippetForm(forms.ModelForm):
	class Meta:
		model = CodeSnippet
		exclude = ('user',)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user