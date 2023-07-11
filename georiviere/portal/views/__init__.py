from rest_framework import response, permissions
from rest_framework.views import APIView

from georiviere import __version__


class GeoriviereVersionAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        return response.Response({'version': __version__})
