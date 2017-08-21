# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from findamate.models import Hike
from findamate.forms import HikeForm

import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'findamate/index.html')

# Hike form
def hike(request, hike_id=None):
    tmp_hike = Hike()
    if request.method == 'POST':
        # new object received : checking and saving
        logger.debug('In create')
        form = HikeForm(request.POST, instance=tmp_hike)
        form.save()
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
