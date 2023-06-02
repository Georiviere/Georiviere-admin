from easy_thumbnails.alias import aliases
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer
from PIL.Image import DecompressionBombError
from rest_framework import serializers

from geotrek.api.v2.utils import build_url

from georiviere.main import models as main_models


class AttachmentsSerializerMixin(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(write_only=True, required=False)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    license = serializers.SlugRelatedField(
        read_only=True,
        slug_field='label'
    )

    def get_attachment_file(self, obj):
        return obj.attachment_file

    def get_thumbnail(self, obj):
        thumbnailer = get_thumbnailer(self.get_attachment_file(obj))
        try:
            thumbnail = thumbnailer.get_thumbnail(aliases.get('valorization'))
        except (IOError, InvalidImageFormatError, DecompressionBombError):
            return ""
        thumbnail.author = obj.author
        thumbnail.legend = obj.legend
        return build_url(self, thumbnail.url)

    def get_url(self, obj):
        if obj.attachment_file:
            return build_url(self, obj.attachment_file.url)
        if obj.attachment_video:
            return obj.attachment_video
        if obj.attachment_link:
            return obj.attachment_link
        return ""

    class Meta:
        model = main_models.Attachment
        fields = (
            'author', 'thumbnail', 'legend', 'title', 'url', "author", "image"
        )


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.FileType
        fields = ('id', 'structure', 'type')


class AttachmentSerializer(AttachmentsSerializerMixin):
    type = serializers.SerializerMethodField(read_only=True)
    filetype = FileTypeSerializer(many=False, read_only=True)

    def get_type(self, obj):
        if obj.is_image or obj.attachment_link:
            return "image"
        if obj.attachment_video != '':
            return "video"
        return "file"

    class Meta:
        model = main_models.Attachment
        fields = (
            'type', 'filetype',
        ) + AttachmentsSerializerMixin.Meta.fields
