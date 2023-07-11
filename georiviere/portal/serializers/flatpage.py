from django.urls import reverse

from georiviere.flatpages.models import FlatPage, FlatPagePicture

from rest_framework.serializers import ModelSerializer, SerializerMethodField


class FlatpagePortalSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = FlatPage
        fields = ('title', 'url', 'order', 'hidden')

    def get_url(self, obj):
        # TODO: Make lang dynamic
        if obj.external_url:
            return obj.external_url
        reverse_kwargs = {'lang': 'fr', 'portal_pk': self.context.get('portal_pk'), 'pk': obj.id}
        return reverse('api_portal:flatpages-detail', kwargs=reverse_kwargs)


class FlatPagePictureSerializer(ModelSerializer):

    class Meta:
        model = FlatPagePicture
        fields = ('picture', )


class FlatPageSerializer(ModelSerializer):
    pictures = FlatPagePictureSerializer(many=True)

    class Meta:
        model = FlatPage
        fields = ('title', 'content', 'pictures')
