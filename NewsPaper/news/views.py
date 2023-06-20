from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Author
from datetime import datetime
from .forms import PostForm
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
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
        # context['filterset'] = self.filterset
        return context



class NewsDeta(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_creating.html'




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
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    model = Post
    ordering = 'postType'
    template_name = 'article.html'
    context_object_name = 'newses'


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_creating.html'

    def form_valid(self, form):
        """If the form is valid, firstly save with commit=False argument the associated model."""
        self.object = form.save(commit=False)
        self.object.postType = 'AR'
        self.object.save()
        # возвращаем form_valid предка
        return super().form_valid(form)
        # или формируем response самостоятельно
        # return HttpResponseRedirect(self.get_success_url())



# Представление удаляющее Post.
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_search')
    context_object_name = 'news'


class NewsUpdate(UpdateView):
    model = Post
    template_name = 'news_update.html'
    form_class = PostForm


# class ArticleUpdate(UpdateView):
#     model = Post
#     template_name = 'news_update.html'
#     form_class = PostForm
