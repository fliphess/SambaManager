from django import forms


class ServerCommandForm(forms.Form):
    enabled = forms.BooleanField(required=False, label="Enable")
    sudo = forms.BooleanField(required=False, label="Enable")
    name = forms.CharField(required=True, label="Name")
    command = forms.CharField(required=True, label="Command")
    title = forms.CharField(required=True, label="Title")