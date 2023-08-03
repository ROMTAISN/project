from django.urls import path
from .views import AuthorList, AuthorDetail


urlpatterns = [
    path('', AuthorList.as_view()),
    path('<int:pk>', AuthorDetail.as_view()),
]
