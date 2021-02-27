from django import forms
from .models import Listing
"""
Citing this article on using models as forms. 
https://www.geeksforgeeks.org/django-modelform-create-form-from-models/
"""


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        # fields = "__all__"
       # exclude = ['selling_user']
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']