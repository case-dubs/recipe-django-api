# Database models.

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):
    # Manager for users
    # make sure "create_user" method is spelled correctly
    # default password to None for cases where you create a user that doesn't yet have a password
    # extra_fields allows us to pass key-word arguments to model. So, anytime you want to add new fields in, you don't have to create a new user method (eg: you want to pass a name field that will be added in when user model is created)
    def create_user(self, email, password=None, **extra_fields):
        # Create, save and return a new user
        if not email:
            raise ValueError("Use must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # This passes the password and encrypts it
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # Create and return a new superuser
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Define a new class based from AbstractBaseUser (functionality for base user system) and PermissionsMixin (contains fields needed for permissions feature)
class User(AbstractBaseUser, PermissionsMixin):
    # User in the system
    # need to make sure all email addresses in system are unique
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assigning our custom UserManager
    objects = UserManager()
    USERNAME_FIELD = 'email'