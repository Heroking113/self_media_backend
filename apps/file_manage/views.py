from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from .models import ImageFile
from .serializers import ImageFileSerializer


class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
    pagination_class = None

    def get_queryset(self):
        inst_type = self.request.query_params.get('inst_type', '0')
        return ImageFile.objects.filter(inst_type=inst_type)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        img_paths = [settings.DOMAIN + '/media/' + i['file_path'] for i in queryset.values('file_path')]
        return Response(img_paths)
