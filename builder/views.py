from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from builder.models import UserProfile, Project, WorkExperience, VolunteerExperience
from builder.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


models = { 
	'work': 		WorkExperience,
	'volunteer': 	VolunteerExperience,
	'project': 		Project,
	'other': 		UserProfile,
	}
forms = {
	'work': 		WorkExperienceForm,
	'volunteer': 	VolunteerExperienceForm,
	'project': 		ProjectForm,
	'other': 		UserProfileForm,
	}

@login_required
def add_form(request, formType):
	exp = models[formType]()
	if request.method == 'POST':
		form = forms[formType](request.POST, instance = exp)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/contact/thanks')
	else:
		form = forms[formType]
	
	return render(request, 'experience_form.html', locals())

@login_required
def edit_form(request, formType, formId):
	if formType == 'other':
		formFromId = models[formType].objects.get(user=formId)
	else:
		formFromId = models[formType].objects.get(id=formId)
	if request.method == 'POST':
		form = forms[formType](request.POST, instance=formFromId)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/contact/thanks')
	else:
		form = forms[formType](instance=formFromId)

	return render(request, 'experience_form.html', locals())


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = UserProfile(firstName=new_user.first_name, lastName=new_user.last_name, user=new_user)
            new_profile.save()
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', locals())


def index(request):
	userList = UserProfile.objects.all()
	return render(request, 'index.html', {'userList': userList})

def profile(request, name):
	user = request.user
	name = name.rsplit("-")
	userProfile = UserProfile.objects.get(firstName__istartswith = name[0], lastName__istartswith = name[1])
	if user.id == userProfile.user.id: 
		isThisUser = True
	else: 
		isThisUser = False
	workExperience = WorkExperience.objects.filter(user=userProfile)
	projects = Project.objects.filter(user=userProfile)
	volunteerExperience = VolunteerExperience.objects.filter(user=userProfile)
	return render(request, 'profile.html', locals())

@login_required
def edit_profile(request, name):
	edit = True
	response = profile(request, name)
	return response

def search(request):
	errors = []
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append('Enter a search term.')
		elif len(q) > 20:
			errors.append('Please enter at most 20 characters.')
		else:
			projects = Project.objects.filter(title__icontains=q)
			return render_to_response('search_results.html', 
				{'projects': projects, 'query': q})
	return render_to_response('search_form.html', {'errors': errors})

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['ryanzbone@gmail.com'],
			)
			return HttpResponseRedirect('/contact/thanks')
	else:
		form = ContactForm(
			initial={'subject': 'I love your site!'}
		)
	return render_to_response('contact_form.html', {'form': form}, context_instance=RequestContext(request))

def thanks(request):
	return render_to_response('thanks.html')
