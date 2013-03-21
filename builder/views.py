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

def search_form(request):
	return render_to_response('search_form.html')

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

def experience_form(request, experienceType):
	if experienceType == 'work':
		exp = WorkExperience( )
		if request.method == 'POST':
			form = WorkExperienceForm(request.POST,instance=exp )
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/contact/thanks')
		else:
			form = WorkExperienceForm(instance=exp)
	elif experienceType == 'volunteer':
		exp = VolunteerExperience()
		if request.method == 'POST':
			form = VolunteerExperienceForm(request.POST,instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/contact/thanks')
		else:
			form = VolunteerExperienceForm(instance=exp)
	elif experienceType == 'project':
		exp = Project()
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/contact/thanks')
		else:
			form = ProjectForm(instance=exp)
	else:
		raise Http404
	
	return render(request, 'experience_form.html', locals())

# def work_experience_form(request):
# 	exp = WorkExperience( )
# 	if request.method == 'POST':
# 		form = WorkExperienceForm(request.POST,instance=exp )
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/contact/thanks')
# 	else:
# 		form = WorkExperienceForm(instance=exp)
# 	return render(request, 'work_experience_form.html', locals())

# def volunteer_experience_form(request):
# 	exp = VolunteerExperience()
# 	if request.method == 'POST':
# 		form = VolunteerExperienceForm(request.POST,instance=exp)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/contact/thanks')
# 	else:
# 		form = VolunteerExperienceForm(instance=exp)
# 	return render(request, 'volunteer_experience_form.html', locals())

