from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login/')
def index(request):
    return render(request, 'server_control/base.html', {'text': 'This should become some wild overview page with statistics and logs and events and messages but for now all you got is this lousy empty page'})
