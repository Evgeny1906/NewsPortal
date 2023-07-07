from django.urls import path
from .views import (NewsList, NewsDeta, NewsCreate, NewsSearch, ArticleList,
                    ArticleCreate, NewsDelete, NewsUpdate, Category_List_View, subscribe, unsubscribe)

urlpatterns = [

   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', NewsList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>', NewsDeta.as_view(), name='news_detail'),
   path('news/create/', NewsCreate.as_view()),
   path('news/search/', NewsSearch.as_view(), name='news_search'),
   path('news/delete/<int:pk>', NewsDelete.as_view(), name='news_delete'),
   path('news/edit/<int:pk>', NewsUpdate.as_view(), name='news_edit'),

   path('article/', ArticleList.as_view()),
   path('article/create', ArticleCreate.as_view()),
   path('article/edit/<int:pk>', NewsUpdate.as_view(), name='artikle_edit'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>', Category_List_View.as_view(), name='category_list'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]