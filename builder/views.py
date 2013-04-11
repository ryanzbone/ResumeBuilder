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

# Used for exporting docx
# from docx import *





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


# Renders list of user profiles
def index(request):
	userList = UserProfile.objects.all()
	return render(request, 'index.html', {'userList': userList})

# Renders profile page for userId
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
	code = CodeSnippet.objects.filter(user=userProfile)
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

# Exports a fileType file for a given userId
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

	for p in Project.objects.filter(user=userId):
		projectInfo += [
			'\nTitle: ' + p.title, 
			'URL: ' + p.projectURL, 
			'Description: ' + p.description,
			]

	for we in WorkExperience.objects.filter(user=userProfile):
		workInfo += [
			'\nJob Title: ' + we.jobTitle, 
			'Location: ' + we.location, 
			'Description: ' + we.description, 
			'Start Date: ' + str(we.startDate),
			'End Date: ' + str(we.endDate),
			'Supervisor: ' + we.supervisorName, 
			'Supervisor Email: ' + we.supervisorEmail,
		]

	for v in VolunteerExperience.objects.filter(user=userProfile):
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

	for c in CodeSnippet.objects.filter(user=userProfile):
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

def export_doc(request, userId):
	info = userInfo(request, userId)
	relationships = relationshiplist()
	document = newdocument()
	body = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]

	body.append(heading(info['userProfile'].firstName + ' ' + info['userProfile'].lastName, 1))
	profileInfo = [
		'Email: ' + info['userProfile'].email,
		'Website: ' + info['userProfile'].url,
		'Phone: ' + info['userProfile'].phone,
		'Altenate Phone: ' + info['userProfile'].altPhone,
		'School: ' + info['userProfile'].school,
		'Degree: ' + info['userProfile'].degree,
		'Alternate Degree: ' + info['userProfile'].altDegree,
		'Other Info: ' + info['userProfile'].altInfo,
		'Hobbies: ' + info['userProfile'].hobbies,
		'Clients: ' + info['userProfile'].clients,
		'Interests: ' + info['userProfile'].interests,
	]

	for i in profileInfo:
		body.append(paragraph(i, style='ListBullet'))

	projectInfo = []
	workInfo = []
	volunteerInfo = []

	for p in info['projects']:
		projectInfo += [
			'\nTitle: ' + p.title, 
			'URL: ' + p.projectURL, 
			'Description: ' + p.description,
			]

	for we in info['workExperience']:
		workInfo += [
			'\nJob Title: ' + we.jobTitle, 
			'Location: ' + we.location, 
			'Description: ' + we.description, 
			'Start Date: ' + str(we.startDate),
			'End Date: ' + str(we.endDate),
			'Supervisor: ' + we.supervisorName, 
			'Supervisor Email: ' + we.supervisorEmail,
		]

	for v in info['volunteerExperience']:
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

	for p in projectInfo:
		body.append(paragraph(p))
	for w in workInfo:
		body.append(paragraph(w))
	for v in volunteerInfo:
		body.append(paragraph(v))

	# Create our properties, contenttypes, and other support files

	title    = 'Career Builder Resume'
	subject  = 'Work done for the OCIO'
	creator  = info['userProfile'].firstName + ' ' + info['userProfile'].lastName
	keywords = ['resume', 'ocio', 'career', 'work', 'project']

	coreprops = coreproperties(title=title, subject=subject, creator=creator, keywords=keywords)
    
	appprops = appproperties()
	thecontenttypes = contenttypes()
	thewebsettings = websettings()
	thewordrelationships = wordrelationships(relationships)

    # Save our document
	# savedocx(document, coreprops, appprops, thecontenttypes, thewebsettings, thewordrelationships, 'Career Builder Resume.docx')

	response = HttpResponse(document, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
	response['Content-Disposition'] = 'attachment; filename="A Career Builder Resume.docx"'

	return response

# Exports plain text file containg all information a user has entered into the app
def export_txt(request, userId):
	# gets dictionary of user information
	info = userInfo(request, userId)

	# Declare response to return as a plain text file named "Career Builder Resume.txt"
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename="Career Builder Resume.txt"'
	
	response.write('\n'.join(info['profileInfo']))
	response.write((u'\n\nPROJECTS\n'))
	response.write('\n'.join(info['projectInfo']))
	response.write((u'\n\nCODE\n'))
	response.write('\n'.join(info['code']))
	response.write((u'\n\nWORK HISTORY\n'))
	response.write('\n'.join(info['workInfo']))
	response.write((u'\n\nVOLUNTEERING\n'))
	response.write('\n'.join(info['volunteerInfo']))

	return response

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
