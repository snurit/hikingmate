# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import datetime

# Extended Django User class
class User(AbstractUser):
    """ Hiker model """
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_NOT_SPECIFIED = 'ND'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_NOT_SPECIFIED, 'Not specified'),
    )
    gender = models.CharField(max_length=16, blank=False, choices=GENDER_CHOICES, default=GENDER_NOT_SPECIFIED)
    birth_date = models.DateField(blank=True, null=True)
    adress = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=16)
    city = models.CharField(max_length=64)
    mobile_phone = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='upload/avatar/', blank=True, null=True)
    member_since = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    def __str__(self):
        return self.gender + ' ' + self.first_name + ' ' + self.last_name

# Abstract class localisable
class Localisable(models.Model):
    longitude = models.DecimalField(max_digits=8, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    class Meta:
        abstract = True

# Path class
class Point(Localisable):
    POINT_TYPE_START = 'S'
    POINT_TYPE_WAYPOINT = 'W'
    POINT_TYPE_BASE_CAMP = 'B'
    POINT_TYPE_FINISH = 'F'
    POINT_TYPE_CHOICES = (
        (POINT_TYPE_START, 'Start'),
        (POINT_TYPE_WAYPOINT, 'Waypoint'),
        (POINT_TYPE_BASE_CAMP, 'Base camp'),
        (POINT_TYPE_FINISH, 'Finish')
    )
    point_type = models.CharField(choices=POINT_TYPE_CHOICES, default=POINT_TYPE_WAYPOINT, max_length=16)
    comment = models.TextField(blank=True, null=True, max_length=1024)
    hike  = models.ForeignKey('Hike', on_delete=models.CASCADE)
    def __str__(self):
        return self.point_type + ' ' + self.hike.__str__()

# Class Hike
class Hike(models.Model):
    HIKE_TYPE_WALK = 'W'
    HIKE_TYPE_CLIMB = 'C'
    HIKE_TYPE_SKI = 'S'
    HIKE_TYPE_CHOICES = (
        (HIKE_TYPE_WALK, 'Walk'),
        (HIKE_TYPE_CLIMB, 'Climbing'),
        (HIKE_TYPE_SKI, 'Ski')
    )
    type = models.CharField(choices=HIKE_TYPE_CHOICES, default=HIKE_TYPE_WALK, max_length=16)
    title = models.CharField(blank=False, null=False, default='My hike', max_length=64)
    mate_min = models.PositiveSmallIntegerField(default=1)
    mate_max = models.PositiveSmallIntegerField(default=1)
    difficulty = models.PositiveSmallIntegerField()
    date = models.DateField()
    date_margin = models.PositiveSmallIntegerField(default=0)
    enrolled_hikers = models.ManyToManyField(
        User,
        through='Enrollment',
        through_fields=('hike', 'hiker'),
    )
    def __str__(self):
        return '(' + self.type + ') ' + self.title

# Class Flare
class Flare(Localisable):
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField()
    radius = models.PositiveSmallIntegerField(default=5)
    hiker = models.ForeignKey('User', on_delete=models.CASCADE)

# Class Enrollment
class Enrollment(models.Model):
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)
    hiker = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(blank=True, null=True, max_length=256)
    hike_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    leader_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    is_leader = models.BooleanField(default=False)
    invite_accepted = models.BooleanField(default=False)
    invite_date = models.DateField(auto_now_add=True)
    enrollment_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return str(self.hike) + ' by ' + str(self.hiker)
