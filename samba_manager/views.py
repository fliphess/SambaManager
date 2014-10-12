from ConfigParser import NoSectionError
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.views.generic import View

from control.utils.status import Status, SambaTotals
from control.utils import samba_utils as utils
from samba_manager.models import ManageableUser, ManageableGroup, ManageableShare
from samba_manager.forms import AddChangePasswordForm, GroupForm, UserOnlyForm, SambaShareForm


class BaseSambaView(View):
    status = Status()
    template = None
    data = None

    def get(self, request, *args, **kwargs):
        return render(request, self.template, self.status.get())


class IndexView(BaseSambaView):
    status = Status()
    status.add({"totals": SambaTotals()})
    template = 'samba_manager/base.html'


class ListUsers(BaseSambaView):
    status = Status()
    status.add({"users": ManageableUser.objects.all()})
    template = "samba_manager/list_users.html"


class ListGroups(BaseSambaView):
    status = Status()
    status.add(item={"groups": ManageableGroup.objects.all()})
    template = 'samba_manager/list_groups.html'


class ListShares(BaseSambaView):
    status = Status()
    status.add(item={"shares": ManageableShare.objects.all()})
    template = 'samba_manager/list_shares.html'


class AddUser(BaseSambaView):
    status = Status()
    template = "samba_manager/add_user.html"

    def get(self, request, *args, **kwargs):
        self.status.set(message='Fill in all fields to add a user', success=True)
        self.status.add(item={"form": AddChangePasswordForm()})
        return super(AddUser, self).get(request)


    @transaction.atomic()
    def post(self, request):
        form = AddChangePasswordForm(request.POST)

        if form.is_valid():
            name = form.clean()['username']
            pass1 = form.clean()['password']
            pass2 = form.clean()['confirm_password']
            groups = form.clean()['groups']

            if ManageableUser.objects.filter(name=name) or name in settings.USERS:
                self.status.set(message='User already exists', success=False)
            else:
                if pass1 == pass2:
                    utils.add_user(name, pass1)
                    utils.set_user_groups(name, groups)
                    self.status.set(message='User added', success=True)
                    self.status.add(item={"users": ManageableUser.objects.all()})
                    return render(request, 'samba_manager/list_users.html', self.status.get())
                else:
                    self.status.set(message='Passwords do not match.', success=False)
        else:
            self.status.set(message='Invalid input', success=False)

        return self.get(request)


class AddGroup(BaseSambaView):
    status = Status()
    template = "samba_manager/add_group.html"

    def get(self, request, *args, **kwargs):
        self.status.add(item={"form": GroupForm()})
        self.status.set(message='Fill in all fields to add a group', success=True)
        return super(AddGroup, self).get(request)

    def post(self, request):
        form = GroupForm(request.POST)
        if form.is_valid():
            name = form.clean()['name']

            if ManageableGroup.objects.filter(name=name) or name in settings.GROUPS:
                self.status.set(message='Group already exists', success=False)
            else:
                utils.add_group(name)
                self.status.set(message='Group added', success=True)
        else:
            self.status.set(message='Invalid input', success=False)
        return self.get(request)


class AddShare(BaseSambaView):
    status = Status()
    template = "samba_manager/add_share.html"

    def get(self, request, *args, **kwargs):
        self.status.add(item={"form": SambaShareForm()})
        self.status.set(message='Fill in all fields to add a share', success=True)
        return super(AddShare, self).get(request)

    @transaction.atomic()
    def post(self, request):
        form = SambaShareForm(request.POST)

        if form.is_valid():
            name = form.clean()['name']

            if ManageableGroup.objects.filter(name=name):
                self.status.set(message='Group already exists', success=False)
            else:
                utils.add_change_samba_share(form.clean())
                self.status.set(message='Share added', success=True)
                self.status.add(item={"shares": ManageableShare.objects.all()})
        else:
            self.status.set(message='Invalid input', success=False)
        return self.get(request)


