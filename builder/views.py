from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from builder.models import UserProfile, Project, WorkExperience, VolunteerExperience
from builder.forms import *

def index(request):
	userList = UserProfile.objects.all()
	return render(request, 'index.html', {'userList': userList})

def profile(request, name):
	name = name.rsplit("-")
	user = UserProfile.objects.get(firstName__istartswith = name[0], lastName__istartswith = name[1])
	workExperience = WorkExperience.objects.filter(user=user)
	projects = Project.objects.filter(user=user)
	volunteerExperience = VolunteerExperience.objects.filter(user=user)
	return render(request, 'profile.html', locals())

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

def add_form(request, formType):
	if formType == 'work':
		exp = WorkExperience( )
		if request.method == 'POST':
			form = WorkExperienceForm(request.POST,instance=exp )
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/profile/thanks')
		else:
			form = WorkExperienceForm(instance=exp)
	elif formType == 'volunteer':
		exp = VolunteerExperience()
		if request.method == 'POST':
			form = VolunteerExperienceForm(request.POST,instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/contact/thanks')
		else:
			form = VolunteerExperienceForm(instance=exp)
	elif formType == 'project':
		exp = Project()
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/contact/thanks')
		else:
			form = ProjectForm(instance=exp)
	# elif formType == 'userprofile':
	# 	exp = 
	else:
		raise Http404
	
	return render(request, 'experience_form.html', locals())

