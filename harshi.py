from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import rolestbl,campustbl,depttbl,coursetbl,User,stuhead_vol_profiletbl
# from .decorators import unauthenticated_user

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


#---------------------------------------------------campus views-----------------------------------------------------------------
def campusaddformfunc(request):
    form =campusaddform()
    temp = None
    if campustbl.objects.exists():
        temp = campustbl.objects.all()
    
    context = {'temp':temp, 'form':form}
    if request.method == "POST":
        form = campusaddform(request.POST)
        if form.is_valid():
            messages.success(request, "form saved")
            a = form.save(commit = False)
            a.save()
            form = campusaddform()
        else:
            messages.error(request, "cannot add campus. Invalid information.")

    return render (request,"campusaddform.html", context)

def campusdeletefunc(request, pkid):
    record=campustbl.objects.get(id=pkid)
    print(record)
    record.delete()
    messages.success(request, "record deleted")
    return redirect("campusaddform_url")


def campusupdatefunc(request, pkid):
    record=campustbl.objects.get(id=pkid)
    form = campusaddform(instance=record)
    if request.method == "POST":
        form = campusaddform(request.POST,instance=record)
        if form.is_valid():
            messages.success(request, "form saved")
            print("success")
            a = form.save(commit = False)
            a.save()
            messages.success(request, "Campus form saved")
        else:
            messages.error(request, "cannot update campus. Invalid info.")
        return redirect("campusaddform_url")
    
    context={'form':form}
    return render (request,"campusupdateform.html", context)


#---------------------------------------------------Session views-----------------------------------------------------------------
  
def success(request):
    return HttpResponse('successfully uploaded')
#---------------------------------------------------home views-----------------------------------------------------------------
def homefunc(request):
    return render(request, 'index.html',)

#---------------------------------------------------home views-----------------------------------------------------------------
def dashboardfunc(request):
    return render(request, 'dashboard.html')
