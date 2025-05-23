from django.urls import path
from .views import (
    CategoryListCreate,
    CategoryRetrieveUpdateDestroy,
    AuctionListCreate,
    AuctionRetrieveUpdateDestroy,
    BidListCreate,
    BidRetrieveUpdateDestroy,
    UserAuctionListView,
    MyBidsView,   
    MyAuctionsView
)

app_name = "auctions"

urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),

    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),

    path('<int:auction_id>/bid/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),

    path('users/', UserAuctionListView.as_view(), name='auctions-from-user'),
    
    # RUTA IMPORTANTE:
    path('mybids/', MyBidsView.as_view(), name='my-bids'),
    
    path('users/misSubastas/', MyAuctionsView.as_view(), name='my-auctions'),
]
