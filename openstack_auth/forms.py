# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import forms as django_auth_forms
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from openstack_auth import exceptions
from openstack_auth import utils

import requests
import json

LOG = logging.getLogger(__name__)


class Login(django_auth_forms.AuthenticationForm):
    """Form used for logging in a user.

    Handles authentication with Keystone by providing the domain name, username
    and password. A scoped token is fetched after successful authentication.

    A domain name is required if authenticating with Keystone V3 running
    multi-domain configuration.

    If the user authenticated has a default project set, the token will be
    automatically scoped to their default project.

    If the user authenticated has no default project set, the authentication
    backend will try to scope to the projects returned from the user's assigned
    projects. The first successful project scoped will be returned.

    Inherits from the base ``django.contrib.auth.forms.AuthenticationForm``
    class for added security features.
    """
    use_required_attribute = False
    region = forms.ChoiceField(label=_("Region"), required=False)
    email = forms.EmailField(label=('Email Address'), required=True,
        widget=forms.EmailInput(attrs={"autofocus": "autofocus"}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        fields_ordering = ['email', 'password', 'region']

        self.fields['region'].choices = self.get_region_choices()
        if len(self.fields['region'].choices) == 1:
            self.fields['region'].initial = self.fields['region'].choices[0][0]
            self.fields['region'].widget = forms.widgets.HiddenInput()
        elif len(self.fields['region'].choices) > 1:
            self.fields['region'].initial = self.request.COOKIES.get(
                'login_region')

        self.fields = collections.OrderedDict(
            (key, self.fields[key]) for key in fields_ordering)

    @staticmethod
    def get_region_choices():
        default_region = (settings.OPENSTACK_KEYSTONE_URL, "Default Region")
        regions = getattr(settings, 'AVAILABLE_REGIONS', [])
        if not regions:
            regions = [default_region]
        return regions

    @sensitive_variables()
    def clean(self):
        default_domain = getattr(settings,
                                 'OPENSTACK_KEYSTONE_DEFAULT_DOMAIN',
                                 'Default')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        region = self.cleaned_data.get('region')

        payload = {'emailAddress': email}
        headers = {'Content-type': 'application/json'}
        response = requests.get(settings.DIAM_USER_URL, params=payload, headers=headers)

        if response.status_code == 404:
            self.add_error(None, "User does not exist. Please sign up.")
            return self.cleaned_data
        elif response.status_code != 200:
            self.add_error(None, "There was a problem logging in. Please try again")
            return self.cleaned_data

        domain = str(response.json().get('domainName'))
        try:
            self.user_cache = authenticate(request=self.request,
                                           username=email,
                                           password=password,
                                           user_domain_name=domain,
                                           auth_url=region)
            LOG.info('Login successful for user "%(username)s" using domain '
                     '"%(domain)s", remote address %(remote_ip)s.',
                     {'username': email, 'domain': domain,
                      'remote_ip': utils.get_client_ip(self.request)})
        except exceptions.KeystoneAuthException as exc:
            LOG.info('Login failed for user "%(username)s" using domain '
                     '"%(domain)s", remote address %(remote_ip)s.',
                     {'username': email, 'domain': domain,
                      'remote_ip': utils.get_client_ip(self.request)})
            raise forms.ValidationError(exc)
        if hasattr(self, 'check_for_test_cookie'):  # Dropped in django 1.7
            self.check_for_test_cookie()
        return self.cleaned_data
