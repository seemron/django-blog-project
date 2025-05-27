from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class PrivatePostAccess(models.Model):
#     email = models.EmailField()
#     post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('email', 'post')

#     def __str__(self):
#         return f"{self.email} -> {self.post.title}"

class AccessRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_requests')
    message = models.TextField(blank=True, null=True)  # Optional message from user
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Approved' if self.is_approved else 'Pending'}"

from django.db import models

class ApprovedEmail(models.Model):
    email = models.EmailField(unique=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.email
