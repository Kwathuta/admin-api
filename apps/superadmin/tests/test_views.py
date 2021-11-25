from django.http import response
from apps.superadmin.tests.test_setup import TestSetUp
from apps.superadmin.models import *
from rest_framework import status
from django.core import mail

from apps.superadmin.tokens import *

class TestViews(TestSetUp):
    """Tests for superadmin module

    Args:
        TestSetUp ([type]): [description]
    """

    def test_roles_creation(self):
        """This test if all the roles are created on app initialization
        """
        self.assertTrue(Role.objects.all().count(),4)

    def test_company_creation(self):
        """This tests if a company can be created
        """
        res = self.client.post(self.create_company_url,self.company_details)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        my_company = Company.objects.get(name = self.company_details['company_name'])
        self.assertTrue(my_company is not None)

    def test_login_without_activating_token(self):
        """This will test a user loggin in without activating their account
        """
        self.client.post(self.create_company_url,self.company_details)

        res = self.client.post(self.login_url,self.first_super_admin)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        user = Employee.objects.get(is_active=False)
        self.assertTrue(user is not None)

    def test_activate_account(self):
        """This will test the activate account functionality
        """
        self.client.post(self.create_company_url,self.company_details)
        self.assertEqual(len(mail.outbox), 1)
        response = self.client.get(mail.outbox[0].body)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_user_while_unauthorised(self):
        """This tests if a user can create an employee without credentials
        """
        res = self.client.post(self.login_url,self.normal_user_data)
        self.assertEqual(res.status_code, 400)

    def authenticate(self,user_data):
        response = self.client.post(self.login_url,user_data)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {response.data['token']}")

    def test_create_user_while_authorised(self):
        """This will tes if a user can be created
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        res = self.client.post(self.create_user_url,self.normal_user_data)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_change_role(self):
        """This will test if a user's role can be changed
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        self.client.post(self.create_user_url,self.normal_user_data)

        user = Employee.objects.get(email = self.normal_user_data['email'])
        role = Role.objects.get(name="human_resources")

        role_changer = {
            'user':user.pk,
            'role':role.pk
        }

        response = self.client.post(self.change_role_url,role_changer)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        user_now = Employee.objects.get(email = self.normal_user_data['email'])
        self.assertEqual(user_now.role,role)