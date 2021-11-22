from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Configuration


@api_view(['POST'])
def fetch_spe_config(request):
    keys = request.data.get('keys', [])
    query = Configuration.objects.filter(key__in=keys).values('key',
                                                              'uni_val',
                                                              'opt_val_one')
    return Response(query)