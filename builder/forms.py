from django import forms
from builder.models import UserProfile

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

class WorkExperienceForm(forms.Form):
	user = forms.ModelChoiceField(queryset=UserProfile.objects.all())
	jobTitle = forms.CharField()
	startDate = forms.DateField()
	endDate = forms.DateField(required=False)
	description = forms.CharField(widget=forms.Textarea)
	supervisorName = forms.CharField()
	supervisorEmail = forms.CharField()
	location = forms.CharField()

