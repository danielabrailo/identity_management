from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from identities.models import (
    Context,
    ContextProfile,
    Policy,
    RequesterType
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
        #use django's rever to generate URL based on view name
        url = reverse("identity-evaluation")
        #call endpoint
        response = self.client.post(
            url,
            {
                "target_user_id": self.user.id,
                "context_id": self.context.id,
                "requester_type_id": requester.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["display_name"], "John Doe")
        self.assertIsNone(response.data["email"])