from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User 
import string

BASE62=string.digits+string.ascii_letters #0-9+a-z_A-Z

def encode(num):
    #converting an integer to base62 string
    if num==0:
        return BASE62[0]
    arr=[]
    while num:
        num, rem=divmod(num,62)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)
        

# Create your models here.
class link_generator(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    link=models.CharField(max_length=10000)
    link_id=models.CharField(max_length=10, unique=True, blank=True)
    created_At=models.DateTimeField(default=timezone.now)
    click_count=models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #only after saving object to the databse we have id
        if not self.link_id:
            self.link_id=encode(self.id)
            super().save(update_fields=['link_id'])




    def __str__(self):
        return f"{self.link_id}->{self.link}"

 