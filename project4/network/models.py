from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

def limit(s,n): return s[:n-1-(s+" ")[n-1::-1].find(" ")]

class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "username" : self.username,
            "following" : [follower.username for follower in self.following.all()],
            "following_count" : self.following.count(),
            "followers_count" : self.followers.count(),
            "followers" : [follower.username for follower in self.followers.all()],
            "posts" : [post.serialize() for post in self.persons_posts.all()]
        }

class Post(models.Model):
    content = models.CharField(max_length=280)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username", related_name="persons_posts")
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def __str__(self):
        return f"{self.creator}: {limit(self.content, 50)}"

    def serialize(self):
        return {
            "id" : self.pk,
            "content" : self.content,
            "creator" : self.creator.username,
            "time" : self.time.strftime("%b %d %Y, %I:%M %p"),
            "likes" : [liker.username for liker in self.likes.all()],
            "likes_count" : self.likes.all().count()
        }