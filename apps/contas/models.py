import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,unique=True,null=True)
    email = models.EmailField(unique=True,max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    force_change_password = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def requires_password_change(self):
        return self.force_change_password
        
    def save(self, *args, **kwargs):
        get_email = self.email.split("@")[0]
        email = re.sub(r"[^a-zA-Z0-9]","",get_email)
        self.username = email
        super(MyUser, self).save(*args, **kwargs)