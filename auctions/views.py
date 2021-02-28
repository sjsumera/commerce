from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment
from .forms import ListingForm, CommentForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new_listing(request):
    """
    View to handle displaying the new listing form and process saving the form.
    If form input is valid, process save and redirect user. Citing this article for how I
    associated the authenticated user with the form:
    https://www.geeksforgeeks.org/associate-user-to-its-upload-post-in-django/
    """
    form = ListingForm(request.POST or None)

    if form.is_valid():
        if float(form['starting_bid'].value()) > 0:
            object = form.save(commit=False)
            object.selling_user = request.user
            object.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", 
                          {"form": form, "message": "Starting bid must be greater than 0"})

    return render(request, "auctions/new_listing.html", {"form": form})


def item(request, item_id):
    """
    View to display individual items and allow users to add comments and bid. 
    Citation: https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist
    Queryset citation: https://stackoverflow.com/questions/42080864/set-in-django-for-a-queryset
    """
    item = Listing.objects.get(id=item_id)
    comments = item.comment_set.all()
    comment_form = CommentForm()
    bid_form = BidForm()
    message = ""

    # Add comment
    if request.POST.get("comment-btn"):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            object = comment_form.save(commit=False)
            object.post_author = request.user
            object.listing = item
            object.save()
            comment_form = CommentForm()

    # Add bid 
    if request.POST.get("bid-btn"):
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            if float(bid_form['bid'].value()) > item.starting_bid and float(bid_form['bid'].value()) > item.current_bid:
                object = bid_form.save(commit=False)
                object.listing = item
                object.bidding_user = request.user
                item.bidding_user = object.bidding_user
                item.current_bid = object.bid
                item.save()
                object.save()
                bid_form = BidForm()
            else: 
                message = "Bid must be higher than starting bid and current bid!"    
            
    return render(request, "auctions/items.html", {"item": item, "comments": comments, "comment_form": comment_form, "bid_form": bid_form, "message": message})

