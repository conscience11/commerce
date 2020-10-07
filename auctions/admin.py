from django.contrib import admin
from auctions.models import Listing, Comment, User,Bid,Wlist,ClosedListing
class ListingAdmin(admin.ModelAdmin):
    list_display=('id', 'owner', 'title', 'price', 'category')

class CommentAdmin(admin.ModelAdmin):
    list_display=('id', 'commenter', 'time', 'comment')
class BidAmin(admin.ModelAdmin):
    list_display=('bidder', 'bid', 'listid')

class WlistAdmin(admin.ModelAdmin):
    list_display=('owner', 'listid')
class ClosedListingAdmin(admin.ModelAdmin):
    list_display=('winner', 'owner', 'winprice', 'title', )

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
admin.site.register(Bid, BidAmin)
admin.site.register(Wlist, WlistAdmin)
admin.site.register(ClosedListing, ClosedListingAdmin)
