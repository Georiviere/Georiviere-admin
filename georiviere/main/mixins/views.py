from mapentity import views as mapentity_views


class DocumentReportMixin:
    template_name_suffix = "_report"

    # Override view_permission_required
    def dispatch(self, *args, **kwargs):
        return super(mapentity_views.MapEntityDocumentBase, self).dispatch(*args, **kwargs)
