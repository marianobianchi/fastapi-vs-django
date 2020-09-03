from rest_framework import pagination
from rest_framework.response import Response


class OnlyResultsPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(data)

    def get_count(self, queryset):
        # avoid calling database for a count query
        return self.default_limit + 1
