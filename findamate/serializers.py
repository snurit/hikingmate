from django.contrib.auth.models import Group
from findamate.models import User, Hike, Flare, Enrollment
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('gender', 'first_name', 'last_name', 'city', 'avatar')

class HikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hike
        fields = ('type', 'title', 'mate_min', 'mate_max', 'difficulty', 'date', 'date_margin', 'enrolled_hikers')

class FlareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flare
        fields = ('longitude', 'latitude', 'date_start', 'date_end', 'radius', 'hiker')

class EnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('hike', 'hiker', 'hike_rating', 'leader_rating', 'invite_accepted', 'enrollment_date')
