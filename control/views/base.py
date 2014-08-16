from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def start(request):
    return render(request, 'auth/main.html')


@login_required(login_url='/login/')
def run_command(request, name):
    return render(request, 'auth/main.html')
