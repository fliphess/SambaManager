from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def start(request):
    return render(request, 'auth/main.html')
