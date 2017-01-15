#!usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import modify_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from main.models import User 

SELF_USERNAME = 'self'
NORMAL_USER_USERNAME = 'normal_user'
ADMIN_USERNAME = 'admin'
NEW_USER_USERNAME = 'new_user'
ORIGINAL_PASSWORD = 'foo'
NEW_PASSWORD = 'bar'

@modify_settings(MIDDLEWARE_CLASSES = {
    'remove': 'silk.middleware.SilkyMiddleware',
})
class UserPermissionTests(APITestCase):
    
    def setUp(self):
        """
        Run before every test case
        Create normal user, another user, and admin
        """
        User.objects.create_user(
                username=SELF_USERNAME, 
                password=ORIGINAL_PASSWORD)
        User.objects.create_user(
                username=NORMAL_USER_USERNAME, 
                password=ORIGINAL_PASSWORD)
        User.objects.create_superuser(
                username=ADMIN_USERNAME, 
                password=ORIGINAL_PASSWORD)
        self.client = APIClient()

    def tearDown(self):
        """
        Run after every test case
        Do something not related with database (e.g. Create or delete local file)
        """
        pass

    def test_list_users(self):
        """
        Test list users
        Permission : admin only
        """
        # GET /users/
        url = reverse('user-list')
        
        # 1. No authentication
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # 2. Authentication with normal user
        user = User.objects.get(username=NORMAL_USER_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.client.force_authenticate(user=None)
        
        # 3. Authentication with admin
        user = User.objects.get(username=ADMIN_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)

    def test_create_user(self):
        """
        Test create user
        Perminssion : anyone
        """
        # POST /users/
        url = reverse('user-list')
        
        # 1. No authentication (Required fields are not given)
        response = self.client.post(
                url, 
                {
                    'username': NEW_USER_USERNAME, 
                }, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # 2. No authentication
        response = self.client.post(
                url, 
                {
                    'username': NEW_USER_USERNAME, 
                    'password': ORIGINAL_PASSWORD
                }, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], NEW_USER_USERNAME)
        self.client.force_authenticate(user=None)

    def test_retrieve_user(self):
        """
        Test retrieve user
        Permission : self or admin
        """
        # GET /users/{pk}/
        url = '/users/' + str(User.objects.get(username=SELF_USERNAME).id) + '/'
        
        # 1. No authentication
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # 2. Authentication with another user
        user = User.objects.get(username=NORMAL_USER_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.client.force_authenticate(user=None)
        
        # 3. Authentication with own self
        user = User.objects.get(username=SELF_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], SELF_USERNAME)
        self.client.force_authenticate(user=None)
        
        # 4. Authentication with admin
        user = User.objects.get(username=ADMIN_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], SELF_USERNAME)
        self.client.force_authenticate(user=None)

    def test_update_user(self):
        """
        Test update user
        Permission : self or admin
        """
        # PUT /users/{pk}/
        url = '/users/' + str(User.objects.get(username=SELF_USERNAME).id) + '/'
        
        # 1. No authentication
        response = self.client.put(
                url, 
                {
                    'username': SELF_USERNAME + '1',
                    'original_password': ORIGINAL_PASSWORD,
                    'password': NEW_PASSWORD
                }, 
                format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # 2. Authentication with another user
        user = User.objects.get(username=NORMAL_USER_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.put(
                url, 
                {
                    'username': SELF_USERNAME + '2', 
                    'original_password': ORIGINAL_PASSWORD,
                    'password': NEW_PASSWORD
                }, 
                format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.client.force_authenticate(user=None)
        
        # 3. Authentication with own self (Required fields are not given)
        user = User.objects.get(username=SELF_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.put(
                url, 
                {}, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.force_authenticate(user=None)
        
        # 4. Authentication with own self
        user = User.objects.get(username=SELF_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.put(
                url, 
                {
                    'username': SELF_USERNAME + '3', 
                    'original_password': ORIGINAL_PASSWORD,
                    'password': NEW_PASSWORD
                }, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], SELF_USERNAME + '3')
        self.client.force_authenticate(user=None)
        
        # 5. Authentication with admin
        user = User.objects.get(username=ADMIN_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.put(
                url, 
                {
                    'username': SELF_USERNAME + '4', 
                    'original_password': NEW_PASSWORD,
                    'password': ORIGINAL_PASSWORD
                }, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], SELF_USERNAME + '4')
        self.client.force_authenticate(user=None)

    def test_partial_update_user(self):
        """
        Test partial update user
        Permission : self or admin
        """
        # PATCH /users/{pk}/
        url = '/users/' + str(User.objects.get(username=SELF_USERNAME).id) + '/'
        
        # 1. No authentication
        response = self.client.patch(
                url, 
                {
                    'email': 'username1@domain.com', 
                }, 
                format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # 2. Authentication with another user
        user = User.objects.get(username=NORMAL_USER_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.patch(
                url, 
                {
                    'email': 'username2@domain.com', 
                }, 
                format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.client.force_authenticate(user=None)
        
        # 3. Authentication with own self
        user = User.objects.get(username=SELF_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.patch(
                url, 
                {
                    'email': 'username3@domain.com', 
                }, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'username3@domain.com')
        self.client.force_authenticate(user=None)
        
        # 4. Authentication with admin
        user = User.objects.get(username=ADMIN_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.patch(
                url, 
                {
                    'email': 'username4@domain.com', 
                }, 
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'username4@domain.com')
        self.client.force_authenticate(user=None)

    def test_destroy_user(self):
        """
        Test destroy user
        Permission : admin only
        """
        # DELETE /users/{pk}/
        url = '/users/' + str(User.objects.get(username=SELF_USERNAME).id) + '/'
        
        # 1. No authentication
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # 2. Authentication with own self
        user = User.objects.get(username=SELF_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.client.force_authenticate(user=None)
        
        # 3. Authentication with admin
        user = User.objects.get(username=ADMIN_USERNAME)
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.force_authenticate(user=None)
