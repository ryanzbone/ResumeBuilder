from django.http import HttpResponse, HttpResponseRedirect, Http404
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
	# # Get user information
	# user = request.user
	# userProfile = UserProfile.objects.get(user=userId)
	# workExperience = WorkExperience.objects.filter(user=userProfile)
	# projects = Project.objects.filter(user=userProfile)
	# volunteerExperience = VolunteerExperience.objects.filter(user=userProfile)

 #    # Create the HttpResponse object with the appropriate PDF headers.
	# response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="Career Builder Resume.pdf"'

	# buffer = BytesIO()
	# p = canvas.Canvas(buffer, pagesize=letter)
	# p.drawString(100, 100, "hello there")
	# p.showPage()
	# p.save()
	# pdf = buffer.getvalue()
	# buffer.close()
	# response.write(pdf)
	# return response

    # buffer = BytesIO()

    # # Create the PDF object, using the BytesIO object as its "file."
    # p = canvas.Canvas(buffer)

    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100, 100, "Hello world.")

    # # Close the PDF object cleanly.
    # p.showPage()
    # p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()
    # buffer.close()
    # response.write(pdf)
    # return response

# @login_required
# def export_csv(request, userId):
	user = request.user
	userProfile = UserProfile.objects.get(user=userId)
	workExperience = WorkExperience.objects.filter(user=userProfile)
	projects = Project.objects.filter(user=userProfile)
	volunteerExperience = VolunteerExperience.objects.filter(user=userProfile)

	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename="Career Builder Resume.txt"'
	w = unicodecsv.writer(response, encoding='utf-8')

	# w.writerow((userProfile.firstName, userProfile.lastName))
	# w.writerow((userProfile.email))
	# w.writerow((userProfile.url))
	# w.writerow((userProfile.phone))
	# w.writerow((userProfile.altPhone))
	# w.writerow((userProfile.school))
	# w.writerow((userProfile.degree))
	# w.writerow((userProfile.altDegree))
	# w.writerow((userProfile.altInfo))
	# w.writerow((userProfile.hobbies))
	# w.writerow((userProfile.clients))
	# w.writerow((userProfile.interests))

	response.write((userProfile.firstName + " " + userProfile.lastName +"\n"))
	response.write((userProfile.email+"\n"))
	response.write((userProfile.url+"\n"))
	response.write((userProfile.phone+"\n"))
	response.write((userProfile.altPhone+"\n"))
	response.write((userProfile.school+"\n"))
	response.write((userProfile.degree+"\n"))
	response.write((userProfile.altDegree+"\n"))
	response.write((userProfile.altInfo+"\n"))
	response.write((userProfile.hobbies+"\n"))
	response.write((userProfile.clients+"\n"))
	response.write((userProfile.interests+"\n"))

	# w.writerow((u'Projects'))
	# for p in projects:
	# 	w.writerow((p.title))
	# 	w.writerow((p.projectURL))
	# 	w.writerow((p.description))

	# w.writerow((u'Work Experience'))
	# for we in workExperience:
	# 	w.writerow((we.jobTitle))
	# 	w.writerow((we.location))
	# 	# w.writerow((we.startDate))
	# 	# w.writerow((we.endDate))
	# 	w.writerow((we.description))
	# 	w.writerow((we.supervisorName))
	# 	w.writerow((we.supervisorEmail))

	# w.writerow((u'Volunteering'))
	# for v in volunteerExperience:
	# 	w.writerow((v.jobTitle))
	# 	w.writerow((v.organization))
	# 	w.writerow((v.location))
	# 	# w.writerow((v.startDate))
	# 	# w.writerow((v.endDate))
	# 	w.writerow((v.description))
	# 	w.writerow((v.supervisorName))
	# 	w.writerow((v.supervisorEmail))

	return response
