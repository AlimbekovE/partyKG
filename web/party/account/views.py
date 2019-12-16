import re

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import render
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
