from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from identities.models import (
    Context,
    ContextProfile
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
        #make user authenticated
        self.client.force_authenticate(user=self.user)

    #test: create a context profile
    def test_create_context_profile(self):
        #context data
        data = {
            "context": self.context.id,
            "display_name": "John Doe",
            "email": "johndoe@test.com",
            "job_title": "Developer"
        }
        #use django's rever to generate URL based on view name
        url = reverse("context-profile-list-create")
        #call endpoint
        response = self.client.post(
            url,
            data,
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContextProfile.objects.count(), 1)

    #test: retrieve user's profiles
    def test_retrieve_all_context_profiles(self):
        #create a profile
        ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe"
        )
        #generate url
        url = reverse("context-profile-list-create")
        #call endpoint
        response = self.client.get(url)
        #assertions
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["display_name"],
            "John Doe"
        )
