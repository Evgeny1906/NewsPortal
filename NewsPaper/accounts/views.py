from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import CustomSignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import logout

from news.models import Author


# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('/news/search')


@login_required
def create_author(request):
    user = request.user
    group = Group.objects.get(name='Authors')
    if not user.groups.filter(name='Authors').exists():
        group.user_set.add(user)
    Author.objects.create(authorUser=User.objects.get(pk=user.id))
    return redirect('/news/search')


class CustomSignUp(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/accounts/login'
    template_name = 'registration/login.html'



