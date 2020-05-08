from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import mixins, generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from party.account.models import Avatar, Position
from party.account.serializers import UserSerializer, AvatarSerializer, UserListSerializer, PositionSerializer
from party.core.permissions import IsUserOrReadOnly
from party.event.models import Event

User = get_user_model()


def qr_code_scan(request, pk):
    qr_id_data = request.POST.get('id', '')
    qr_id_data = qr_id_data.split('/')[-1]
    id = re.sub('[^0-9]', '', qr_id_data)
    if request.method == 'POST' and id:
        user = User.objects.filter(id=id).first()
        if user:
            event = get_object_or_404(Event, pk=pk)
            event.user.add(user)
            event.save()
    return render(request, 'user/scan.html', {'site_header': 'scan qr code'})


def user_detail(request, pk):
    user = User.objects.filter(id=pk).first()
    return render(request, 'user/user_detail.html', {
        'app_label': 'account',
        'user': user})


def event_users_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participants = event.participants.user.all()
    return render(request, 'user/user_list.html', {'users': participants})


class UserView(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOrReadOnly]

    @action(methods=['POST', 'GET'], detail=False)
    def avatar(self, request):
        if request.method == 'POST':
            Avatar.objects.filter(user=request.user).delete()
            data = request.data
            data['user'] = request.user.id
            serializer = AvatarSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            serializer = AvatarSerializer(Avatar.objects.filter(user=request.user).first(),
                                          context={'request': request})
            return Response(serializer.data)


class PartyMembers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['position']

    def get_queryset(self):
        if search := self.request.GET.get('search', None):
            self.queryset = self.queryset.filter(
                Q(name__icontains=search) |
                Q(surname__icontains=search) |
                Q(patronymic__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        return self.queryset


class PositionList(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
