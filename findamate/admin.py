# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from findamate.models import User
from findamate.models import Point, Hike, Flare, Enrollment

# Register your models here.
admin.site.register(User)
admin.site.register(Point)
admin.site.register(Hike)
admin.site.register(Flare)
admin.site.register(Enrollment)
