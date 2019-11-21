from django.utils.translation import gettext as _
from django.contrib.auth import logout

from rest_framework import permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from party.account.serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            raise exceptions.NotFound(_('User is not signed in'))
        logout(request)
        token.delete()

        return Response({'status': 'success'})
