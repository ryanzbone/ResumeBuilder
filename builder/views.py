from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from builder.models import UserProfile, Project, WorkExperience
from builder.forms import *

def index(request):
	userList = UserProfile.objects.all()
	return render(request, 'index.html', {'userList': userList})

def profile(request, name):
	name = name.rsplit("-")
	user = UserProfile.objects.get(firstName__istartswith = name[0], lastName__istartswith = name[1])
	# user = UserProfile.objects.get(pk = id)
	return render(request, 'profile.html', {'user': user})
	#return HttpResponse("User %s" % user)

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

def work_experience_form(request):
	if request.method == 'POST':
		form = WorkExperienceForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			exp = WorkExperience(jobTitle = cd['jobTitle'], startDate = cd['startDate'], 
				endDate = cd['endDate'], description = cd['description'], supervisorName = cd['supervisorName'], 
				supervisorEmail = cd['supervisorEmail'], location = cd['location'], user = cd['user'])
			exp.save()
			return HttpResponseRedirect('/')
	else:
		form = WorkExperienceForm()
	return render_to_response('work_experience_form.html', {'form': form}, context_instance=RequestContext(request))



