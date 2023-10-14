from django.urls import path

from django.views.decorators.cache import cache_page

from .views import (PostList, PostDetail, AuthorList, AuthorDetail, NewsList, ArticleList,
                    SearchList, NewsCreate, ArticleCreate, ArticleUpdate, ArticleDelete,
                    NewsUpdate, NewsDelete, CategoryListView, subscribe, upgrade_me, add_comment)


urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('author/', AuthorList.as_view(), name='author_detail'),
    path('author/<int:pk>', AuthorDetail.as_view(), name='author'),
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
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('comment/<post_id>/', add_comment, name='add_comment'),
]

# path('upgrade', upgrade_user, name='account_upgrade'),
# path('addcomment/<post_id>/', addcomment, name='comment'),