#---------------------------------------------------LOGIN view-----------------------------------------------------------------
# @unauthenticated_user
def loginfunc(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("dashboard_url")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render (request,"login.html", context={'form':form})


def logoutfunc(request):
    logout(request)
    return redirect("login_url")


#--------------------------------------------------- Department  views-----------------------------------------------------------------
def deptaddformfunc(request):
    form =deptaddform()
    if depttbl.objects.exists():
        temp = depttbl.objects.all()
    
    context = {'temp':temp, 'form':form}
    if request.method == "POST":
        form = deptaddform(request.POST)
        if form.is_valid():
            messages.success(request, "form saved")
            a = form.save(commit = False)
            a.save()
            form = deptaddform()
        else:
            messages.error(request, "cannot add dept. Invalid information.")
        
        return redirect("deptaddform_url")
    return render (request,"deptaddform.html", context)

def deptdeletefunc(request, pkid):
    record=depttbl.objects.get(id=pkid)
    print(record)
    record.delete()
    messages.success(request, "record deleted")
    return redirect("deptaddform_url")


def deptupdatefunc(request, pkid):
    record=depttbl.objects.get(id=pkid)
    form = deptaddform(instance=record)
    if request.method == "POST":
        form = deptaddform(request.POST,instance=record)
        if form.is_valid():
            messages.success(request, "form saved")
            print("success")
            a = form.save(commit = False)
            a.save()
            messages.success(request, "manga form saved")
        else:
            messages.error(request, "cannot update department. Invalid info.")
        return redirect("deptaddform_url")
    
    context={'form':form}
    return render (request,"deptupdateform.html", context)



#--------------------------------------------------- Course  views-----------------------------------------------------------------
def courseaddformfunc(request):
    form =courseaddform()
    temp = None
    if coursetbl.objects.exists():
        temp = coursetbl.objects.all()
    
    context = {'temp':temp, 'form':form}
    if request.method == "POST":
        form = courseaddform(request.POST)
        if form.is_valid():
            messages.success(request, "form saved")
            a = form.save(commit = False)
            a.save()
            form = courseaddform()
        else:
            messages.error(request, "cannot add course. Invalid information.")

    return render (request,"courseaddform.html", context)

def coursedeletefunc(request, pkid):
    record=coursetbl.objects.get(id=pkid)
    print(record)
    record.delete()
    messages.success(request, "record deleted")
    return redirect("courseaddform_url")


def courseupdatefunc(request, pkid):
    record=coursetbl.objects.get(id=pkid)
    form = courseaddform(instance=record)
    if request.method == "POST":
        form = courseaddform(request.POST,instance=record)
        if form.is_valid():
            messages.success(request, "form saved")
            print("success")
            a = form.save(commit = False)
            a.save()
            messages.success(request, "manga form saved")
        else:
            messages.error(request, "cannot update department. Invalid info.")
        return redirect("courseaddform_url")
    
    context={'form':form}
    return render (request,"courseupdateform.html", context)


#-----------------------------------------------------------------------
# Student head dashboard -----------------------------------------------------------
def studenthead_dashboard_func(request):
    
    return render(request, 'studenthead/sh_dashboard.html')

def sh_volunteer_list_func(request):
    try:
        if request.User.stuhead_vol_profiletbl.wing:
            currentwing = request.User.stuhead_vol_profiletbl.wing
            print(currentwing)

        templist = stuhead_vol_profiletbl.objects.filter(wing=currentwing)
        context = {'templist':templist,'currentwing':currentwing}
        return render(request, 'volunteer_list.html', context)
    except:
        messages.error(request,"Unable to fetch data! sorry!")
        return render(request, 'studenthead/sh_volunteer_list.html')

def sh_volunteer_add_func(request):
    form1 = UserAddForm
    form2 = VolunteerAddForm

    if request.method == "POST":
        form1 = UserAddForm(request.POST)
        form2 = VolunteerAddForm(request.POST)

        if form1.is_valid() & form2.is_valid():
            tempuser = form1.save(commit=False)
            tempuser.roles = rolestbl.objects.filter(roles = 'volunteer').first()
            print(tempuser.roles)
            tempuser.save()
            tempvol = form2.save(commit=False)
            tempvol.user = tempuser
            tempvol.save()

            # send email code with pwd and OTP and link to login page

            messages.success(request, "Volunteer registered successfully")
            return redirect("sh_volunteer_list_url")
        else:
            print(form1.errors)
            print(form2.errors)
            messages.error(request, "Invalid data! please check the form.")

    context = {"form1":form1,"form2":form2}
    return render(request, 'studenthead/sh_volunteer_add.html',context)


def sessionaddformfunc(request):
    form =sessionaddform()
    temp = None
    if sessiontbl.objects.exists():
        temp = sessiontbl.objects.all()
    
    context = {'temp':temp, 'form':form}
    if request.method == "POST":
        form = sessionaddform(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, "form saved")
            a = form.save(commit = False)
            a.save()
            form = sessionaddform()
        else:
            messages.error(request, "cannot add session. Invalid information.")
    return render (request,"sessionaddform.html", context)


def sessiondeletefunc(request, pkid):
    record=sessiontbl.objects.get(id=pkid)
    print(record)
    record.delete()
    messages.success(request, "record deleted")
    return redirect("sessionaddform_url")


def sessionupdatefunc(request, pkid):
    record=sessiontbl.objects.get(id=pkid)
    form = sessionaddform(instance=record)
    if request.method == "POST":
        form = sessionaddform(request.POST,request.FILES,instance=record)
        if form.is_valid():
            messages.success(request, "form saved")
            print("success")
            a = form.save(commit = False)
            a.save()
            messages.success(request, "session form saved")
        else:
            messages.error(request, "cannot update session. Invalid info.")
        return redirect("sessionaddform_url")
    
    context={'form':form}
    return render (request,"sessionupdateform.html", context)


def usersessionlistfunc(request):
    if sessiontbl.objects.exists():
        temp = sessiontbl.objects.all()
        context = {'temp':temp}
        return render(request, 'usersessionlist.html', context)
    else:
        if not sessiontbl.objects.exists():
            return render(request, 'usersessionlist.html',)
    return render(request, 'usersessionlist.html', context)




#_______________________________________________________________accounts models_____________________________________________________________


from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager

#_________________________________________________________________roles table____________________________________________________________
class rolestbl(models.Model):
    roles = models.CharField(max_length=30,null=False,unique=True)

    def __str__(self):
        return (self.roles)

#_________________________________________________________________campus table____________________________________________________________
class campustbl(models.Model):
    campus= models.CharField(max_length=50,null=False,verbose_name="Campus")

    def __str__(self):
        return (self.campus)

#_________________________________________________________________department table_______________________________________________________
class depttbl(models.Model):
    dept = models.CharField(max_length=50,null=False,verbose_name="Department")

    def __str__(self):
        return (self.dept)

#_________________________________________________________________course table___________________________________________________________
class coursetbl(models.Model):
    course=models.CharField(max_length=70,null=False, verbose_name="coursename")


#_______________________________________________________________customizing user table________________________________________________
class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(('first name'), max_length=30, null=False)
    last_name = models.CharField(('last name'), max_length=30, null=False)
    mobile=models.CharField(max_length=10, verbose_name="mobile", null=False)
    email = models.EmailField(('email address'), unique=True, null=False)
    usercreated_date = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    roles = models.ForeignKey(rolestbl,null=True, on_delete=models.SET_NULL )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)




