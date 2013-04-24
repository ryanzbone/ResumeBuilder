from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from builder.models import UserProfile, Project, WorkExperience, VolunteerExperience
from builder.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Used for PDF export
from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet

# Dictionaries used for adding and editing information through forms
models = { 
	'work': 		WorkExperience,
	'volunteer': 	VolunteerExperience,
	'project': 		Project,
	'other': 		UserProfile,
	'code':			CodeSnippet,
	}
forms = {
	'work': 		WorkExperienceForm,
	'volunteer': 	VolunteerExperienceForm,
	'project': 		ProjectForm,
	'other': 		UserProfileForm,
	'code':			CodeSnippetForm,
	}

# Creates formType form for adding new information
@login_required
def add_form(request, formType):
	exp = models[formType](user=UserProfile.objects.get(user=request.user))
	if request.method == 'POST':
		form = forms[formType](request.POST, instance = exp)
		if form.is_valid():
			form.save()
			redirect = '/profile/' + str(request.user.id)
			return HttpResponseRedirect(redirect)
	else:
		form = forms[formType]
	
	return render(request, 'experience_form.html', locals())

# Loads formType form with information from formID for user to edit or update
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
			redirect = '/profile/' + str(request.user.id)
			return HttpResponseRedirect(redirect)
	else:
		form = forms[formType](instance=formFromId)

	return render(request, 'experience_form.html', locals())

# Renders page where a given entry may be deleted
@login_required
def delete_request(request, formType, formId):
	entry = models[formType].objects.get(id=formId)
	return render(request, 'delete.html', locals())

# "Deletes" the entry by making it not visible on a profile
@login_required
def delete_confirm(request, formType, formId):
	entry = models[formType].objects.get(id=formId)
	if entry.visible != False:
		entry.visible = False
		entry.save()
	else:
		raise Http404 # User is trying to delete something that's already been deleted

	return HttpResponseRedirect('/profile/' + str(request.user.id))

# Renders page for creating new user, rerenders page with already entered info if not everything is valid
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = UserProfile(firstName=new_user.first_name.capitalize(), lastName=new_user.last_name.capitalize(), user=new_user, email=new_user.email)
            new_profile.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)

            return HttpResponseRedirect("/form/edit/other/" + str(new_user.id))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', locals())

# Renders list of user profiles
def index(request):
	userList = UserProfile.objects.filter(visible=True,).order_by('lastName')
	return render(request, 'index.html', {'userList': userList})

# Renders profile page for userId
def profile(request, userId):
	user = request.user
	userProfile = UserProfile.objects.get(user=userId)
	if user.id == userProfile.user.id: 
		isThisUser = True
	else: 
		isThisUser = False
	workExperience = WorkExperience.objects.filter(user=userProfile, visible=True).order_by('-startDate')[:3]
	projects = Project.objects.filter(user=userProfile, visible=True).order_by('-id')[:3]
	volunteerExperience = VolunteerExperience.objects.filter(user=userProfile, visible=True).order_by('-startDate')[:3]
	code = CodeSnippet.objects.filter(user=userProfile, visible=True).order_by('-id')[:3]
	return render(request, 'profile.html', locals())

def view_all(request, userId, entryType):
	user = request.user
	userProfile = UserProfile.objects.get(user=userId)

	if user.id == userProfile.user.id: 
		isThisUser = True
	else: 
		isThisUser = False
	if entryType == 'code' or entryType == 'project':
		order = '-id'
	else:
		order = '-startDate'
	entries = models[entryType].objects.filter(user=userProfile, visible=True).order_by(order)

	return render(request, 'view_all.html', locals())

# Exports a fileType file for a given userId
@login_required
def export_file(request, fileType, userId):
	if fileType == 'txt':
		response = export_txt(request, userId)
	elif fileType == 'pdf':
		response = export_pdf(request, userId)
	# elif fileType == 'doc':
	# 	response = export_doc(request, userId)
	else: 
		raise Http404
	return response

