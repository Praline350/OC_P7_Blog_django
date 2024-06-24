from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB
MAX_WIDTH = 500
MAX_HEIGHT = 500


class LoginForm(forms.Form):
    login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )
    login_username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={"placeholder": "Nom utilisateur"}),
        label=False,
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
        label=False,
    )


class SignUpForm(UserCreationForm):
    signup_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Nom utilisateur"})
        self.fields["username"].label = False
        self.fields["password1"].widget.attrs.update({"placeholder": "Mot de passe"})
        self.fields["password1"].label = False
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirmez le mot de passe"}
        )
        self.fields["password2"].label = False

        # Remove help texts
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("profile_photo",)
