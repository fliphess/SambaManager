from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.http import HttpResponseRedirect

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
    message = 'Fill in all fields to add a user'
    success = True

    if request.method == 'POST':
        form = AddChangePasswordForm(request.POST)
        if form.is_valid():
            name = form.clean()['username']
            pass1 = form.clean()['password']
            pass2 = form.clean()['confirm_password']
            groups = form.clean()['groups']

            if ManageableUser.objects.filter(name=name) or name in settings.USERS:
                message = 'User already exists'
                success = False

            else:
                if pass1 == pass2:
                    utils.add_user(name, pass1)
                    utils.set_user_groups(name, groups)
                    message = 'User added'
                    success = True
                else:
                    message = 'Passwords do not match.'
                    success = False
    else:
        form = AddChangePasswordForm()
    return render(request, 'samba_manager/add_user.html', {'form': form, 'message': message, 'success': success})


@transaction.atomic()
@login_required(login_url='/login/')
def add_group(request):
    message = 'Fill in all fields to add a group'
    success = True

    if request.method == 'POST':
        form = GroupForm(request.POST)
        message = 'Invalid input'
        success = False

        if form.is_valid():
            utils.add_group(form.clean()['name'])
            message = 'Group added'
            success = True
    else:
        form = GroupForm()
    return render(request, 'samba_manager/add_group.html', {'form': form, 'message': message, 'success': success})


@transaction.atomic()
@login_required(login_url='/login/')
def add_share(request):
    message = 'Fill in all fields to add a share'
    success = True

    if request.method == 'POST':
        form = SambaShareForm(request.POST)
        if form.is_valid():
            utils.add_change_samba_share(form.clean())
            message = 'Share added'
            success = True
    else:
        form = SambaShareForm()
    return render(request, 'samba_manager/add_share.html', {'form': form, 'message': message, 'success': success})


@transaction.atomic()
@login_required(login_url='/login/')
def edit_user(request, id):
    user = get_object_or_404(ManageableUser, pk=id)
    if request.method == 'POST':
        form = UserOnlyForm(request.POST)
        if form.is_valid():
            utils.set_user_groups(user.name, form.clean()['groups'])
            return HttpResponseRedirect(reverse('edit_user', args=(user.pk,)))
    else:
        form = UserOnlyForm(initial={'username': user.name, 'groups': utils.get_user_groups(user.name)})
    return render(request, 'samba_manager/edit_user.html', {'user': user, 'form': form})


@transaction.atomic()
@login_required(login_url='/login/')
def edit_share(request, id):
    share = get_object_or_404(ManageableShare, pk=id)
    share_conf = utils.get_samba_conf()

    if request.method == 'POST':
        form = SambaShareForm(request.POST)
        if form.is_valid():
            utils.add_change_samba_share(form.clean())
    else:
        groups = map(lambda x: x.lstrip('@'), share_conf.get(share.name, 'valid users').split(' '))
        form = SambaShareForm(initial={'allowed_groups': groups,
                                       'name': share.name,
                                       'comment': share_conf.get(share.name, 'comment')})
    return render(request, 'samba_manager/add_share.html', {'form': form})


@transaction.atomic()
@login_required(login_url='/login/')
def delete_user(request, id):
    user = get_object_or_404(ManageableUser, pk=id)

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            utils.del_user(user.name)
            return HttpResponseRedirect(reverse('list_users'))
    return render(request, 'samba_manager/delete_user.html', {'user': user})


@transaction.atomic()
@login_required(login_url='/login/')
def delete_group(request, id):
    group = get_object_or_404(ManageableGroup, pk=id)

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            utils.del_group(group.name)
            return HttpResponseRedirect(reverse('list_groups'))
    return render(request, 'samba_manager/delete_group.html', {'group': group})


@transaction.atomic()
@login_required(login_url='/login/')
def delete_share(request, id):
    share = get_object_or_404(ManageableShare, pk=id)

    if request.method == 'POST':
        if request.POST.get('delete', None) == '1':
            utils.del_samba_share(share.name)
            return HttpResponseRedirect(reverse('list_shares'))
    return render(request, 'samba_manager/delete_share.html', {'share': share})
