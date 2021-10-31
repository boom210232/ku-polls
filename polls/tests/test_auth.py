"""Test of authentication"""

import django.test
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        super().setUp()
        self.username = "fakeone"
        self.password = "nopassword"
        self.user1 = User.objects.create_user(username=self.username, password=self.password, email="getF@inw007.go.th")
        self.user1.first_name = "Stranger"
        self.user1.save()

    def test_login_view(self):
        """Test that user can login via login view"""
        login_url = reverse("login")
        # Can get to login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {"username": "fakeone", "password": "nopassword"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("polls:index"))

    def test_auth_require_to_vote(self):
        # where user id?
        # vote_url = reverse('polls:vote' , args=[self.question_id])

        pass



