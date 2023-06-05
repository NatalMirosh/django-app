from django import forms


class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField(label='Upload Avatar')