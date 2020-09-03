from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, BookCreateEditSerializer


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BookSerializer
        return BookCreateEditSerializer

    def get_queryset(self):
        qs = Book.objects.all()

        if self.action == 'list' and 'title' in self.request.query_params:
            qs = qs.filter(title__contains=self.request.query_params['title'])

        return qs.prefetch_related('authors')


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            'access_token': user.username,
            'token_type': 'bearer',
        })
