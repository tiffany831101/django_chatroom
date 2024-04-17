from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserRetreiveSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def perform_create(self, serializer):
    #     salt = User.objects.make_random_password()

    #     serializer.validated_data['salt'] = salt

    #     serializer.validated_data['password'] = make_password(serializer.validated_data['password'], salt=salt)

    #     serializer.save()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
          return UserRetreiveSerializer
        # else:
        return UserSerializer