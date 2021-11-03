from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserManage
from .serializers import UserManageSerializer


class UserManageViewSet(viewsets.ModelViewSet):
    queryset = UserManage.objects.all()
    serializer_class = UserManageSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        return Response({'status': 'success', 'code': 200})
