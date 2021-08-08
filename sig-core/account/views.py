from django.shortcuts import render
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.conf import settings


@login_required(login_url='/')
def about(request):
    context = {}
    return render(request, 'site/about.html', context)


@login_required(login_url='/')
def contact(request):
    if request.method == "POST":
        # contact_username = request.POST["username"]
        # contact_email = request.POST['email']
        message = request.POST['subject']
        send_mail(
            request.user.email,
            message,
            settings.EMAIL_HOST_USER,
            ['sigcore.contact@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'site/contact.html', {'message': message})

    else:
        context = {}
        return render(request, 'site/contact.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('../home')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    context = {}
    return render(request, 'account/login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('account:login')


@unauthenticated_user
def registerpage(request):
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain

            link = reverse('account:activate', kwargs={
                'uidb64': uidb64,
                'token': token_generator.make_token(user)
                    }
                )
            activate_url = 'http://'+domain+link

            Email = form.cleaned_data.get('email')

            email_subject = 'Activate your account'

            email_body = 'Hello ' + user.username + ' Please confirm your email by using this link:\n' + activate_url

            email = EmailMessage(
                email_subject,
                email_body,
                'sigcore1@gmail.com',
                [Email],
            )
            email.send(fail_silently=False)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username + ' please verify your email adress')
            return redirect("account:login")

    context = {'form': form}
    return render(request, 'account/register/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('account:login'+'?message='+'User is already activated')

            if user.is_active:
                return redirect('account:login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfuly')
            return redirect('account:login')

        except Exception as ex:
            pass

        return redirect('account:login')



@login_required(login_url='/')
def Profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'informations have been updated ')
            return redirect('/Profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/profile/profile.html', context)

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/Profile/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'account/profile/password_change.html', context)