class EditUser(View):
    status = Status()
    status.set(message="Update all fields to edit a user", success=True)
    template = "samba_manager/add_user.html"

    def get(self, request, id):
        user = get_object_or_404(ManageableUser, pk=id)
        self.status.add(item={"form": UserOnlyForm(initial={
            'username': user.name, 'groups': utils.get_user_groups(user.name)})})
        return render(request, self.template, self.status.get())

    @transaction.atomic()
    def post(self, request, id):
        form = UserOnlyForm(request.POST)
        user = get_object_or_404(ManageableUser, pk=id)

        if form.is_valid():
            name = user.name
            groups = form.clean()['groups']
            utils.set_user_groups(name, groups)

            self.status.set(message="User %s updated" % name, success=True)
            self.status.add(item={"users": ManageableUser.objects.all()})
            return render(request, "samba_manager/list_users.html", self.status.get())
        else:
            self.status.set(success=False, message='Invalid input')
            return self.get(request, id)


class EditShare(View):
    status = Status()
    status.set(message='Update all fields to edit a share', success=True)
    template = "samba_manager/add_share.html"

    def get(self, request, id):
        share = get_object_or_404(ManageableShare, pk=id)
        share_conf = utils.get_samba_conf()
        try:
            groups = map(lambda x: x.lstrip('@'), share_conf.get(share.name, 'valid users').split(' '))

            initial = {
                'name': share.name,
                'comment': share_conf.get(share.name, 'comment'),
                'allowed_groups': groups,
            }
        except NoSectionError:
            # Insert wild error message here
            groups = []
            initial = {}

        self.status.add(item={"groups": groups, "share": share})
        self.status.add(item={"form": SambaShareForm(initial=initial)})
        return render(request, self.template, self.status.get())

    @transaction.atomic()
    def post(self, request, id):
        form = SambaShareForm(request.POST)
        if form.is_valid():
            utils.add_change_samba_share(form.clean())
            self.status.set(message="Shared updated", success=True)
            self.status.add(item={"shares": ManageableShare.objects.all()})
            return render(request, "samba_manager/list_shares.html", self.status.get())
        else:
            self.status.set(message="Invalid input", success=True)
            return self.get(request, id)


class BaseDeleteView(View):
    status = Status()
    template = None
    model = None
    element = None

    def get(self, request, id):
        data = get_object_or_404(self.model, pk=id)
        self.status.add(item={self.element: data})
        return render(request, self.template, self.status.get())


class DeleteUser(BaseDeleteView):
    status = Status()
    template = "samba_manager/delete_user.html"
    model = ManageableUser
    element = "user"

    @transaction.atomic()
    def post(self, request, id):
        user = get_object_or_404(ManageableUser, pk=id)

        if request.POST.get('delete', None) == '1':
            utils.del_user(user.name)
            self.status.set(message="User deleted", success=True)
            self.status.add(item={"users": ManageableUser.objects.all()})
            return render(request, "samba_manager/list_users.html", self.status.get())
        else:
            self.status.set(message="Deletion canceled", success=False)
        return self.get(request, id)


class DeleteGroup(BaseDeleteView):
    status = Status()
    template = 'samba_manager/delete_group.html'
    model = ManageableGroup
    element = "group"

    @transaction.atomic()
    def post(self, request, id):
        group = get_object_or_404(ManageableGroup, pk=id)
        if request.POST.get('delete', None) == '1':
            utils.del_group(group.name)
            self.status.set(message='Group deleted', success=True)
            self.status.add(item={"shares": ManageableGroup.objects.all()})
            return render(request, "samba_manager/list_groups.html", self.status.get())
        else:
            self.status.set(message="Deletion canceled", success=False)
        return self.get(request, id)


class DeleteShare(BaseDeleteView):
    status = Status()
    template = "samba_manager/delete_share.html"
    model = ManageableShare
    element = "share"

    @transaction.atomic()
    def post(self, request, id):
        share = get_object_or_404(ManageableShare, pk=id)
        if request.POST.get('delete', None) == '1':
            utils.del_samba_share(share.name)
            self.status.set(message="Share deleted", success=True)
        else:
            self.status.set(message="Deletion canceled", success=False)

        self.status.add(item={"shares": ManageableShare.objects.all()})
        return render(request, "samba_manager/list_shares.html", self.status.get())

