from django.urls import path
from .views import SignUp, AccountUpdate, AccountDetail

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('account', AccountDetail.as_view(), name='account'),
    path('account/edit/', AccountUpdate.as_view(), name='account_update'),
]

# path('upgrade', upgrade_user, name='account_upgrade'),
