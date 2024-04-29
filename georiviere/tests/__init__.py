from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mapentity.tests import MapEntityTest

from georiviere.main.models import DistanceToSource
from georiviere.river.models import Stream
from georiviere.tests.factories import UserAllPermsFactory

from geotrek.authent.tests.factories import StructureFactory


class CommonRiverTest(MapEntityTest):
    userfactory = UserAllPermsFactory

    # TODO: find a way to fix these tests
    def test_api_geojson_list_for_model(self):
        pass

    def test_api_geojson_detail_for_model(self):
        pass

    def test_structure_is_set(self):
        if not hasattr(self.model, 'structure'):
            return
        self.login()
        self.user.user_permissions.remove(Permission.objects.get(codename='can_bypass_structure'))

        response = self.client.post(self._get_add_url(), self.get_good_data())
        self.assertEqual(response.status_code, 302)
        obj = self.model.objects.last()
        self.assertEqual(obj.structure, self.user.profile.structure)

    def test_structure_is_not_changed_without_permission(self):
        if not hasattr(self.model, 'structure'):
            return
        self.login()
        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        self.user.user_permissions.remove(Permission.objects.get(codename='can_bypass_structure'))
        self.assertFalse(self.user.has_perm('authent.can_bypass_structure'))
        obj = self.modelfactory.create(structure=structure)
        result = self.client.post(obj.get_update_url(), self.get_good_data())
        self.assertEqual(result.status_code, 302)
        obj.refresh_from_db()
        self.assertEqual(obj.structure, structure)
        self.logout()

    def test_structure_is_changed_with_permission(self):
        if not self.model or 'structure' not in self.model._meta.get_fields():
            return
        self.login()
        self.assertTrue(self.user.has_perm('authent.can_bypass_structure'))
        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        obj = self.modelfactory.create(structure=structure)
        data = self.get_good_data()
        data['structure'] = self.user.profile.structure.pk
        result = self.client.post(obj.get_update_url(), data)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(self.model.objects.first().structure, self.user.profile.structure)
        self.logout()

    def test_set_structure_with_permission(self):
        if not hasattr(self.model, 'structure'):
            return
        self.login()
        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        data = self.get_good_data()
        data['structure'] = self.user.profile.structure.pk
        response = self.client.post(self._get_add_url(), data)
        self.assertEqual(response.status_code, 302)
        obj = self.model.objects.last()
        self.assertEqual(obj.structure, self.user.profile.structure)
        self.logout()

    def test_delete_not_same_structure_no_permission(self):
        if not hasattr(self.model, 'structure'):
            return
        self.login()

        self.user.user_permissions.remove(Permission.objects.get(codename='can_bypass_structure'))
        self.user.save()

        self.assertFalse(self.user.has_perm('authent.can_bypass_structure'))

        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        obj = self.modelfactory(structure=structure)
        response = self.client.get(obj.get_delete_url())
        self.assertRedirects(response, obj.get_detail_url())

    def test_update_not_same_structure_no_permission(self):
        if not hasattr(self.model, 'structure'):
            return
        self.login()

        self.user.user_permissions.remove(Permission.objects.get(codename='can_bypass_structure'))
        self.user.save()

        self.assertFalse(self.user.has_perm('authent.can_bypass_structure'))

        structure = StructureFactory()
        self.assertNotEqual(structure, self.user.profile.structure)
        obj = self.modelfactory(structure=structure)
        response = self.client.get(obj.get_update_url())
        self.assertRedirects(response, obj.get_detail_url())

    def test_distance_to_source_is_available(self):
        if self.model is None or not hasattr(self.modelfactory, 'with_stream'):
            return  # Abstract test should not run
        self.login()
        obj = self.modelfactory.create(with_stream=True)
        response = self.client.get(obj.get_detail_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            f'''<a data-pk="{Stream.objects.first().pk}" href="/stream/{Stream.objects.first().pk}/"''')
        distance = DistanceToSource.objects.get(
            object_id=obj.pk,
            content_type=ContentType.objects.get_for_model(obj)
        ).distance
        self.assertContains(response, f'''({round(distance, 1) if distance else 0}&nbsp;m)''')
