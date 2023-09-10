from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)
       
       
class CustomUser(AbstractBaseUser, PermissionsMixin):
    customer_id=models.IntegerField(auto_created=True,null=True)
    customer_name=models.CharField(max_length=300,unique=True,null=True)
    email = models.EmailField(unique=True)
    dob=models.DateField(default=timezone.now)
    address=models.CharField(max_length=300,null=True)
    gender = models.CharField(max_length=300,null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def check_password(self, raw_password):
        if raw_password == self.password:
            return True
        else:
            raise ValueError("Incorrect password")
        
    def __str__(self):
            return self.customer_name
    


