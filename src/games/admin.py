from django.contrib import admin

from games.models import CompletedGames, Game, PurchaseHistory, Review, Wishlist

admin.site.register([Game, Review, PurchaseHistory, Wishlist, CompletedGames])
