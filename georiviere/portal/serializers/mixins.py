class SerializerAPIMixin:
    def _get_url_detail_kwargs(self, pk, format="json"):
        return {
            "lang": self.context["lang"],
            "portal_pk": self.context["portal_pk"],
            "format": format,
            "pk": pk,
        }