# returns dictionary of user information
def userInfo(request, userId):
	userProfile = UserProfile.objects.get(user=userId)

	profileInfo = []
	projectInfo = []
	workInfo = []
	volunteerInfo = []
	code = []

	profileInfo = [
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

	for p in Project.objects.filter(user=userId, visible=True):
		projectInfo += [
			'\nTitle: ' + p.title, 
			'URL: ' + p.projectURL, 
			'Description: ' + p.description,
			]

	for we in WorkExperience.objects.filter(user=userProfile, visible=True):
		workInfo += [
			'\nJob Title: ' + we.jobTitle, 
			'Location: ' + we.location, 
			'Description: ' + we.description, 
			'Start Date: ' + str(we.startDate),
			'End Date: ' + str(we.endDate),
			'Supervisor: ' + we.supervisorName, 
			'Supervisor Email: ' + we.supervisorEmail,
		]

	for v in VolunteerExperience.objects.filter(user=userProfile, visible=True):
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

	for c in CodeSnippet.objects.filter(user=userProfile, visible=True):
		code += [
			'\nTitle: ' + c.title,
			'Description: ' + c.description,
			'Code:\n' + c.code,
		]

	return {
		'user': request.user, 
		'profileInfo': profileInfo,
		'workInfo': workInfo,
		'projectInfo': projectInfo,
		'volunteerInfo': volunteerInfo,
		'code': code,
		}

# Exports plain text file containg all information a user has entered into the app
@login_required
def export_txt(request, userId):
	# gets dictionary of user information
	info = userInfo(request, userId)

	# Declare response to return as a plain text file named "Career Builder Resume.txt"
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename="Career Builder Resume.txt"'
	if "windows" in request.META['HTTP_USER_AGENT']:
		newline = '\r\n'
		response.write(u'WINDOWS')
	else:
		newline = '\n'

	response.write(newline.join(info['profileInfo']))
	response.write((u'\n\nPROJECTS\n'))
	response.write(newline.join(info['projectInfo']))
	response.write((u'\n\nCODE\n'))
	response.write(newline.join(info['code']))
	response.write((u'\n\nWORK HISTORY\n'))
	response.write(newline.join(info['workInfo']))
	response.write((u'\n\nVOLUNTEERING\n'))
	response.write(newline.join(info['volunteerInfo']))

	return response

# Exports PDF containing all infomation a user has entered into the app
@login_required
def export_pdf (request, userId):
	# Get info to print
	info = userInfo(request, userId)

	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Career Builder Resume.pdf"'

	# Create the PDF object, using the BytesIO object as its "file."
	buffer = StringIO()
	doc = SimpleDocTemplate(buffer, pagesize=letter)
	Story = []
	stylesheet = getSampleStyleSheet()
	style = stylesheet['Normal']

	# Append user information into Story. 
	# "counter" used for formatting - keeps track of what's been printed and allows for new line between project, work, etc entries
	Story.append(Paragraph(info['user'].first_name + ' ' + info['user'].last_name, style))
	Story.append(Spacer(1, 12))

	for i in info['profileInfo']:
		Story.append(Paragraph(i, style))
	
	Story.append(Spacer(1, 12))
	Story.append(Paragraph('Projects', style))
	Story.append(Spacer(1, 12))

	counter = 0

	for p in info['projectInfo']:
		Story.append(Paragraph(p, style))
		counter += 1
		if counter > 2:
			Story.append(Spacer(1, 12))
			counter = 0

	Story.append(Spacer(1, 12))
	Story.append(Paragraph('Code Snippets', style))
	Story.append(Spacer(1, 12))

	for c in info['code']:
		if counter < 2:
			Story.append(Paragraph(c, style))
			counter += 1
		else:
			Story.append(Preformatted(c, stylesheet['Code']))
			Story.append(Spacer(1, 12))
			counter = 0

	Story.append(Spacer(1, 12))
	Story.append(Paragraph('Work History', style))
	Story.append(Spacer(1, 12))

	for w in info['workInfo']:
		Story.append(Paragraph(w, style))
		counter += 1
		if counter > 6:
			Story.append(Spacer(1, 12))
			counter = 0

	Story.append(Spacer(1, 12))
	Story.append(Paragraph('Volunteering', style))
	Story.append(Spacer(1, 12))

	for v in info['volunteerInfo']:
		Story.append(Paragraph(v, style))
		counter += 1
		if counter > 7:
			Story.append(Spacer(1, 12))
			counter = 0

	# Build the document, get the value of the BytesIO buffer and write it to the response.
	doc.build(Story)
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)

	return response
