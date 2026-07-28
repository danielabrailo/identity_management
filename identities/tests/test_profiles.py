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

    #test: create an invalid context profile
    def test_create_invalid_context_profile(self):
        #context data
        data = {
            "context": 11,
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContextProfile.objects.count(), 0)

    #test: create an invalid email in context profile
    def test_create_invalid_email(self):
        #context data
        data = {
            "context": self.context.id,
            "display_name": "John Doe",
            "email": "not-a-valid-email",
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContextProfile.objects.count(), 0)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["display_name"], "John Doe")
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

    #test: cannot update another user's profile
    def test_other_user_update_context_profile(self):
        #context profiles from different users
        profile1 = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            job_title="Developer"
        )   
        profile2 = ContextProfile.objects.create(
            account=self.user2,
            context=self.context,
            display_name="Marie",
            job_title="Developer"
        )        
        #generate url
        url = reverse(
            "context-profile-detail",
            kwargs={"pk": profile2.pk}
        )
        #update profile
        response = self.client.patch(url, {"job_title":"Software Engineer"},
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

    #test: cannot delete another user's profile
    def test_delete_another_user_context_profile(self):
        #context profiles from different users
        profile1 = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            job_title="Developer"
        )   
        profile2 = ContextProfile.objects.create(
            account=self.user2,
            context=self.context,
            display_name="Marie",
            job_title="Developer"
        )              
        #generate url
        url = reverse(
            "context-profile-detail",
            kwargs={"pk": profile2.pk}
        )
        #delete profile
        response = self.client.delete(url, {"job_title":"Software Engineer"},
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #test: unauthenticated users
    def test_update_unauthenticated_context_profile(self):
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

    #test: create a policy
    def test_create_policy(self):
        #create requester type
        requester = RequesterType.objects.create(name="HR")
        #create a policy
        data = {
            "context": self.context.id,
            "requester_type": requester.id,
            "can_view_display_name": True,
            "can_view_email": False
        }
        #use django's rever to generate URL based on view name
        url = reverse("policy-list-create")
        #call endpoint
        response = self.client.post(
            url,
            data,
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.count(), 1)

    #test: cannot access another user's policy
    def test_create_different_users_policy(self):
        #create requester type
        requester = RequesterType.objects.create(name="HR")
        #create a second context
        context2 = Context.objects.create(name="Academic")
        #create policies for different users
        Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_email=True
        )
        Policy.objects.create(
            account=self.user2,
            context=context2,
            requester_type=requester,
            can_view_email=False
        )
        #use django's rever to generate URL based on view name
        url = reverse("policy-list-create")
        #call endpoint
        response = self.client.get(url)
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["context_name"], "Professional")
        self.assertNotEqual(response.data[0]["context_name"], "Academic")

    #test: cannot create a duplicate policy
    def test_duplicate_policy(self):
        #create requester type
        requester = RequesterType.objects.create(name="HR")
        #create a policy
        data = {
            "context": self.context.id,
            "requester_type": requester.id,
            "can_view_display_name": True,
            "can_view_email": False
        }
        data2 = {
            "context": self.context.id,
            "requester_type": requester.id,
            "can_view_display_name": True,
            "can_view_email": False
        }
        #use django's rever to generate URL based on view name
        url = reverse("policy-list-create")
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
        self.assertEqual(Policy.objects.count(), 1)

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

    #test: policy evaluator when everything is visible
    def test_policy_evaluator_everything(self):
        #create a profile
        profile = ContextProfile.objects.create(
            account=self.user,
            context=self.context,
            display_name="John Doe",
            email="test@test.com",
            phone="123456",
            job_title="Developer",
            linkedin="https://linkedin.com/test",
            nickname="Johnny",
            social_media="@johnny",
            organization="Best Org",
        )
        #create requester type
        requester = RequesterType.objects.create(name="HR")
        #create a policy
        policy = Policy.objects.create(
            account=self.user,
            context=self.context,
            requester_type=requester,
            can_view_display_name=True,
            can_view_email=True,
            can_view_phone=True,
            can_view_job_title=True,
            can_view_linkedin=True,
            can_view_social_media=True,
            can_view_nickname=True,
            can_view_organization=True
        )
        #call policy evaluator
        result = PolicyEvaluator.evaluate(profile, policy)
        #assertions
        self.assertEqual(result["display_name"],"John Doe")
        self.assertEqual(result["email"], "test@test.com")
        self.assertEqual(result["phone"], "123456")
        self.assertEqual(result["job_title"], "Developer")
        self.assertEqual(result["linkedin"], "https://linkedin.com/test")
        self.assertEqual(result["nickname"], "Johnny")
        self.assertEqual(result["social_media"], "@johnny")
        self.assertEqual(result["organization"], "Best Org")

    #test: policy evaluator when everything is hidden
    def test_policy_evaluator_everything_hidden(self):
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
            can_view_display_name=False,
            can_view_email=False,
            can_view_phone=False,
            can_view_job_title=False,
            can_view_linkedin=False,
            can_view_social_media=False,
            can_view_nickname=False,
            can_view_organization=False
        )
        #call policy evaluator
        result = PolicyEvaluator.evaluate(profile, policy)
        #assertions
        self.assertIsNone(result["display_name"])
        self.assertIsNone(result["email"])
        self.assertIsNone(result["phone"])
        self.assertIsNone(result["job_title"])
        self.assertIsNone(result["linkedin"])
        self.assertIsNone(result["social_media"])
        self.assertIsNone(result["nickname"])
        self.assertIsNone(result["organization"])
