from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

from .models import User, Listing, Comment, Bid, Wlist, ClosedListing


def index(request):
    # basic information are being requested from the database and displayed to a user.
    cc=ClosedListing.objects.filter(owner=request.user.username)
    ctotal=len(cc)
    items=[]
    wbid=ClosedListing.objects.filter(winner=request.user.username)
    for w in wbid:
        items.append(w)
    wtcount=len(items)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    items=Listing.objects.all()
    
    return render(request, "auctions/index.html", {"items":items,"wattotal":wattotal, "wtotal":wtcount, "ctotal":ctotal})

def add_watchlist(request, pk):
    if request.user.username:
        # Assign Wlist (Watch List Table) to watchlist variable, save two unique details which are a username and a listind primary key.
        watchlist=Wlist()
        watchlist.owner=request.user.username
        watchlist.listid=pk
        watchlist.save()
        return redirect('listpage', pk=pk)
    else:
        return redirect('index')
def remove_watchlist(request, pk):
    if request.user.username:
        # Get a column from the databse where owner is the current user and listid is the pk of the current listing, then delete.
        try:
            watchlist=Wlist.objects.get(owner=request.user.username, listid=pk)
            watchlist.delete()
            return redirect('listpage', pk=pk)
        except:
            return redirect('listpage', pk=pk)
    else:
        return redirect('index')

def watchlist(request, username):
    ################### These repeated variables and code are for the sake of the notifation. So that no matter where the user is on the site, they will always see their current status.################################
    cc=ClosedListing.objects.filter(owner=request.user.username)
    ctotal=len(cc)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    ites=[]
    wbid=ClosedListing.objects.filter(winner=username)
    for w in wbid:
        ites.append(w)
    wtcount=len(ites)
    ##########################################################
    if request.user.username:
        # Get details associated with user from watchlist table and store them in a list var.
        wat=Wlist.objects.filter(owner=request.user.username)
        items=[]
        for i in wat:
            items.append(Listing.objects.filter(pk=i.listid))
        return render(request, "auctions/watchlist.html", {"items":items, "wtotal":wtcount, "wattotal":wattotal, "ctotal":ctotal})



def listpage(request, pk):
    cc=ClosedListing.objects.filter(owner=request.user.username)
    ctotal=len(cc)
    ites=[]
    wbid=ClosedListing.objects.filter(winner=request.user.username)
    for w in wbid:
        ites.append(w)
    wtcount=len(ites)
    comment=Comment.objects.all()
    comtt=comment.filter(listid=pk)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    added=None
    owner=None
    bidder=None
    username=request.user.username
    
    try:
        cl=ClosedListing.objects.get(winner=request.user.username, listid=pk)
        return render(request, "auctions/woninactive.html", {"item":cl, "wtotal":wtcount, "wattotal":wattotal, "ctotal":ctotal})
    except:
        pass
    
    try:
        item=Listing.objects.get(pk=pk)
        
           
    except:
         return redirect('wonpage', username, pk)

    
    try:
        if Wlist.objects.get(owner=request.user.username, listid=pk):
            added=True
        else:
            added=False
    except:
        pass
    try:
        if Listing.objects.get(owner=request.user.username, pk=pk):
            owner=True
        else:
            owner=False
    except:
        pass
    try:
        if Bid.objects.get(listid=pk, bidder=request.user.username):
            bidder=True
        else:
            bidder=False
    except:
        pass
    if request.method=='POST':
            comt = Comment()
            comt.comment=request.POST['comment']
            comt.commenter=request.user.username
            time=datetime.now()
            comt.time=time.strftime("%Y-%m-%d %H:%M:%S")
            comt.listid=pk
            comt.save()
            return redirect('listpage', pk=pk)
    else:
        return render(request, "auctions/listpage.html",{
            "item":item,
            "comments":comtt,
            "wattotal":wattotal,
            "added":added,
            "owner":owner,
            "failed":request.COOKIES.get('failed'),
            "success":request.COOKIES.get('success'),
            "bidder":bidder,
            "wtotal":wtcount,
            "ctotal":ctotal

        })

def bid(request, pk):
    bid=Listing.objects.get(pk=pk)
    c_bid=float(bid.price)
    if request.method=='POST':
        bid=float(request.POST['bid'])
        if bid > c_bid:
            i_list=Listing.objects.get(pk=pk)
            i_list.price=bid
            i_list.save()
            try:
                if Bid.objects.filter(pk=pk):
                    b=Bid.Objects.filter(pk=pk)
                    b.delete()
                bt=Bid()
                bt.listid=pk
                bt.bidder=request.user.username
                bt.bid=bid
                bt.save()
            except:
                bt=Bid()
                bt.bid=bid
                bt.bidder=request.user.username
                bt.listid=pk
                bt.save()
            response=redirect('listpage', pk=pk)
            response.set_cookie('success', 'Your bid was successfull!', max_age=3)
            return response
        else:
            response=redirect('listpage', pk=pk)
            response.set_cookie('failed', 'Sorry, your bid must be higher than current bid or price.', max_age=3)
            return response
    else:
        return redirect('index')

