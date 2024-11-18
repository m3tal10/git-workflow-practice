from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create_user')
TOKEN_URL = reverse('user:token')
ME_URL= reverse('user:me')

def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)

class PublicUserApiTests(TestCase):
    """Tests the user API public. Needs no authentication."""
    def setUp(self) -> None:
        self.client= APIClient()
        pass

    def test_create_valid_user_success(self):
        """Test create user using valid payload successful."""
        payload={
            'email':'test@gmail.com',
            'password':'pass1234',
            'name':'test'
        }
        res = self.client.post(CREATE_USER_URL,data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user= get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
    
    def test_create_duplicate_user_fail(self):
        """Test check creating duplicate user throws error"""
        payload={
            'email':'test@gmail.com',
            'password':'pass1234',
            'name':'test'
        }
        create_user(**payload)
        res= self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Test check password too short throws error"""
        payload={
            'email':'test@gmail.com',
            'password':'pass',
            'name':'test'
        }
        res= self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists= get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_user(self):
        """Test check creates and sends user token on login"""
        payload={
            'email':'test@gmail.com',
            'password':'pass1234',
        }
        user = create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Test check if logging in with invalid credentials throws error"""
        payload={
            'email':'test@gmail.com',
            'password':'pass1234',
        }
        user=create_user(**payload)
        res= self.client.post(TOKEN_URL,data={**payload,'password':'wrong'})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """Test token not created if no user found"""
        payload={
            'email':'test@gmail.com',
            'password':'pass1234',
        }
        res= self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class PrivateUserApiTest(TestCase):
    """Tests the user API private. Authentication needed."""
    def setUp(self) -> None:
        self.user= create_user(
            email='test@gmail.com',
            password='pass1234',
            name='test'
        )
        self.client= APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res= self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
