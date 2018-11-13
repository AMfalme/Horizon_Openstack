from django.shortcuts import render
from django.conf.urls import url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django import shortcuts
from django.conf import settings

from . import forms

@sensitive_post_parameters()
@csrf_protect
@never_cache
def signup(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            # Login User
            return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = forms.UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})