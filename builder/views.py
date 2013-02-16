from django.http import HttpResponse
from django.shortcuts import render_to_response

from builder.models import UserProfile

def index(request):
	userList = UserProfile.objects.all()
	return render_to_response('index.html', {'userList': userList})

def profile(request, id):
	user = UserProfile.objects.get(pk = id)
	return render_to_response('profile.html', {'user': user})
	#return HttpResponse("User %s" % user)
