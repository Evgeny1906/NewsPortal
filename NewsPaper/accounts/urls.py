from django.urls import path
from .views import CustomSignUp, create_author, logout_view

urlpatterns = [
    path('signup', CustomSignUp.as_view(), name='signup'),
    path('create_author', create_author, name='create_author'),
    path('logout', logout_view, name='logout'),

]