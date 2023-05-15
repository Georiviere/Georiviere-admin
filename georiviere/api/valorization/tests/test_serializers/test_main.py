from django.test import TestCase
from django.test.client import RequestFactory
from unittest import mock
from geotrek.common.utils.testdata import get_dummy_uploaded_file, get_dummy_uploaded_image

from georiviere.api.valorization.serializers.main import AttachmentSerializer
from georiviere.main.tests.factories import AttachmentFactory
from georiviere.valorization.tests.factories import POIFactory


class AttachmentSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poi = POIFactory.create()
        cls.image = get_dummy_uploaded_image()
        cls.file = get_dummy_uploaded_file()
        cls.attachment_image = AttachmentFactory.create(content_object=cls.poi,
                                                        attachment_file=cls.image)
        cls.attachment_link = AttachmentFactory.create(content_object=cls.poi,
                                                       attachment_file='',
                                                       attachment_link='https://georiviere.fr/assets/img/logo.svg')
        cls.attachment_file = AttachmentFactory.create(content_object=cls.poi,
                                                       attachment_file=cls.file)
        cls.attachment_video = AttachmentFactory.create(content_object=cls.poi,
                                                        attachment_file='',
                                                        attachment_video='https://www.youtube.com/embed/Jm3anSjly0Y?wmode=opaque')
        cls.attachment_empty = AttachmentFactory.create(content_object=cls.poi,
                                                        attachment_file='')
        cls.request = RequestFactory().get('/')
        cls.serializer_attachment = AttachmentSerializer

    def test_attachment_image_content(self):
        data = self.serializer_attachment(instance=self.attachment_image,
                                          context={'request': self.request}).data
        self.assertSetEqual(set(data.keys()), {'url', 'legend', 'type', 'author', 'filetype', 'title', 'thumbnail'})
        self.assertEqual(data['type'], 'image')

    def test_attachment_link_content(self):
        data = self.serializer_attachment(instance=self.attachment_link,
                                          context={'request': self.request}).data
        self.assertSetEqual(set(data.keys()), {'url', 'legend', 'type', 'author', 'filetype', 'title', 'thumbnail'})
        self.assertEqual(data['type'], 'image')
        self.assertEqual(data['url'], 'https://georiviere.fr/assets/img/logo.svg')

    def test_attachment_file_content(self):
        data = self.serializer_attachment(instance=self.attachment_file,
                                          context={'request': self.request}).data
        self.assertSetEqual(set(data.keys()), {'url', 'legend', 'type', 'author', 'filetype', 'title', 'thumbnail'})
        self.assertEqual(data['type'], 'file')

    def test_attachment_video_content(self):
        data = self.serializer_attachment(instance=self.attachment_video,
                                          context={'request': self.request}).data
        self.assertSetEqual(set(data.keys()), {'url', 'legend', 'type', 'author', 'filetype', 'title', 'thumbnail'})
        self.assertEqual(data['type'], 'video')
        self.assertEqual(data['url'], 'https://www.youtube.com/embed/Jm3anSjly0Y?wmode=opaque')

    @mock.patch('easy_thumbnails.files.ThumbnailerFieldFile.get_thumbnail', side_effect=IOError)
    def test_attachment_thumbnail_fail(self, mock_thumbnailer):
        data = self.serializer_attachment(instance=self.attachment_image,
                                          context={'request': self.request}).data
        self.assertSetEqual(set(data.keys()), {'url', 'legend', 'type', 'author', 'filetype', 'title', 'thumbnail'})
        self.assertEqual(data['thumbnail'], '')

    def test_attachment_empty_content(self):
        data = self.serializer_attachment(instance=self.attachment_empty,
                                          context={'request': self.request}).data
        self.assertSetEqual(set(data.keys()), {'url', 'legend', 'type', 'author', 'filetype', 'title', 'thumbnail'})
