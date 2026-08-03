from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from identities.models import (
    Context,
    ContextProfile,
    RequesterType,
    IdentityRequest,
    Policy
)

class IdentityRequestAPITest(APITestCase):
    def setUp(self):
        #create requester user
        self.requester = User.objects.create_user(
            username="alice",
            password="password123"
        )
        #create target user
        self.target = User.objects.create_user(
            username="john",
            password="password123"
        )
        #create context
        self.context, _ = Context.objects.get_or_create(
            name="Professional"
        )
        #target's profile
        self.profile = ContextProfile.objects.create(
            account=self.target,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #authenticate requester
        self.client.force_authenticate(user=self.requester)
        #url
        self.url = reverse("identity-request-list-create")

    def test_create_identity_request(self):
        #call endpoint
        response = self.client.post(
            self.url,
            {
                "target_user": self.target.id,
                "context": self.context.id,
                "reason": "Employment verification."
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IdentityRequest.objects.count(), 1)
        #get request from db
        identity_request = IdentityRequest.objects.first()
        #verify data
        self.assertEqual(identity_request.requester, self.requester)
        self.assertEqual(identity_request.target_user, self.target)
        self.assertEqual(identity_request.context, self.context)
        self.assertEqual(identity_request.status, IdentityRequest.Status.PENDING)
        self.assertIsNone(identity_request.requester_type)          
        
    def test_list_requests(self):
        #switch users
        self.client.force_authenticate(user=self.target)
        #create identity request
        IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
        )
        #create user
        other = User.objects.create_user(
            username="bob",
            password="password123"
        )
        #create another idenity requester from the other user
        IdentityRequest.objects.create(
            requester=other,
            target_user=self.target,
            context=self.context,
        )
        #call endpoint
        response = self.client.get(self.url)
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_permissions(self):
        #create another target
        other_target = User.objects.create_user(username="charlie", password="password123")
        #create another profile
        ContextProfile.objects.create(account=other_target, context=self.context)
        #create request for John user
        IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
        )
        #create request for other target
        IdentityRequest.objects.create(
            requester=self.requester,
            target_user=other_target,
            context=self.context,
        )
        #authenticate John
        self.client.force_authenticate(self.target)
        #call endpoint
        response = self.client.get(self.url)
        #assertions
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["target_username"], "john")

    def test_user_cannot_create_duplicate_pending_request(self):
        #create identity request
        IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            status=IdentityRequest.Status.PENDING,
        )
        #call endpoint
        response = self.client.post(
            self.url,
            {
                "target_user": self.target.id,
                "context": self.context.id,
                "reason": "Another request"
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
    def test_user_cannot_request_their_own_identity(self):
        #call endpoint
        response = self.client.post(
            self.url,
            {
                "target_user": self.requester.id,
                "context": self.context.id,
                "reason": "Trying myself"
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
        
    def test_target_user_can_approve_request(self):
        #create requeter type
        requester_type = RequesterType.objects.create(
            name="Employer"
        )
        #create identity request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            status=IdentityRequest.Status.PENDING,
        )
        #authenticate target user
        self.client.force_authenticate(
            user=self.target
        )
        #create url
        url = reverse("identity-request-approve", args=[identity_request.id])
        #call endpoint
        response = self.client.patch(
            url,
            {
                "requester_type": requester_type.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #refresh identity request from database
        identity_request.refresh_from_db()
        #assertions
        self.assertEqual(identity_request.status, IdentityRequest.Status.APPROVED)
        self.assertEqual(identity_request.requester_type, requester_type)
        self.assertIsNotNone(identity_request.decided_at)

    def test_other_user_cannot_approve_request(self):
        #create anpother user
        other_user = User.objects.create_user(username="bob",  password="password123")
        #create identity request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context
        )
        #authenticate Bob
        self.client.force_authenticate(
            user=other_user
        )
        #create requester type
        requester_type = RequesterType.objects.create(name="Employer")
        #create url
        url = reverse("identity-request-approve", args=[identity_request.id])
        #call endpoint
        response = self.client.patch(
            url,
            {
                "requester_type": requester_type.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_target_user_can_deny_request(self):
        #create identity request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            status=IdentityRequest.Status.PENDING,
        )
        #authenticate user
        self.client.force_authenticate(user=self.target)
        #create url
        url = reverse("identity-request-deny", args=[identity_request.id])
        #call endpoint
        response = self.client.patch(url)
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #refresh from database
        identity_request.refresh_from_db()
        #assertions
        self.assertEqual(identity_request.status, IdentityRequest.Status.DENIED)    
        self.assertIsNotNone(identity_request.decided_at)
        self.assertIsNone(identity_request.requester_type)

    def test_target_user_cannot_approve_already_approved_request(self):
        #create requeter type
        requester_type = RequesterType.objects.create(
            name="Employer"
        )
        #create identity request already approved
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            status=IdentityRequest.Status.APPROVED,
        )
        #authenticate target user
        self.client.force_authenticate(user=self.target)
        #create url
        url = reverse("identity-request-approve", args=[identity_request.id])
        #call endpoint
        response = self.client.patch(
            url,
            {
                "requester_type": requester_type.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This request has already been decided.")
    
    def test_target_user_cannot_deny_already_denied_request(self):
        #create requeter type
        requester_type = RequesterType.objects.create(
            name="Employer"
        )
        #create identity request already approved
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            status=IdentityRequest.Status.DENIED,
        )
        #authenticate target user
        self.client.force_authenticate(user=self.target)
        #create url
        url = reverse("identity-request-deny", args=[identity_request.id])
        #call endpoint
        response = self.client.patch(
            url,
            {
                "requester_type": requester_type.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This request has already been decided.")

    def test_pending_request_cannot_evaluate_identity(self):
        #create requester type
        requester_type = RequesterType.objects.create(name="Employer")
        #create John's profile
        ContextProfile.objects.get_or_create(
            account=self.target,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        Policy.objects.create(
            account=self.target,
            context=self.context,
            requester_type=requester_type,
            can_view_display_name=True,
        )
        #create pending request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            requester_type=requester_type,
            status=IdentityRequest.Status.PENDING,
        )
        #authenticate as requester
        self.client.force_authenticate(user=self.requester)
        #call evaluation
        url = reverse("identity-evaluation")
        response = self.client.post(
            url,
            {
                "request_id": identity_request.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_approved_request_evaluates_identity(self):
        #create requester type
        requester_type = RequesterType.objects.create(name="Employer")
        #create John's profile
        ContextProfile.objects.get_or_create(
            account=self.target,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        Policy.objects.create(
            account=self.target,
            context=self.context,
            requester_type=requester_type,
            can_view_display_name=True,
        )
        #create approved reuqest
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            requester_type=requester_type,
            status=IdentityRequest.Status.APPROVED,
        )
        #authenticate as requester
        self.client.force_authenticate(user=self.requester)
        #call endpoint
        url = reverse("identity-evaluation")
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

    def test__denied_request_cannot_evaluate_identity(self):
        #create requester type
        requester_type = RequesterType.objects.create(name="Employer")
        #create John's profile
        ContextProfile.objects.get_or_create(
            account=self.target,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        Policy.objects.create(
            account=self.target,
            context=self.context,
            requester_type=requester_type,
            can_view_display_name=True,
        )
        #create denied request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            requester_type=requester_type,
            status=IdentityRequest.Status.DENIED,
        )
        #authenticate as requester
        self.client.force_authenticate(user=self.requester)
        #call evaluation
        url = reverse("identity-evaluation")
        response = self.client.post(
            url,
            {
                "request_id": identity_request.id
            },
            format="json"
        )
        #assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_another_user_cannot_use_someone_else_request(self):
        #create another user
        other_user = User.objects.create_user(
            username="bob",
            password="password123"
        )
        #create requester type
        requester_type = RequesterType.objects.create(name="Employer")
        #create John progile
        ContextProfile.objects.get_or_create(
            account=self.target,
            context=self.context,
            display_name="John Doe",
            email="john@test.com"
        )
        #create policy
        Policy.objects.create(
            account=self.target,
            context=self.context,
            requester_type=requester_type,
            can_view_display_name=True,
            can_view_email=False,
        )
        #create approved request
        identity_request = IdentityRequest.objects.create(
            requester=self.requester,
            target_user=self.target,
            context=self.context,
            requester_type=requester_type,
            status=IdentityRequest.Status.APPROVED,
        )
        #authenticate Bob
        self.client.force_authenticate(user=other_user)
        #call endpoint
        url = reverse("identity-evaluation")
        response = self.client.post(
            url,
            {
                "request_id": identity_request.id
            },
            format="json"
        )
        #assertion
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    