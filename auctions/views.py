from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category

class NewListing(forms.Form):
    title = forms.CharField(label="Title")
    desc = forms.CharField(label="Description")
    url = forms.CharField(label="Image url", required=False)
    price = forms.FloatField(min_value=0.01)
    category = forms.MultipleChoiceField(choices=zip(range(len(Category.objects.all())), Category.objects.all()), required=False)
    other_category = forms.CharField(label="Category (if not listed)", required=False)
    #lister from signed in user

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True), "heading": "Active Listings"
    })

def listing(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)
    #if no existing listing?

    bids = Bid.objects.filter(listing=current_listing)
    current_bid = None

    price = current_listing.price

    comments = Comment.objects.filter(listing=current_listing)

    close_msg = "Close auction"
    if not current_listing.active:
        close_msg = "Reopen auction"

    winner = False
    if bids:
        current_bid = max(bids, key=lambda k: k.bidding)
        price = current_bid.bidding
        if not current_listing.active and current_listing.lister != current_bid.user:
            winner = current_bid.user

    valid_bid = price + 0.01 

    watchlist_msg = "Watchlist"
    if request.user in User.objects.all() and current_listing in request.user.watchlist.all():
        watchlist_msg = "Remove from watchlist"
    return render(request, "auctions/listing.html", {
        "listing": current_listing, "bids": bids, "max_bid": current_bid, 
        "bid_count": len(bids), "valid_bid": valid_bid, "price": price,
        "watchlist_msg": watchlist_msg, "comments": comments, "close_msg": close_msg,
        "lister": current_listing.lister, "winner": winner, "categories": current_listing.category.all()
    })

def category(request, category_name):
    return render(request, "auctions/index.html", {
        "listings": Category.objects.get(category=category_name).listings.all()
    })


def settle(request, listing_id):
    
    current_listing = Listing.objects.get(pk=listing_id)
    if request.user != current_listing.lister:
        return login_view(request)
    
    current_listing.active = current_listing.active ^ True
    current_listing.save()
    return HttpResponseRedirect(reverse(listing, args=(listing_id,)))

def comment(request, listing_id):
    if request.user not in User.objects.all():
        return login_view(request) 
    if request.method == "POST":
        current_listing = Listing.objects.get(pk=listing_id)
        new_comment= Comment(comment=request.POST["comment"], listing=current_listing, commenter=request.user)
        new_comment.save()
        return HttpResponseRedirect(reverse(listing, args=(listing_id,)))

def watchlist(request):
    if request.user not in User.objects.all():
        return login_view(request)
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(), "heading": request.user.username + "'s watchlist"
    })

def follow(request, listing_id):
    if request.user not in User.objects.all():
        return login_view(request)
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        if request.user in listing.followers.all():
            request.user.watchlist.remove(listing)
        else:
            listing.followers.add(request.user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def bid(request, listing_id):
    if request.user not in User.objects.all():
        return login_view(request)
    if request.method == "POST":
        bidding_listing = Listing.objects.get(pk=listing_id)
        new_bid = Bid(listing=bidding_listing, user=request.user, bidding=float(request.POST["bid_price"]))
        new_bid.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def create(request):
    if request.user not in User.objects.all():
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        created_form = NewListing(request.POST)
        if created_form.is_valid():
            t = created_form.cleaned_data["title"]
            d = created_form.cleaned_data["desc"]
            u = created_form.cleaned_data["url"]
            p = created_form.cleaned_data["price"]
            other_category = created_form.cleaned_data["other_category"]

            new_listing = Listing(title=t, desc=d, url=u, lister=request.user, price=p)
            new_listing.save()
            for cat in created_form.cleaned_data["category"]:
                new_listing.category.add(Category.objects.all()[int(cat)])         
            if other_category:
                #create new category
                new_category = Category(category=other_category)
                new_category.save()
                #add new cat
                new_listing.category.add(new_category)
            return index(request)

    else:
        return render(request, "auctions/create.html", {
        "create_form": NewListing()
    })

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
