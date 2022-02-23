from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='media/profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed
    # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image



class Post(models.Model):
      title = models.CharField(max_length =200, unique=True)
      #author = models.ForeignKey(User, on_delete = models.CASCADE)
      owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
      body = models.TextField(max_length = 600)
      created_on = models.DateTimeField(auto_now_add = True)
      updated_on = models.DateTimeField(auto_now =True)
      
      comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through = 'Comment', related_name = "my_comments")
      
      def __str__(self):
         
         return self.title
         
class Comment(models.Model):
      body = models.TextField(max_length = 600)
      post = models.ForeignKey(Post, on_delete = models.CASCADE)
      owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
      created_on = models.DateTimeField(auto_now_add = True)
      updated_on = models.DateTimeField(auto_now =True)
      
      def __str__(self):
          if len(self.body) <=20:
             return self.body
          else:
             return self.body[:20] + '...'
      
