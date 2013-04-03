from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from builder.models import UserProfile, Project, WorkExperience, VolunteerExperience
from builder.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Used for exporting CSV information
import csv
import unicodecsv
from cStringIO import StringIO


def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

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
	exp = models[formType](user=UserProfile.objects.get(user=request.user))
	if request.method == 'POST':
		form = forms[formType](request.POST, instance = exp)
		if form.is_valid():
			form.save()
			redirect = '/profile/' + request.user.first_name.lower() + '-' + request.user.last_name.lower()
			return HttpResponseRedirect(redirect)
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
			redirect = '/profile/' + request.user.first_name.lower() + '-' + request.user.last_name.lower()
			return HttpResponseRedirect(redirect)
	else:
		form = forms[formType](instance=formFromId)

	return render(request, 'experience_form.html', locals())


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = UserProfile(firstName=new_user.first_name, lastName=new_user.last_name, user=new_user, email=new_user.email)
            new_profile.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)

            return HttpResponseRedirect("/form/edit/other/" + str(new_user.id))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', locals())


def index(request):
	userList = UserProfile.objects.all()
	return render(request, 'index.html', {'userList': userList})

def profile(request, userId):
	user = request.user
	userProfile = UserProfile.objects.get(user=userId)
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

def export_file(request, fileType, userId):
	if fileType == 'txt':
		response = export_txt(request, userId)
	elif fileType == 'pdf':
		response = export_pdf(request, userId)
	elif fileType == 'doc':
		response = export_doc(request, userId)
	else: 
		raise Http404
	return response

def export_pdf (request, userId):
	raise Http404

def export_doc(request, userId):
	raise Http404

def export_txt(request, userId):
	user = request.user
	userProfile = UserProfile.objects.get(user=userId)
	workExperience = WorkExperience.objects.filter(user=userProfile)
	projects = Project.objects.filter(user=userProfile)
	volunteerExperience = VolunteerExperience.objects.filter(user=userProfile)

	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename="Career Builder Resume.txt"'

	profileInfo = [
		userProfile.firstName + ' ' + userProfile.lastName,
		'Email: ' + userProfile.email,
		'Website: ' + userProfile.url,
		'Phone: ' + userProfile.phone,
		'Altenate Phone: ' + userProfile.altPhone,
		'School: ' + userProfile.school,
		'Degree: ' + userProfile.degree,
		'Alternate Degree: ' + userProfile.altDegree,
		'Other Info: ' + userProfile.altInfo,
		'Hobbies: ' + userProfile.hobbies,
		'Clients: ' + userProfile.clients,
		'Interests: ' + userProfile.interests,
	]

	projectInfo = []
	workInfo = []
	volunteerInfo = []

	for p in projects:
		projectInfo += [
			'\nTitle: ' + p.title, 
			'URL: ' + p.projectURL, 
			'Description: ' + p.description,
			]

	for we in workExperience:
		workInfo += [
			'\nJob Title: ' + we.jobTitle, 
			'Location: ' + we.location, 
			'Description: ' + we.description, 
			'Start Date: ' + str(we.startDate),
			'End Date: ' + str(we.endDate),
			'Supervisor: ' + we.supervisorName, 
			'Supervisor Email: ' + we.supervisorEmail,
		]

	for v in volunteerExperience:
		volunteerInfo += [
			'\nJob Title: ' + v.jobTitle, 
			'Organization: ' + v.organization, 
			'Location: ' + v.location, 
			'Description: ' + v.description, 
			'Start Date: ' + str(v.startDate),
			'End Date: ' + str(v.endDate),
			'Supervisor: ' + v.supervisorName, 
			'Supervisor Email: ' + v.supervisorEmail,
		]
	
	response.write('\n'.join(profileInfo))
	response.write((u'\n\nPROJECTS\n'))
	response.write('\n'.join(projectInfo))
	response.write((u'\n\nWORK HISTORY\n'))
	response.write('\n'.join(workInfo))
	response.write((u'\n\nVOLUNTEERING\n'))
	response.write('\n'.join(volunteerInfo))

	return response
