from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#def uploadUserPic(instance, filename):
#    return 'images/%s/profilepicture' % (instance.user.username, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    firstName = models.CharField(max_length = 50, blank = True)
    lastName = models.CharField(max_length = 50, blank = True)
    email = models.EmailField()
    url = models.URLField(blank = True)
    phone = models.CharField(max_length = 20)
    altPhone = models.CharField(max_length = 20, blank = True)
    image = models.ImageField(upload_to='Images', blank = True)
    school = models.CharField(max_length = 100)
    degree = models.CharField(max_length = 100)
    altDegree = models.CharField(max_length = 100, blank = True)
    altInfo = models.TextField('Other information', blank = True)
    hobbies = models.TextField(blank = True)
    clients = models.TextField(blank = True)
    interests = models.TextField(blank = True)
   
    def __unicode__(self):
        #return self.email
        return u'%s %s' %(self.firstName, self.lastName)

    class Meta:
        ordering = ['lastName', 'firstName']

class Project(models.Model):
    user = models.ForeignKey(UserProfile)
    title = models.CharField(max_length = 250)
    projectURL = models.URLField(blank = True)
    description = models.TextField()
    inDevelopment = models.BooleanField()
    isPublic = models.BooleanField(default = True)
    projectImage = models.ImageField('Screen shot', upload_to = 'Images', blank = True)
    highlight = models.BooleanField()
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']

class WorkExperience(models.Model):
    user = models.ForeignKey(UserProfile)
    jobTitle = models.CharField('Job title', max_length = 100)
    startDate = models.DateField('Start date', blank = True)
    endDate = models.DateField('End date', blank = True)
    description = models.TextField('Job description')
    supervisorName = models.CharField('Supervisor name', max_length = 100)
    supervisorEmail = models.EmailField('Supervisor email')
    location = models.CharField(max_length = 250)
    def __unicode__(self):
        return self.jobTitle

    class Meta:
        ordering = ['-startDate']

class VolunteerExperience(models.Model):
    user = models.ForeignKey(UserProfile)
    organization = models.CharField(max_length = 150)
    jobTitle = models.CharField('Title', max_length = 100)
    startDate = models.DateField('Start date', blank = True)
    endDate = models.DateField('End date', blank = True, null=True)
    description = models.TextField('Job description')
    supervisorName = models.CharField('Supervisor name', max_length = 100)
    supervisorEmail = models.EmailField('Supervisor email')
    location = models.CharField(max_length = 250)
    def __unicode__(self):
        return u'%s - %s' % (self.jobTitle, self.organization)

    class Meta:
        ordering = ['-startDate']
