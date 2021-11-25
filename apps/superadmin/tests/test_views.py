from apps.superadmin.tests.test_setup import TestSetUp
from apps.superadmin.models import *
from rest_framework import status

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

