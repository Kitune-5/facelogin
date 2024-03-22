from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to='photos')
    bio = models.TextField()
    reg_number = models.CharField(max_length = 20)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"profile of {self.user.username}"
    
    
class LoginHistory(models.Model):
    user=models.CharField(max_length=200,null=True)
    count=models.IntegerField(default=0,blank=True,null=True)
    
    def __str__(self):
        return self.user