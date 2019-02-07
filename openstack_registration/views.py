from django.shortcuts import render
from django.conf.urls import url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django import shortcuts
from django.conf import settings

from . import forms

import requests
import json
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages

@sensitive_post_parameters()
@csrf_protect
@never_cache
def signup(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Successfully created account. Please check your email to verify your account before logging in.')
            return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = forms.UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def verify(request):
    if request.GET.get('token') is not None:
        payload = {'token': request.GET.get('token')}
        headers = {'Content-type': 'application/json'}
        res = requests.post(settings.EMAIL_VERIFICATION_URL, data=json.dumps(payload), headers=headers)

        if res.status_code == 200:
            messages.success(request, 'Email Address Verified! Please log in.')
            return redirect('/auth/login')

    raise Http404()

def reset_password(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)
    
    if request.method == 'POST':
        form = forms.UserResetPasswordForm(request.POST)
        if form.is_valid():
            messages.success(request, "We have sent a password reset link. Please check your email.")
            return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = forms.UserResetPasswordForm()

    return render(request, 'registration/reset_password.html', {'form': form})

@sensitive_post_parameters()
@csrf_protect
@never_cache
def password_update(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = forms.UserPasswordUpdateForm(request.POST)
        if form.is_valid():
            token = request.path.rsplit('/', 1)[-1]
            password = form.cleaned_data['password1']
            payload = {'token': token, 'password': password}
            headers = {'Content-type': 'application/json'}
            res = requests.post(settings.PASSWORD_UPDATE_URL, data=json.dumps(payload), headers=headers)
            if res.status_code == 200:
                messages.success(request, "Password updated successfully. Please log in.")
            else:
                messages.error(request, "That reset link does not exist or has expired. Please request a new reset password link by going to the reset password page.")
            return redirect('/auth/login')

    else:
        form = forms.UserPasswordUpdateForm()
        return render(request, 'registration/password_update.html', {'form': form})