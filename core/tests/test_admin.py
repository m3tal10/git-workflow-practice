from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client= Client()
        self.admin_user= get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='pass1234'
        )
        self.client.force_login(self.admin_user)
        self.user= get_user_model().objects.create_user(
            email='user@gmail.com',
            password='pass1234',
            name='Test User'
        )
    def test_for_user_listed(self):
        """Test if the user is listed in the admin dashboard."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_edit_page_loads(self):
        """Test that user edit page loads"""
        url= reverse('admin:core_user_change', args=[self.user.id])
        res= self.client.get(url)

        self.assertEqual(res.status_code,200)
    def test_user_add_page(self):
        """Test that user add page loads"""
        url= reverse('admin:core_user_add')
        res= self.client.get(url)

        self.assertEqual(res.status_code,200)