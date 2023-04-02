from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.models import AccountsModel
from .serializers import AccountSerializers, RegistrationSerializers


class AccountView(generics.RetrieveAPIView):
    queryset = AccountsModel.objects.all()
    serializer_class = AccountSerializers


class AccountsListView(generics.ListAPIView):
    """ Account list """
    queryset = AccountsModel.objects.all()
    serializer_class = AccountSerializers
    permission_classes = [IsAuthenticated]


class RegistrationView(generics.CreateAPIView):
    """ Account registration """
    queryset = AccountsModel.objects.all()
    serializer_class = RegistrationSerializers
    permission_classes = [AllowAny]
