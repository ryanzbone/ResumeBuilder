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

# Used for exporting docx
from docx import *

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
	return {
		'user': request.user, 
		'userProfile': UserProfile.objects.get(user=userId),
		'workExperience': WorkExperience.objects.filter(user=userProfile),
		'projects': Project.objects.filter(user=userProfile),
		'volunteerExperience': VolunteerExperience.objects.filter(user=userProfile),
		'code': CodeSnippet.objects.filter(user=userProfile),
		}

def export_pdf (request, userId):
	raise Http404

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

	# Declare arrays to store user info for writing
	profileInfo = []
	code = []
	projectInfo = []
	workInfo = []
	volunteerInfo = []

	# Get general info
	profileInfo += [
	info['userProfile'].firstName + ' ' + info['userProfile'].lastName,
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

	# Get all project info
	for p in info['projects']:
		projectInfo += [
			'\nTitle: ' + p.title, 
			'URL: ' + p.projectURL, 
			'Description: ' + p.description,
			]

	# Get all code snippets
	for c in info['code']:
		code += [
		'\nTitle: ' + c.title,
		'Description: ' + c.description,
		'Code:\n' + c.code,
	]

	# Get all work expreience 
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

	# Get all volunteering info
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
	
	response.write('\n'.join(profileInfo))
	response.write((u'\n\nPROJECTS\n'))
	response.write('\n'.join(projectInfo))
	response.write((u'\n\nCODE\n'))
	response.write('\n'.join(code))
	response.write((u'\n\nWORK HISTORY\n'))
	response.write('\n'.join(workInfo))
	response.write((u'\n\nVOLUNTEERING\n'))
	response.write('\n'.join(volunteerInfo))

	return response
