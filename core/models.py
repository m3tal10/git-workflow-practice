from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self,email,password=None, **kwargs):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user= self.model(email= self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,email,password):
        super_user= self.create_user(email,password)
        super_user.is_staff= True
        super_user.is_superuser= True
        super_user.save(using=self.db)
        return super_user

class User(AbstractBaseUser, PermissionsMixin):
    """Custome user model that supports using email instead of username"""
    email= models.EmailField(max_length=255, unique=True)
    name= models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)

    objects= UserManager()

    USERNAME_FIELD= 'email'