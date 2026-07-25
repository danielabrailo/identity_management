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
from identities.services.policy_evaluator import PolicyEvaluator

class ContextProfileTests(APITestCase):
    #create test data
    def setUp(self):
        #create test users
        self.user = User.objects.create_user(
            username="john",
            password="testpassword123"
        )
        self.user2 = User.objects.create_user(
            username="marie",
            password="testpassword123"
        )
        #get or create create "Professional" test context
        self.context, _ = Context.objects.get_or_create(
            name="Professional"
        )
        #make users authenticated
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

    #test: retrieve all context profiles
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

    #test: retrieve all context profiles from authenticated user
    def test_retrieve_authenticated_user_context_profiles(self):
        #create profiles from different users
        ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe"
        )
        ContextProfile.objects.create(
            account=self.user2,
            context=self.context,
            display_name="Marie"
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
        #assert that Marie is not among the response
        display_names = [profile["display_name"] for profile in response.data]
        self.assertNotIn("Marie", display_names)

    #test: retrieve user's single profile
    def test_retrieve_user_context_profile(self):
        #create a profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe"
        )
        #generate url
        url = reverse("context-profile-detail", kwargs={"pk": profile.pk})
        #call endpoint
        response = self.client.get(url)
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["display_name"],
            "John Doe"
        )

    #test: update a profile
    def test_update_context_profile(self):
        #context data
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            job_title="Developer"
        )        
        #generate url
        url = reverse(
            "context-profile-detail",
            kwargs={"pk": profile.pk}
        )
        #update profile
        response = self.client.patch(url, {"job_title":"Software Engineer"},
            format="json"
        )
        #reload db
        profile.refresh_from_db()
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.job_title, "Software Engineer")

    #test: delete a profile
    def test_delete_context_profile(self):
        #context data
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            job_title="Developer"
        )        
        #generate url
        url = reverse(
            "context-profile-detail",
            kwargs={"pk": profile.pk}
        )
        #update profile
        response = self.client.delete(url, {"job_title":"Software Engineer"},
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContextProfile.objects.count(),0)

    #test: unauthenticated users
    def test_update_context_profile(self):
        #remove authentication 
        self.client.force_authenticate(user=None)
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #test: confirm cannot create duplocate context profile
    def test_create_duplicated_context_profile(self):
        #context data
        data = {
            "context": self.context.id,
            "display_name": "John Doe",
            "email": "johndoe@test.com",
            "job_title": "Developer"
        }
        data2 = {
            "context": self.context.id,
            "display_name": "John Doe2",
            "email": "johndoe@test.com",
            "job_title": "Developer2"
        }
        #use django's rever to generate URL based on view name
        url = reverse("context-profile-list-create")
        #call endpoint
        response1 = self.client.post(
            url,
            data,
            format="json"
        )
        response2 = self.client.post(
            url,
            data2,
            format="json"
        )
        #assertions
        self.assertEqual(response2.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContextProfile.objects.count(), 1)

    #test: policy evaluator
    def test_policy_evaluator(self):
        #create a profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            email="test@test.com"
        )
        #create requester type
        requester = RequesterType.objects.create(name="HR")
        #create a policy
        policy = Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_display_name=True,
            can_view_email=False
        )
        #call policy evaluator
        result = PolicyEvaluator.evaluate(profile, policy)
        #assertions
        self.assertEqual(result["display_name"],"John Doe")
        self.assertIsNone(result["email"])
        self.assertIsNone(result["phone"])
        self.assertIsNone(result["job_title"])
        self.assertIsNone(result["linkedin"])
        self.assertIsNone(result["social_media"])
