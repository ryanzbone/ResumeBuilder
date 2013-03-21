from django import forms
from django.forms import extras
from builder.models import WorkExperience, VolunteerExperience, Project

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	email = forms.EmailField(required=False)
	message = forms.CharField(widget=forms.Textarea)

	def clean_messgae(self):
		message = self.cleaned_data['message']
		num_words = len(message.split())
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message


class SignUpForm(forms.Form):
	firstName = forms.CharField()
	lastName = forms.CharField()
	email = forms.EmailField()
	username = forms.CharField()
	password = forms.CharField()

class WorkExperienceForm(forms.ModelForm):
	class Meta:
		model = WorkExperience
		# startDate = forms.DateField(widget=extras.widgets.SelectDateWidget())
		# exclude = ('user',)

class VolunteerExperienceForm(forms.ModelForm):
	class Meta:
		model = VolunteerExperience

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project