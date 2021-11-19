from apps.superadmin.tests.test_setup import TestSetUp
from apps.superadmin.models import Role,User
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

    def authenticate(self):
        response = self.client.post(self.login_url,self.super_user_data)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {response.data['token']}")

    def test_create_user_while_un_authorised(self):
        """This will tes if a user can be created by an unauthorised user
        """
        response = self.client.post(self.create_user_url,self.normal_user_data)

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_create_user_while_authorised(self):
        """This will tes if a user can be created
        """
        self.authenticate()
        response = self.client.post(self.create_user_url,self.normal_user_data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_change_role(self):
        """This will test if a user's role can be changed
        """
        self.authenticate()
        self.client.post(self.create_user_url,self.normal_user_data)

        user = User.objects.get(email = self.normal_user_data['email'])
        role = Role.objects.get(name="human_resources")

        role_changer = {
            'user':user.pk,
            'role':role.pk
        }

        response = self.client.post(self.change_role,role_changer)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        user_now = User.objects.get(email = self.normal_user_data['email'])
        self.assertEqual(user_now.role,role)

    def test_change_role_for_self(self):
        """This will test if a user's role can be changed by the same user
        """
        self.authenticate()

        user = User.objects.get(email = self.super_user_data['username'])
        role = Role.objects.get(name="human_resources")

        role_changer = {
            'user':user.pk,
            'role':role.pk
        }

        response = self.client.post(self.change_role,role_changer)

        self.assertTrue(response.status_code != status.HTTP_403_FORBIDDEN)

    