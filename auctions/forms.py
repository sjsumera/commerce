from django import forms
from .models import Listing, Comment, Bid
"""
Citing this article on using models as forms. 
https://www.geeksforgeeks.org/django-modelform-create-form-from-models/
"""


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
