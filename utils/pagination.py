from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE_SIZE = 18

class DataPageNumberPagination(PageNumberPagination):

    page_size = DEFAULT_PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        ENV = settings.ENV
        if next_link and ENV == 'prod':
            next_link = next_link.replace('http', 'https')

        return Response({
            'count': self.page.paginator.count,
            'previous': self.get_previous_link(),
            'next': next_link,
            'results': data
        })


class CommentMsgPagination(DataPageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
