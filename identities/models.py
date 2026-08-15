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
    pronouns = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=150, blank=True)
    university = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    preferred_contact_way = models.CharField(max_length=50, blank=True)

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
    can_view_nickname = models.BooleanField(default=False)
    can_view_organization = models.BooleanField(default=False)
    can_view_pronouns = models.BooleanField(default=False)
    can_view_location = models.BooleanField(default=False)
    can_view_university = models.BooleanField(default=False)
    can_view_website = models.BooleanField(default=False)
    can_view_bio = models.BooleanField(default=False)
    can_view_preferred_contact_way = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.username} - {self.context.name} - {self.requester_type.name}"

class IdentityRequest(models.Model):
    class Status(models.TextChoices):
        #possible states
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        DENIED = "denied", "Denied"
    #user that requests identity
    requester = models.ForeignKey(
        User,
        related_name="identity_requests_sent",
        on_delete=models.CASCADE,
    )
    #target useer (user being looked up)
    target_user = models.ForeignKey(
        User,
        related_name="identity_requests_received",
        on_delete=models.CASCADE,
    )
    #context of the lookup
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE,
    )
    #requester type (nullable)
    requester_type = models.ForeignKey(
        RequesterType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    #status of the request
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    #reason the requester can add for why they are searching this user's identity
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        #show in order
        ordering = ["-created_at"]
        # add a constraint to prevent duplicate requests
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "requester",
                    "target_user",
                    "context",
                ],
                name="unique_identity_request"
            )
        ]

    def __str__(self):
        return (
            f"{self.requester.username} -> "
            f"{self.target_user.username} "
            f"({self.context.name})"
        )