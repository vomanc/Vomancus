""" The views modul """
import smtplib
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import DeleteView, DetailView
from django.views.generic.edit import FormMixin
from .utils import email_activation_token
from .models import AccountsModel, TwitterAPIModel
from .forms import RegistrationUserForm, AccountUpdateForm, TwitterAPIForm


def response_error_handler(request, exception=None):
    """ If 403 error """
    return render(request, 'main/error_404.html', status=404)


def index(requests):
    """ Home page """
    return render(requests, 'main/index.html')


def about(requests):
    """ About page """
    return render(requests, 'main/about.html')


@login_required(login_url='signin')
def account(requests, pk):
    """ User account """
    obj = get_object_or_404(AccountsModel, id=pk)
    obj.password = None
    return render(requests, 'account/account.html', {"account": obj})


def signin(request):
    """ Sign in """
    if request.user.is_authenticated:
        return redirect(f'/account/{request.user.id}')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/account/{request.user.id}')
        messages.error(request, 'Error login or password')
        return redirect('signin')
    return render(request, 'account/signin.html')


@login_required(login_url='signin')
def logout_(request):
    """  Logout in User  """
    logout(request)
    return redirect('/')


def send_activation_email(request, user_email):
    """ Send email verification token """
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_message = render_to_string('account/verification_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'protocol': 'http',
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token': email_activation_token.make_token(request.user)
    })
    send_mail(
        subject=email_subject,
        message=email_message,
        from_email='aperna@mail.com',
        recipient_list=[user_email],
    )
    messages.success(request, 'Your email data was successfully updated! \
    The confirmation link is sent to your mail')


def verification_email(request, udb_64, token):
    """ Check token from email """
    uid = force_str(urlsafe_base64_decode(udb_64))
    user = AccountsModel.objects.get(pk=uid)
    if user and email_activation_token.check_token(user, token):
        user.confirm_email = True
        user.save()
        messages.success(request, 'Email verified, you can now login')
        return redirect('signin')
    messages.error(request, "ERROR")
    return render(request, 'account/account.html', {"user": user})


def signup(request):
    """ Registration User """
    if request.user.is_authenticated:
        return redirect(f'/account/{request.user.id}')
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Successful registration')
            login(request, user)
            try:
                send_activation_email(request, form['email'].value())
            except smtplib.SMTPRecipientsRefused:
                messages.error(request, 'Error: SMTP Recipients Refused')
            return redirect('signin')
        if AccountsModel.objects.filter(username=form["username"].value()).exists() is True:
            messages.error(
                request, f'Error, username — {form["username"].value()} already in use!')
        if AccountsModel.objects.filter(email=form["email"].value()).exists() is True:
            messages.error(request, f'Error, email — {form["email"].value()} already in use!')
    form = RegistrationUserForm
    context = {"form": form}
    return render(request, 'account/signup.html', context)


@login_required(login_url='signin')
def account_update(request):
    """ Account update """
    curr_account = AccountsModel.objects.get(id=request.user.id)
    form_account_upd = AccountUpdateForm(instance=curr_account)
    if request.method == 'POST':
        form_account = AccountUpdateForm(request.POST, request.FILES, instance=curr_account)
        if form_account.is_valid():
            # Email check if changed or not confirmed
            if request.user.email != curr_account.email or curr_account.confirm_email is False:
                form_account = form_account.save(commit=False)
                form_account.confirm_email = False
                request.user.email = request.POST['email']
                try:
                    send_activation_email(request, request.POST['email'])
                except smtplib.SMTPRecipientsRefused:
                    messages.error(request, 'Error: SMTP Recipients Refused')
            form_account.save()
            messages.success(request, 'Your account data was successfully updated!')
            return redirect('/account-update')
        messages.error(request, 'Incorrect data!')
        return redirect('/account-update/')

    context = {
        'form_account_upd': form_account_upd,
        'email_status': curr_account.confirm_email
    }
    return render(request, 'account/update_account.html', context)


@login_required(login_url='signin')
def change_password(request):
    """ Change Account Passwd """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(f'/account/{request.user.id}')
        messages.error(request, 'Please correct the error below.')
    form = PasswordChangeForm(request.user)
    return render(request, 'account/signup.html', {'form': form})


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """ Delete new """
    login_url = 'signin'
    model = AccountsModel
    template_name = 'main/delete.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user


class SocialMediaDetailView(LoginRequiredMixin, FormMixin, DetailView):
    """ Update API KEYS """
    login_url = 'signin'
    template_name = 'account/social_media.html'
    form_class = TwitterAPIForm
    success_url = '/account-social'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        objects = TwitterAPIModel.objects.filter(owner_id=self.request.user.id)
        if objects.exists():
            return objects.get()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TwitterAPIForm(instance=self.get_object())
        return context

    def post(self, request):
        form = TwitterAPIForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        v = form.save(commit=False)
        TwitterAPIModel.objects.update_or_create(
            defaults={
                'owner': self.request.user,
                'consumer_key': v.consumer_key,
                'consumer_secret': v.consumer_secret,
                'access_token': v.access_token,
                'access_token_secret': v.access_token_secret
            },
            owner=self.request.user
        )
        messages.success(self.request, 'Keys successfully updated')
        return HttpResponseRedirect(self.get_success_url())

