from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Posts(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField()
    body = models.CharField(max_length = 500)


    url = models.URLField(blank = True, null = True)
    image = models.ImageField(upload_to = 'images/')
    poster = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:50] + ' ...'

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
