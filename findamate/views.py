# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group

# Common Views import
from django.http import HttpResponse
from findamate.models import Hike, Enrollment, User, Flare
from findamate.forms import HikeForm, SignUpForm

# API import
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from findamate.serializers import UserSerializer, HikeSerializer, FlareSerializer, EnrollmentSerializer

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

# API VIEWS
@csrf_exempt
def api_user(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def api_user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

@csrf_exempt
def api_hike(request):
    if request.method == 'GET':
        hikes = Hike.objects.all()
        serializer = HikeSerializer(hikes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HikeSerializer(data=data)
        if serializer.is_valid():
            hike = serializer.save()
            # Creating the base enrollment
            enroll = Enrollment()
            enroll.hike = hike.id
            enroll.hiker = request.user
            enroll.is_leader = True
            enroll.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

csrf_exempt
def api_hike_detail(request, pk):
    try:
        hike = Hike.objects.get(pk=pk)
    except Hike.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HikeSerializer(hike)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HikeSerializer(hike, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        hike.delete()
        return HttpResponse(status=204)

@csrf_exempt
def api_enrollment(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EnrollmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def api_enrollment_detail(request, pk):
    try:
        enroll = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EnrollmentSerializer(enroll)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EnrollmentSerializer(enroll, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        enroll.delete()
        return HttpResponse(status=204)

# API VIEWS SETS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class HikeViewSet(viewsets.ModelViewSet):
    queryset = Hike.objects.all().order_by('first_name')
    serializer_class = HikeSerializer

class FlareViewSet(viewsets.ModelViewSet):
    queryset = Flare.objects.all().order_by('date_start')
    serializer_class = FlareSerializer
