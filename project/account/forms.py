from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import SelectDateWidget
from .models import AccountsModel, TwitterAPIModel


class RegistrationUserForm(UserCreationForm):
    """ The Form for Sign up """
    class Meta:
        model = AccountsModel
        fields = ("username", "email", "password1", "password2")


class AccountUpdateForm(UserChangeForm):
    """ Form for account updating """
    class Meta:
        model = AccountsModel
        fields = ('email', 'username', 'first_name', 'last_name',
                  'gender', 'date_of_birth', 'avatar', 'twitter',
                  'mastodon', 'signal', 'github', 'telegram')
        widgets = {"date_of_birth": SelectDateWidget(years=range(1920, 2023))}

    def clean(self):
        """ If choose {Clear}: delete file """
        cleaned_data = super().clean()
        avatar_clear = cleaned_data.get("avatar")

        if avatar_clear is False:
            self.instance.avatar.delete(False)


class TwitterAPIForm(UserChangeForm):
    """ For update Social Media """
    class Meta:
        model = TwitterAPIModel
        fields = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')
