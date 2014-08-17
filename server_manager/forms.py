from django import forms


class ServerCommandForm(forms.Form):
    visible = forms.BooleanField(required=False, label="Visible")
    sudo = forms.BooleanField(required=False, label="Sudo")
    name = forms.CharField(required=True, label="Name")
    command = forms.CharField(required=True, label="Command")
    title = forms.CharField(required=True, label="Title")
