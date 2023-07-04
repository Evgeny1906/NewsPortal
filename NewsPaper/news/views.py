from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from datetime import datetime
from .forms import PostForm
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
# Create your views here.


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'newses.html'
    context_object_name = 'newses'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        context['is_authent'] = self.request.user.is_authenticated
        return context



class NewsDeta(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_creating.html'

    def form_valid(self, form):
        """If the form is valid, firstly save with commit=False argument the associated model."""
        self.object = form.save(commit=False)
        self.object.postAuthor = self.request.user.author
        self.object.save()
        # возвращаем form_valid предка
        return super().form_valid(form)



class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'newses'
    ordering = 'postCategory'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_authent'] = self.request.user.is_authenticated
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        context['time_now'] = datetime.utcnow()
        return context


class ArticleList(ListView):
    model = Post
    ordering = 'postType'
    template_name = 'article.html'
    context_object_name = 'newses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        context['is_authent'] = self.request.user.is_authenticated
        context['time_now'] = datetime.utcnow()

        return context

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'article_creating.html'

    def form_valid(self, form):
        """If the form is valid, firstly save with commit=False argument the associated model."""
        self.object = form.save(commit=False)
        self.object.postType = 'AR'
        self.object.postAuthor = self.request.user.author
        self.object.save()
        # возвращаем form_valid предка
        return super().form_valid(form)
        # или формируем response самостоятельно
        # return HttpResponseRedirect(self.get_success_url())



# Представление удаляющее Post.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_search')
    context_object_name = 'news'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    template_name = 'news_update.html'
    form_class = PostForm


# @login_required
# @csrf_protect
# def subscriptions(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         category = Category.objects.get(id=category_id)
#         action = request.POST.get('action')

    #     if action == 'subscribe':
    #         Subscription.objects.create(user=request.user, category=category)
    #     elif action == 'unsubscribe':
    #         Subscription.objects.filter(
    #             user=request.user,
    #             category=category,
    #         ).delete()
    #
    # categories_with_subscriptions = Category.objects.annotate(
    #     user_subscribed=Exists(
    #         Subscription.objects.filter(
    #             user=request.user,
    #             category=OuterRef('pk'),
    #         )
    #     )
    # ).order_by('category')
    # return render(
    #     request,
    #     'subscriptions.html',
    #     {'categories': categories_with_subscriptions},
    # )


class Category_List_View(ListView):
    model = Post
    template_name = 'news/category_news.html'
    context_object_name = 'category_news'
    # ordering = ['-date_creation']
    paginate_by = 10
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        quoryset = Post.objects.filter(postCategory=self.category).order_by('-date_creation')
        return quoryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        subscrib = self.category.subscribers.filter(email=user.email)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context