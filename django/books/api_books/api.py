from rest_framework import viewsets

from .models import Book
from .serializers import BookSerializer, BookCreateEditSerializer


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BookSerializer
        return BookCreateEditSerializer

    def get_queryset(self):
        qs = Book.objects.all()

        if self.action == 'list' and 'title' in self.request.query_params:
            qs = qs.filter(title__contains=self.request.query_params['title'])

        return qs.prefetch_related('authors')
