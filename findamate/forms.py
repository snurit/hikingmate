from django.forms import ModelForm
from findamate.models import Hike

# Hike form
class HikeForm(ModelForm):
    class Meta:
        model = Hike
        exclude = ['enrolled_hikers']
