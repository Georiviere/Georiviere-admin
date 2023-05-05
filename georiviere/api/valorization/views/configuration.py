from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework import response


class SettingsView(APIView):
    permission_classes = [AllowAny, ]

    def get_configuration_map(self):
        val = ""
        return val

    def get(self, request, *args, **kwargs):
        return response.Response()
