import os

from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import static

from mapentity import views as mapentity_views


from georiviere.main.models import Attachment


class DocumentReportMixin:
    template_name_suffix = "_report"

    # Override view_permission_required
    def dispatch(self, *args, **kwargs):
        return super(mapentity_views.MapEntityDocumentBase, self).dispatch(*args, **kwargs)

    def get(self, request, pk, slug, lang=None):
        obj = get_object_or_404(self.model, pk=pk)

        attachments = Attachment.objects.filter(content_type=obj.get_content_type_id(), object_id=obj.pk)
        if not attachments:
            return super().get(request, pk, slug, lang)
        if not attachments:
            return HttpResponseNotFound("No attached file")
        path = attachments[0].attachment_file.name

        if settings.DEBUG:
            response = static.serve(self.request, path, settings.MEDIA_ROOT)
        else:
            response = HttpResponse()
            response[settings.MAPENTITY_CONFIG['SENDFILE_HTTP_HEADER']] = os.path.join(settings.MEDIA_URL_SECURE, path)
        response["Content-Type"] = 'application/pdf'
        response['Content-Disposition'] = "attachment; filename={0}.pdf".format(slug)
        return response
