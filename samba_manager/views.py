from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.http import HttpResponseRedirect
from control.status import Status

from samba_manager import utils
from samba_manager.models import ManageableUser, ManageableGroup, ManageableShare
from samba_manager.forms import AddChangePasswordForm, GroupForm, UserOnlyForm, SambaShareForm


@login_required(login_url='/login/')
def index(request):
    return render(request, 'samba_manager/base.html', {'text': 'This should become some wild overview page with statistics and logs and events and messages but for now all you got is this lousy empty page'})


@login_required(login_url='/login/')
def list_users(request):
    users = ManageableUser.objects.all()
    return render(request, 'samba_manager/list_users.html', {'users': users})


@login_required(login_url='/login/')
def list_groups(request):
    groups = ManageableGroup.objects.all()
    return render(request, 'samba_manager/list_groups.html', {'groups': groups})


@login_required(login_url='/login/')
def list_shares(request):
    shares = ManageableShare.objects.all()
    return render(request, 'samba_manager/list_shares.html', {'shares': shares})


@transaction.atomic()
@login_required(login_url='/login/')
def add_user(request):
    status = Status()
    status.set(message='Fill in all fields to add a user', success=True)

    if request.method == 'POST':
        form = AddChangePasswordForm(request.POST)
        if form.is_valid():
            name = form.clean()['username']
            pass1 = form.clean()['password']
            pass2 = form.clean()['confirm_password']
            groups = form.clean()['groups']

            if ManageableUser.objects.filter(name=name) or name in settings.USERS:
                status.set(message='User already exists', success=False)
            else:
                if pass1 == pass2:
                    utils.add_user(name, pass1)
                    utils.set_user_groups(name, groups)
                    status.set(message='User added', success=True)
                else:
                    status.set(message='Passwords do not match.', success=False)
        else:
            status.set(message='Invalid input', success=False)

        status.add(item={"users": ManageableUser.objects.all()})
        return render(request, 'samba_manager/list_users.html', status.get())

    status.add(item={"form": AddChangePasswordForm()})
    return render(request, 'samba_manager/add_user.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def add_group(request):
    status = Status()
    status.set(message='Fill in all fields to add a group', success=True)

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            name = form.clean()['name']
            if ManageableGroup.objects.filter(name=name) or name in settings.GROUPS:
                status.set(message='Group already exists', success=False)
            else:
                utils.add_group(name)
                status.set(message='Group added', success=True)
        else:
            status.set(message='Invalid input', success=False)
        status.add(item={"groups": ManageableGroup.objects.all()})
        return render(request, 'samba_manager/list_groups.html', status.get())

    status.add(item={"form": GroupForm()})
    return render(request, 'samba_manager/add_group.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def add_share(request):
    status = Status()
    status.set(message='Fill in all fields to add a share', success=True)

    if request.method == 'POST':
        form = SambaShareForm(request.POST)
        if form.is_valid():
            name = form.clean()['name']
            if ManageableGroup.objects.filter(name=name):
                status.set(message='Group already exists', success=False)
            else:
                utils.add_change_samba_share(form.clean())
                status.set(message='Share added', success=True)
        else:
            status.set(message='Invalid input', success=False)
        status.add(item={"shares": ManageableShare.objects.all()})
        return render(request, 'samba_manager/list_shares.html', status.get())

    status.add(item={"form": SambaShareForm()})
    return render(request, 'samba_manager/add_share.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def edit_user(request, id):
    user = get_object_or_404(ManageableUser, pk=id)

    status = Status()
    status.set(message="Update all fields to edit a user", success=True)

    if request.method == 'POST':
        form = UserOnlyForm(request.POST)

        if form.is_valid():
            name= user.name
            groups = form.clean()['groups']
            utils.set_user_groups(name, groups)
            status.set(message="User %s updated" % name, success=True)
            status.add(item={"users": ManageableUser.objects.all()})
            return render(request, "samba_manager/list_users.html", status.get())
        else:
            status.set(success=False, message='Invalid input')

    status.add(item={"form": UserOnlyForm(initial={'username': user.name, 'groups': utils.get_user_groups(user.name)})})
    return render(request, 'samba_manager/edit_user.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def edit_share(request, id):
    share = get_object_or_404(ManageableShare, pk=id)
    share_conf = utils.get_samba_conf()

    status = Status()
    status.set(message='Update all fields to edit a share', success=True)

    if request.method == 'POST':
        form = SambaShareForm(request.POST)
        if form.is_valid():
            utils.add_change_samba_share(form.clean())

            status.set(message="Shared updated", success=True)
            status.add(item={"shares": ManageableShare.objects.all()})
            return render(request, "samba_manager/list_shares.html", status.get())
        else:
            status.set(message="Invalid input", success=True)

    groups = map(lambda x: x.lstrip('@'), share_conf.get(share.name, 'valid users').split(' '))


    status.add(item={"groups": groups, "share": share})
    status.add(item={"form": SambaShareForm(
        initial={
            'name': share.name,
            'comment': share_conf.get(share.name, 'comment'),
            'allowed_groups': groups,
        })
    })
    return render(request, 'samba_manager/edit_share.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def delete_user(request, id):
    user = get_object_or_404(ManageableUser, pk=id)
    status = Status()
    status.add(item={"user": user})

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            utils.del_user(user.name)
            status.set(message="User deleted", success=True)
        else:
            status.set(message="Deletion canceled", success=False)

        status.add(item={"users": ManageableUser.objects.all()})
        return render(request, "samba_manager/list_users.html", status.get())

    return render(request, 'samba_manager/delete_user.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def delete_group(request, id):
    group = get_object_or_404(ManageableGroup, pk=id)
    status = Status()
    status.add(item={"group": group})

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            utils.del_group(group.name)
            status.set(message='Group deleted', success=True)
        else:
            status.set(message="Deletion canceled", success=False)

        status.add(item={"shares": ManageableGroup.objects.all()})
        return render(request, "samba_manager/list_groups.html", status.get())

    return render(request, 'samba_manager/delete_group.html', status.get())


@transaction.atomic()
@login_required(login_url='/login/')
def delete_share(request, id):
    share = get_object_or_404(ManageableShare, pk=id)
    status = Status()
    status.add(item={"share": share})

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            utils.del_samba_share(share.name)
            status.set(message="Share deleted", success=True)
        else:
            status.set(message="Deletion canceled", success=False)

        status.add(item={"shares": ManageableShare.objects.all()})
        return render(request, "samba_manager/list_shares.html", status.get())

    return render(request, 'samba_manager/delete_share.html', status.get())
