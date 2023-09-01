from django.urls import path
from .views import (PostList, PostDetail, AuthorList, AuthorDetail, NewsList, ArticleList,
                    SearchList, NewsCreate, ArticleCreate, ArticleUpdate, ArticleDelete,
                    NewsUpdate, NewsDelete, upgrade_me, CategoryListView, subscribe)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('author/', AuthorList.as_view(), name='author_detail'),
    path('author/<int:pk>', AuthorDetail.as_view(), name='author_detail'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('article/', ArticleList.as_view(), name='article_list'),
    path('search/', SearchList.as_view(), name='search_list'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('article/create', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>',CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]

# path('upgrade', upgrade_user, name='account_upgrade'),