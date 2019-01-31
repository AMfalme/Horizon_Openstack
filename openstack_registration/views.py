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
        res = requests.post(settings.TOKEN_VERIFICATION_URL, data=json.dumps(payload), headers=headers)

        if res.status_code == 200:
            messages.success(request, 'Email Address Verified! Please log in.')
            return redirect('/auth/login')

    raise Http404()