from django.conf import settings
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from control.utils.command import logger, executor

from control.utils.status import Status
from server_manager.forms import ServerCommandForm
from server_manager.models import ServerCommand


class BaseCommandView(View):
    status = Status()
    template = None

    def get(self, request, **kwargs):
        self.status.add(item={"commands": ServerCommand.objects.all()})
        return render(request, self.template, self.status.get())


class CommandOverView(BaseCommandView):
    template = "server_manager/command_overview.html"

    def get(self, request, **kwargs):
        return super(CommandOverView, self).get(request)


class CommandEditor(CommandOverView):
    template = "server_manager/command_editor.html"


class AddCommand(BaseCommandView):
    template = "server_manager/add_command.html"

    def get(self, request, **kwargs):
        self.status.add({"form": ServerCommandForm()})
        self.status.set(message="Fill in all fields to add a command", success=True)
        return super(AddCommand, self).get(request)

    @transaction.atomic()
    def post(self, request):
        form = ServerCommandForm(request.POST)

        if form.is_valid():
            visible = form.clean()["visible"]
            sudo = form.clean()["sudo"]
            name = form.clean()["name"]
            command = form.clean()["command"]
            title = form.clean()["title"]

            if ServerCommand.objects.filter(name=name):
                self.status.set(message="Command already exists", success=False)
            else:
                ServerCommand.objects.create(name=name, visible=visible, sudo=sudo, command=command, title=title)
                self.status.set(message="Command added", success=True)
                self.status.add(item={"commands": ServerCommand.objects.all()})
                return render(request, "server_manager/command_editor.html", self.status.get())
        else:
            self.status.set(message='Invalid input', success=False)
            return self.get(request=request)


class EditCommand(View):
    status = Status()
    status.set(message="Update all fields to edit a command", success=True)
    template = "server_manager/edit_command.html"

    def get(self, request, name):
        command = get_object_or_404(ServerCommand, name=name)
        initial = {
            "visible": command.visible,
            "sudo": command.sudo,
            "name": command.name,
            "command": command.command,
            "title": command.title,
        }
        self.status.add(item={"form": ServerCommandForm(initial=initial), "command": command})
        return render(request, self.template, self.status.get())

    @transaction.atomic()
    def post(self, request, name):
        form = ServerCommandForm(request.POST)
        command = get_object_or_404(ServerCommand, name=name)

        if form.is_valid():
            command.visible = form.clean()["visible"]
            command.sudo = form.clean()["sudo"]
            command.name = form.clean()["name"]
            command.command = form.clean()["command"]
            command.title = form.clean()["title"]
            command.save(force_update=True)

            self.status.set(success=True, message="Command updated")
            self.status.add(item={"commands": ServerCommand.objects.all()})
            return render(request, "server_manager/command_editor.html", self.status.get())

        else:
            self.status.set(success=False, message='Invalid input')
            return self.get(request, name)


class DeleteCommand(View):
    status = Status()

    def get(self, request, name):
        command = get_object_or_404(ServerCommand, name=name)
        self.status.add(item={"command": command})
        return render(request, "server_manager/delete_command.html", self.status.get())

    @transaction.atomic()
    def post(self, request, name):
        command = get_object_or_404(ServerCommand, name=name)
        self.status.add(item={"command": command})

        if request.POST.get("delete", None) == "1":
            ServerCommand.objects.get(name=name).delete()
            self.status.set(success=True, message="Command deleted")
            self.status.add(item={"commands": ServerCommand.objects.all()})
            return render(request, "server_manager/command_editor.html", self.status.get())

        self.status.set(success=False, message="Deletion of command %s canceled" % command.name)
        return self.get(request, name)


class CommandExecutor(BaseCommandView):
    status = Status()
    template = 'server_manager/command_overview.html'

    def post(self, request, name):
        command = get_object_or_404(ServerCommand, name=name)
        self.status.add(item={"command": command})

        if request.POST.get("name", None) != name:
            self.status.set(message="Incorrect input", success=False)
            return self.get(request, name)

        command_line = '%s -n %s' % (settings.REMOTE_EXECUTOR, name)
        l = logger(name=name)
        output, exitcode = executor(script=command_line, log=l, sudo=command.sudo)
        self.status.add(item={"output": output, "exitcode": exitcode})

        if exitcode == 0:
            self.status.set(message="command %s succeeded" % name, success=True)
        else:
            self.status.set(message="command %s failed" % name, success=False)
        return self.get(request, name)

