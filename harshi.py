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

    
