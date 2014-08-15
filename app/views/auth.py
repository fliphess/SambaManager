from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render

def logout_view(request):
    logout(request)
    return redirect('/')

def main(request):
    return render(request, 'auth/main.html', {'text': 'Log in to proceed'})