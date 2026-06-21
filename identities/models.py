from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Context(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ContextProfile(models.Model):
    account = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="context_profiles"
    )

    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE,
        related_name="profiles"
    )

    display_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    social_media = models.TextField(blank=True)
    organization = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # avoid duplicated profiles for the same context
    class Meta:
        unique_together = ('account', 'context')

    def __str__(self):
        return f"{self.account.username} - {self.context.name}"

class RequesterType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Policy(models.Model):
    account = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="policies"
    )
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    requester_type = models.ForeignKey(
        RequesterType,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'account',
                    'context',
                    'requester_type'
                ],
                name='unique_user_context_requester'
            )
        ]

    can_view_display_name = models.BooleanField(default=True)
    can_view_email = models.BooleanField(default=False)
    can_view_phone = models.BooleanField(default=False)
    can_view_job_title = models.BooleanField(default=False)
    can_view_linkedin = models.BooleanField(default=False)
    can_view_social_media = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.username} - {self.context.name} - {self.requester_type.name}"