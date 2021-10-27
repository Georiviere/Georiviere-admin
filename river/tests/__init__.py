from django.contrib.auth.models import Permission

from geotrek.authent.factories import StructureFactory

from georiviere.tests import CommonRiverTest


class TopologyTestCase(CommonRiverTest):
    def test_crud_status(self):
        if self.model is None:
            return  # Abstract test should not run

        self.login()

        obj = self.modelfactory()

        response = self.client.get(obj.get_list_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(obj.get_detail_url().replace(str(obj.pk), '1234567890'))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(obj.get_detail_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 200)
        self._post_update_form(obj)
        self._check_update_geom_permission(response)

        url = obj.get_detail_url()
        obj.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # Test to update without login
        self.logout()

        obj = self.modelfactory()

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        if self.model is None:
            return  # Abstract test should not run

        self.login()

        obj = self.modelfactory()

        response = self.client.get(obj.get_delete_url())
        self.assertEqual(response.status_code, 403)

    def test_create(self):
        if self.model is None:
            return  # Abstract test should not run

        response = self.client.get(self.model.get_add_url())
        self.assertEqual(response.status_code, 403)

    def test_structure_is_set(self):
        pass

    def test_delete_not_same_structure_no_permission(self):
        pass

    def test_set_structure_with_permission(self):
        pass

    def test_update_not_same_structure_no_permission(self):
        if self.model is None:
            return  # Abstract test should not run
        self.login()

        self.user.user_permissions.remove(Permission.objects.get(codename='can_bypass_structure'))
        self.user.save()

        self.assertFalse(self.user.has_perm('authent.can_bypass_structure'))

        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        obj = self.modelfactory()
        obj.topology.stream.structure = structure
        obj.topology.stream.save()
        obj.refresh_from_db()
        response = self.client.get(obj.get_update_url())
        self.assertRedirects(response, obj.get_detail_url())

    def test_update_not_same_structure_with_permission(self):
        if self.model is None:
            return  # Abstract test should not run
        self.login()

        self.assertTrue(self.user.has_perm('authent.can_bypass_structure'))

        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        obj = self.modelfactory()
        obj.topology.stream.structure = structure
        obj.topology.stream.save()
        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 200)
