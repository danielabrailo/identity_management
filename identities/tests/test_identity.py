from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from identities.models import (
    Context,
    ContextProfile,
    Policy,
    RequesterType,
    IdentityRequest
)

class ContextProfileTests(APITestCase):
    #create test data
    def setUp(self):
        #create test user
        self.user = User.objects.create_user(
            username="john",
            password="testpassword123"
        )
        #get or create create "Professional" test context
        self.context, _ = Context.objects.get_or_create(
            name="Professional"
        )
        #make users authenticated
        self.client.force_authenticate(user=self.user)

    #test successful evaluation
    def test_successful_evaluation(self):
        #create requester
        requester = RequesterType.objects.create(
            name="HR"
        )
        #create profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        policy = Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_display_name=True,
            can_view_email=False
        )
        #create another user
        self.requester = User.objects.create_user(
            username="alice",
            password="password123"
        )
        #authenticate
        self.client.force_authenticate(self.requester)
        #create identity request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.user,
            context=self.context,
            requester_type=requester,
            status=IdentityRequest.Status.APPROVED,
        )
        #use django's rever to generate URL based on view name
        url = reverse("identity-evaluation")
        #call endpoint
        response = self.client.post(
            url,
            {
                "request_id": identity_request.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["display_name"], "John Doe")
        self.assertIsNone(response.data["email"])

    #test profile not found
    def test_profile_not_found(self):
        #create requester
        requester = RequesterType.objects.create(
            name="HR"
        )
        #create policy
        policy = Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_display_name=True,
            can_view_email=False
        )
        #create another user
        self.requester = User.objects.create_user(
            username="alice",
            password="password123"
        )
        #authenticate
        self.client.force_authenticate(self.requester)
        #create identity request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.user,
            context=self.context,
            requester_type=requester,
            status=IdentityRequest.Status.APPROVED,
        )
        #use django's rever to generate URL based on view name
        url = reverse("identity-evaluation")
        #call endpoint
        response = self.client.post(
            url,
           {
                "request_id": identity_request.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "No profile found")

    # #test policy not found
    def test_policy_not_found(self):
        #create requester
        requester_type = RequesterType.objects.create(
            name="HR"
        )
        #create profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create another user
        self.requester = User.objects.create_user(
            username="alice",
            password="password123"
        )
        #create identity request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.user,
            context=self.context,
            requester_type=requester_type,
            status=IdentityRequest.Status.APPROVED,
        )
        #authenticate
        self.client.force_authenticate(self.requester)
        #use django's rever to generate URL based on view name
        url = reverse("identity-evaluation")
        #call endpoint
        response = self.client.post(
            url,
            {
                "request_id": identity_request.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "No policy found")

    #test invalid requester type
    def test_invalid_requester_type(self):
        #create requester
        requester = RequesterType.objects.create(
            name="HR"
        )
        #create profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        policy = Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_display_name=True,
            can_view_email=False
        )
        #use django's rever to generate URL based on view name
        url = reverse("identity-evaluation")
        #call endpoint
        response = self.client.post(
            url,
            {
                "target_user_id": self.user.id,
                "context_id": self.context.id,
                "requester_type_id": "test"
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #test invalid context
    def test_invalid_context(self):
        #create requester
        requester = RequesterType.objects.create(
            name="HR"
        )
        #create profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        policy = Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_display_name=True,
            can_view_email=False
        )
        #use django's rever to generate URL based on view name
        url = reverse("identity-evaluation")
        #call endpoint
        response = self.client.post(
            url,
            {
                "target_user_id": self.user.id,
                "context_id": "test",
                "requester_type_id": requester.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
