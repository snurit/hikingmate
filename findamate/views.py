# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.
from django.http import HttpResponse
from findamate.models import Hike
from findamate.models import Enrollment
from findamate.forms import HikeForm, SignUpForm

import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'findamate/index.html')

def path(request):
    return render(request, 'findamate/path.html')

# Hike form
def hike(request, hike_id=None):
    tmp_hike = Hike()
    if request.method == 'POST':
        # new object received : checking and saving
        logger.debug('In create')
        form = HikeForm(request.POST, instance=tmp_hike)
        hk = form.save()
        enr = Enrollment()
        enr.hiker = request.user
        enr.hike = hk
        enr.is_leader = True
        enr.save()
    elif hike_id is not None:
        # need to load object to populate the form
        logger.debug('In exists')
        try:
            tmp_hike = Hike.objects.get(pk=hike_id)
            form = HikeForm(instance=tmp_hike)
        except Hike.DoesNotExist:
            raise Http404("Hike does not exist")
    else:
        # new hike
        logger.debug('In new')
        form = HikeForm()
    return render(request, 'findamate/hike.html', {'hike': tmp_hike, 'form': form})

# Basic signup process
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'findamate/index.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Logout
def logout(request):
    logout(request)
    return render(request, 'findamate/index.html')
