from apps.superadmin.tests.test_setup import TestSetUp
from apps.superadmin.models import Role,User

class TestViews(TestSetUp):

    def test_roles_creation(self):
        """This checks if roles are being created on creation
        """
        self.assertEqual(Role.objects.all().count(),3)

    def test_create_user(self):
        """This will test if an initial superuser can be created
        """
        self.assertTrue(self.super_user.role.name == "super_admin")