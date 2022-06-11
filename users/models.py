from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Visitor(models.Model):
    user = models.OneToOneField('User', null=False, on_delete=models.CASCADE, related_name='visitor')
    session_key = models.CharField(null=True, max_length=40)


class UserProfileManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:  # validating email
            raise ValueError('EMAIL IS REQUIRED!!')
        if not username:  # validating username
            raise ValueError('USERNAME IS REQUIRED!!')

        email = self.normalize_email(email)  # normalizing the email
        user = self.model(email=email, username=username)  # creating user
        user.set_password(password)  # making the password hashed
        user.save(using=self._db)  # saving the user object

        return user

    """
    Function for creation of a superuser
    """

    def create_superuser(self, email, username, password):

        user = self.create_user(email=email, username=username, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    profile = models.OneToOneField('staff.StaffProfile', on_delete=models.CASCADE, null=True, related_name='user')

    privilege = models.SmallIntegerField(null=True, default=4)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = UserProfileManager()  # creating a profile manager for controlling the users model via command line

    USERNAME_FIELD = 'email'  # overriding the username field and using the email field for authentication
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['username']  # A list of Fields that are required for user creation

    ''' Creating s string representation of a user '''
    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)

    def get_admin_deactivation_url(self):
        return reverse("deactivate_admin", kwargs={"admin_id": self.pk})


class CodeBase(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    owner = GenericForeignKey("content_type", "object_id")
    rfid_code = models.CharField(unique=True, blank=True, null=True, max_length=20)

    def __str__(self):
        return self.owner.email

    # class Meta:
    #     ordering = ('owner',)