#_________________________________________________________________student head and volunteer profile table___________________________________________________________
#(common profile table used for both studenthead and volunteer)

class stuhead_vol_profiletbl(models.Model):
    WING_CHOICES= (
        ('onetoone', 'onetoone'),
        ('peer', 'peer'),
        )
    campus =models.ForeignKey(campustbl,null=True, on_delete=models.SET_NULL )
    course =models.ForeignKey(coursetbl,null=True, on_delete=models.SET_NULL )
    wing=models.CharField(max_length=20, choices=WING_CHOICES, verbose_name="Wing")
    sh_year=models.DateField(  verbose_name="Year of being Studenthead")
    v_year=models.DateField(  verbose_name="Year of being Volunterer")
    class_sec=models.CharField(max_length=20, choices=WING_CHOICES, verbose_name="Class_sec")
    passout=models.PositiveIntegerField(default=0, verbose_name="Passout")
    total_session_hrs=models.PositiveIntegerField(default=0, verbose_name="Total_session_hrs_taken")
    no_of_sessions_conducted=models.PositiveIntegerField(default=0,verbose_name="Numberofsessionsconducted")
    is_assigned=models.BooleanField(default=False)


 #_______________________________________________________________session booking models_____________________________________________________________
from django.db import models

from accounts.models import rolestbl,User,campustbl,depttbl,coursetbl
#________________________________________________________________session table____________________________________________________________
# Create your models here.
class sessiontbl(models.Model):
    session= models.CharField(max_length=30, verbose_name="session")
    description= models.CharField(max_length=200, verbose_name="session")
    session_pic=models.ImageField(null=True, blank=True,upload_to='static/uploadimg/', verbose_name="Photo")
    uploaded_date=models.DateTimeField( auto_now_add=False, verbose_name="Uploaded_date")

    def __str__(self):
        return self.session

#___________________________________________________ one to one session request table____________________________________________________________
class onetoonetickettbl(models.Model):
    ONETICKET_STATUS_CHOICES= (
        ('requested', 'requested'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('closed', 'closed'),
        )
    session = models.ForeignKey(sessiontbl,null=True, on_delete=models.SET_NULL )
    first_name = models.CharField(('first name'), max_length=30, null=False)
    last_name = models.CharField(('last name'), max_length=30, null=False)
    stuemail =models.EmailField(('email address'), null=False)
    mobile = models.CharField( max_length=10, null=False)

    course=models.ForeignKey(User,null=True, on_delete=models.SET_NULL )
    dept=models.ForeignKey(depttbl,null=True, on_delete=models.SET_NULL )
    campus=models.ForeignKey(campustbl,null=True, on_delete=models.SET_NULL )
    regno= models.PositiveIntegerField( null=False)

    ours=models.PositiveIntegerField( null=False, default =1)
    ticket_no=models.PositiveIntegerField( null=True)
    ticket_status=models.CharField(max_length=50, choices=ONETICKET_STATUS_CHOICES, verbose_name="Status")
    request_datetime=models.DateTimeField( auto_now_add=True, verbose_name="Request_datetime")
    v_feedback=models.CharField(max_length=200, null=True, verbose_name="Volunteer Feedback")
    s_feedback=models.CharField(max_length=200, null=True, verbose_name="Student Feedback")

    accepted_date=models.DateTimeField( auto_now_add=False, verbose_name="Accepted_date")

    accepted_by=models.ForeignKey(User,null=True, related_name="accept" ,on_delete=models.SET_NULL )
    assigned_by=models.ForeignKey(User,null=True,related_name="assign" , on_delete=models.SET_NULL )
    assigned_to=models.ForeignKey(User,null=True,related_name="reject" , on_delete=models.SET_NULL )
    rejected_by=models.ManyToManyField(User,blank=True, related_name="rejected" )
    closed_date=models.DateTimeField(  verbose_name="Closed_date")
    hours=models.PositiveIntegerField(default =1)

    def __str__(self):
        return self.self(ticket_no)

    
