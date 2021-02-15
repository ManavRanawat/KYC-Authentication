
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class KYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar=models.BooleanField(default=False)
    voter_card=models.BooleanField(default=False)
    passport=models.BooleanField(default=False)
    driving_license=models.BooleanField(default=False)
    passbook=models.BooleanField(default=False)
    bank_statement=models.BooleanField(default=False)
    pan=models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
   