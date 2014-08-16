from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from control.status import Status
from server_manager.forms import ServerCommandForm
from server_manager.models import ServerCommand


@login_required(login_url="/login/")
def command_overview(request):
    commands = ServerCommand.objects.all()
    return render(request, "server_manager/command_overview.html", {"commands": commands})


@login_required(login_url="/login/")
def command_editor(request):
    commands = ServerCommand.objects.all()
    return render(request, "server_manager/command_editor.html", {"commands": commands})


@transaction.atomic()
@login_required(login_url="/login/")
def add_command(request):
    status = Status()
    status.set(message="Fill in all fields to add a command", success=True)

    if request.method == "POST":
        form = ServerCommandForm(request.POST)

        if form.is_valid():
            visible = form.clean()["visible"]
            sudo = form.clean()["sudo"]
            name = form.clean()["name"]
            command = form.clean()["command"]
            title = form.clean()["title"]

            if ServerCommand.objects.filter(name=name):
                status.set(message="Command already exists", success=False)
            else:
                ServerCommand.objects.create(name=name, visible=visible, sudo=sudo, command=command, title=title)
                status.set(message="Command added", success=True)
                status.add(item={"commands": ServerCommand.objects.all()})
                return render(request, "server_manager/command_editor.html", status.get())
        else:
            status.set(message='Invalid input', success=False)

    status.add({"form": ServerCommandForm()})
    return render(request, "server_manager/add_command.html", status.get())


@transaction.atomic()
@login_required(login_url="/login/")
def edit_command(request, name):
    command = get_object_or_404(ServerCommand, name=name)

    initial = {
        "visible": command.visible,
        "sudo": command.sudo,
        "name": command.name,
        "command": command.command,
        "title": command.title,
    }

    status = Status()
    status.set(message="Update all fields to edit a command", success=True)

    if request.method == "POST":
        form = ServerCommandForm(request.POST)
        if form.is_valid():
            command.visible = form.clean()["visible"]
            command.sudo = form.clean()["sudo"]
            command.name = form.clean()["name"]
            command.command = form.clean()["command"]
            command.title = form.clean()["title"]
            command.save(force_update=True)

            status.set(success=True, message="Command updated")
            status.add(item={"commands": ServerCommand.objects.all()})
            return render(request, "server_manager/command_editor.html", status.get())

        else:
            status.set(success=False, message='Invalid input')

    status.add(item={"form": ServerCommandForm(initial=initial), "command": command})
    return render(request, "server_manager/edit_command.html", status.get())


@transaction.atomic()
@login_required(login_url="/login/")
def delete_command(request, name):
    command = get_object_or_404(ServerCommand, name=name)
    status = Status()
    status.add(item={"command": command})

    if request.method == "POST":
        if request.POST.get("delete", None) == "1":
            ServerCommand.objects.get(name=name).delete()
            status.set(success=True, message="Command deleted")
        else:
            status.set(success=False, message="Deletion of command %s canceled" % command.name)

        status.add(item={"commands": ServerCommand.objects.all()})
        return render(request, "server_manager/command_editor.html", status.get())
    return render(request, "server_manager/delete_command.html", status.get())
