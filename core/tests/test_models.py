from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        email= 'test@gmail.com'
        password= 'test1234'
        user=get_user_model().objects.create_user(email=email,password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        email= 'test@Gmail.com'
        password= 'test1234'
        user= get_user_model().objects.create_user(email=email,password=password)

        self.assertEqual(email.lower(),user.email)

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test1234')

    def test_super_user_created(self):

        user= get_user_model().objects.create_superuser('test@gmail.com', 'test1234')

        self.assertTrue(user.is_staff,True)
        self.assertTrue(user.is_superuser,True)