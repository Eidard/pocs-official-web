from .serializers import AccountSerializer
from rest_framework import generics
from .models import Account


class SignUpView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer




