from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from server_control.forms import ServerCommandForm
from server_control.models import ServerCommand


@login_required(login_url='/login/')
def index(request):
    return render(request, 'server_control/base.html', {'text': 'This should become some wild overview page with statistics and logs and events and messages but for now all you got is this lousy empty page'})


@login_required(login_url='/login/')
def overview(request):
    commands = ServerCommand.objects.all()
    return render(request, 'server_control/overview.html', {'commands': commands})


@login_required(login_url='/login/')
def list_commands(request):
    commands = ServerCommand.objects.all()
    return render(request, 'server_control/list_commands.html', {'commands': commands})


@transaction.atomic()
@login_required(login_url='/login/')
def add_command(request):
    message = 'Fill in all fields to add a user'
    success = True

    if request.method == 'POST':
        form = ServerCommandForm(request.POST)
        if form.is_valid():
            enabled = form.clean()['enabled']
            name = form.clean()['name']
            command = form.clean()['command']
            title = form.clean()['title']

            if ServerCommand.objects.filter(name=name):
                message = 'Command already exists'
                success = False

            else:
                ServerCommand.objects.create(name=name, enabled=enabled, command=command, title=title)
                message = 'Command added'
                success = True
    else:
        form = ServerCommandForm()
    return render(request, 'server_control/add_command.html', {'form': form, 'message': message, 'success': success})


@transaction.atomic()
@login_required(login_url='/login/')
def edit_command(request, name):
    command = get_object_or_404(ServerCommand, name=name)
    if request.method == 'POST':
        form = ServerCommandForm(request.POST)
        if form.is_valid():
            command.enabled = form.clean()['enabled']
            command.name = form.clean()['name']
            command.command = form.clean()['command']
            command.title = form.clean()['title']
            command.save(force_update=True)
            return HttpResponseRedirect(reverse('edit_command', args=(command.name,)))
    else:
        form = ServerCommandForm()
    return render(request, 'server_control/edit_command.html', {'command': command, 'form': form})


@transaction.atomic()
@login_required(login_url='/login/')
def delete_command(request, name):
    command = get_object_or_404(ServerCommand, name=name)

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            ServerCommand.objects.get(name=name).delete()
            return HttpResponseRedirect(reverse('list_commands'))
    return render(request, 'server_control/delete_command.html', {'command': command})
