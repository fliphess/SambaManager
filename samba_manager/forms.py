import re
from django import forms
from models import ManageableGroup


class UnixUsernameField(forms.CharField):
    def validate(self, value):
        super(UnixUsernameField, self).validate(value)
        
        if len(re.sub('[a-z_\.-]', '', value)) > 0:
            raise forms.ValidationError('Invalid user name')


class UnixGroupField(forms.CharField):
    def validate(self, value):
        super(UnixGroupField, self).validate(value)

        if len(re.sub('[a-z_\.-]', '', value)) > 0:
            raise forms.ValidationError('Invalid group name')


class SambaShareField(forms.CharField):
    def validate(self, value):
        super(SambaShareField, self).validate(value)
        if len(re.sub('[a-z_\.-]', '', value)) > 0:
            raise forms.ValidationError('Invalid share name')

        
class UserOnlyForm(forms.Form):
    username = UnixUsernameField(max_length=50, required=True, label='User')
    groups = forms.ModelMultipleChoiceField(
        label="Group permissions",
        required=False,
        queryset=ManageableGroup.objects.all())


class LoginForm(forms.Form):
    username = UnixUsernameField(max_length=50, required=True, label='User')
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput, label='Password')


class AddChangePasswordForm(LoginForm):
    confirm_password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput, label='Config password')
    groups = forms.ModelMultipleChoiceField(
        label="Group permissions",
        required=False,
        queryset=ManageableGroup.objects.all())


class SambaShareForm(forms.Form):
    name = SambaShareField(label='Name')
    comment = forms.CharField(label='Comment')
    allowed_groups = forms.ModelMultipleChoiceField(
        label="Group permissions",
        required=False,
        queryset=ManageableGroup.objects.all())


class GroupForm(forms.Form):
    name = UnixGroupField(max_length=50, required=True, label='Name')
