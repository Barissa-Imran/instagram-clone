from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

user = get_user_model()

class Profile(models.Model):
    """Handle profile data for all users"""
    account = models.OneToOneField(user, related_name='profile',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    picture = models.ImageField(
        default='', upload_to='profile_pics'
    )
    followers = models.ManyToManyField(user, related_name='followers')
    following = models.ManyToManyField(user, related_name='following')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # resize the profile image before save
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)

class Post(models.Model):
    """Handle posts by users"""
    account = models.ForeignKey(user, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts')
    caption = models.TextField()
    like = models.ManyToManyField(user, blank=True, related_name='likes')
    date_posted = models.DateTimeField(auto_now_add=True)

    # resize the image to instagram default before saving
    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 1080 or img.width > 1350:
            output_size = (1080, 1350)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.username
    
    # send notification if the user has followed and allowed notifications to the post author in save method

class Comment(models.Model):
    """Handle comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    commentor = models.ForeignKey(user, related_name='commentor', on_delete=models.CASCADE)
    commentee = models.ForeignKey(user, related_name='commentee', on_delete=models.CASCADE)
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment by {self.commentor} on {self.commentee}'
    
    #send notification to the poster