def closelisting(request, pk):
    now=datetime.now()
    pnow=now.strftime("%Y-%m-%d %H:%M:%S")
    #first of all move details from the listing table to closedlisting table for future usage
    
    try:

        if Listing.objects.get(pk=pk):
            listin=Listing.objects.get(pk=pk)
        else:
            pass
    except:
        pass
    try:

        bidd=Bid.objects.get(listid=pk, bid=listin.price)
    except:
        pass
    #listing=Wlist.objects.get(pk=pk)
    closedlisting=ClosedListing()
    closedlisting.title= listin.title
    closedlisting.owner=listin.owner
    try:
        closedlisting.winner=bidd.bidder
    except:
        pass
    if not closedlisting.winner:
        closedlisting.winner=listin.owner
    else:
        pass
    closedlisting.url=listin.url
    closedlisting.description=listin.description
    closedlisting.datecreated=listin.date
    closedlisting.dateclosed=pnow
    closedlisting.winprice=listin.price
    closedlisting.category=listin.category
    closedlisting.listid=listin.pk
    
    closedlisting.save()
    listin.delete()
    #check if listing details exists on watchlist table and then deeelleettee hahaha
    try:
        wat=Wlist.objects.filter(listid=pk)
        wat.delete()
    except:
        pass
    #delete list details if any exists on Bid table
    try:
        bidddd=Bid.objects.filter(listid=pk)
        bidddd.delete()
    except:
        pass
    #delete list details if any exists on Comment table
    try:
        comtt=Comment.objects.filter(listid=pk)
        comtt.delete()
    except:
        pass
    return redirect('index')
    
def won(request, username):
    cc=ClosedListing.objects.filter(owner=username)
    ctotal=len(cc)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    items=[]
    wbid=ClosedListing.objects.filter(winner=username)
    for w in wbid:
        items.append(w)
    wtcount=len(items)
    return render(request, "auctions/won.html", {"wtotal":wtcount, "items":items, "wattotal":wattotal, "ctotal":ctotal})

def wonpage(request, username, listid):
    cc=ClosedListing.objects.filter(owner=username)
    ctotal=len(cc)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    wb=ClosedListing.objects.filter(winner=request.user.username)
    wbt=len(wb)
    clist=ClosedListing.objects.get(listid=listid, winner=request.user.username)
    return render(request, "auctions/wonpage.html", {"item":clist, "wattotal":wattotal, "wtotal":wbt, "ctotal":ctotal})

def closed(request, username):
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    wb=ClosedListing.objects.filter(winner=request.user.username)
    wbt=len(wb)
    citems=[]
    cc=ClosedListing.objects.filter(owner=username)
    for c in cc:
        citems.append(c)
    ctotal=len(citems)
    return render(request, "auctions/closedlistpage.html", {"items":citems, "ctotal":ctotal, "wattotal":wattotal, "wtotal":wbt})

def clearclosed(request, username, listid):
    try:
        if ClosedListing.objects.get(listid=listid, owner=request.user.username):
            item=ClosedListing.objects.get(listid=listid, owner=request.user.username)
            item.delete()
        else:
            pass
    except:
        pass

    return redirect('closed', username)



def categories(request):
    cc=ClosedListing.objects.filter(owner=request.user.username)
    ctotal=len(cc)
    wbid=ClosedListing.objects.filter(winner=request.user.username)
    ii=[]
    for w in wbid:
        ii.append(w)
    wtcount=len(ii)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    listitem=Listing.objects.raw("SELECT * FROM auctions_listing GROUP by category")
    return render(request, "auctions/categorypage.html", {"listitem":listitem, "wtotal":wtcount, "wattotal":wattotal, "ctotal":ctotal})
def category(request, category):
    cc=ClosedListing.objects.filter(owner=username)
    ctotal=len(cc)
    wbid=ClosedListing.objects.filter(winner=request.user.username)
    ii=[]
    for w in wbid:
        ii.append(w)
    wtcount=len(ii)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    items=Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {"category":category, "items":items, "wtotal":wtcount, "wattotal":wattotal, "ctotal":ctotal})

        
    
def create(request):
    cc=ClosedListing.objects.filter(owner=request.user.username)
    ctotal=len(cc)
    wat=Wlist.objects.filter(owner=request.user.username)
    wattotal=len(wat)
    wb=ClosedListing.objects.filter(winner=request.user.username)
    wbt=len(wb)
    if request.method=="POST":
        owner=request.user.username
        time=datetime.now()
        dt=time.strftime("%Y-%m-%d %H:%M:%S")
        data=Listing()
        data.title=request.POST['title']
        data.description=request.POST['description']
        data.price=float(request.POST['price'])
        data.url=request.POST['url']
        data.category=request.POST['category']
        data.owner=owner
        data.date=dt
        data.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",{"wattotal":wattotal, "wtotal":wbt, "ctotal":ctotal})

    


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


        

