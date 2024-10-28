from games.models import PurchaseHistory


def create_purchase(user, game):
    purchase = PurchaseHistory(user=user, game=game, price_at_purchase=game.price)
    purchase.save()
    return purchase
