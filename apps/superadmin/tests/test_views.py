from apps.superadmin.tests.test_setup import TestSetUp
from apps.superadmin.models import Role
from rest_framework import status

class TestViews(TestSetUp):

    def test_roles_creation(self):
        """This checks if roles are being created on creation
        """
        self.assertEqual(Role.objects.all().count(),3)

    def test_create_super_user(self):
        """This will test if an initial superuser can be created
        """
        self.assertTrue(self.super_user.role.name == "super_admin")

    def test_user_login_with_invalid_credentials(self):
        """This will test if a user can login with wrong credentials
        """
        res = self.client.post(self.login_url,self.normal_user_data)
        self.assertEqual(res.status_code, 400)

    def test_user_login_with_correct_credentials(self):
        """This will test that if a user can login with the correct credentials
        """
        res = self.client.post(self.login_url,self.super_user_data)
        from rest_framework.authtoken.models import Token
        token = Token.objects.get(user_id = self.super_user.pk)
        self.assertEqual(token.key,res.data['token'])
        self.assertEqual(res.status_code,status.HTTP_200_OK)