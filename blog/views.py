import os
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from django.views import View, generic
from django.shortcuts import get_object_or_404
from .models import Diary, Category
from django.db.models import Q
from .forms import DiarySearchForm
from django.conf import settings
from django.http.response import JsonResponse

# Create your views here.


class ArchiveListMixin:
    model = Diary
    paginate_by = 10
    date_field = 'created_at'
    template_name = 'blog/diary_list.html'
    allow_empty = True
    make_object_list = True


class DiaryList(ArchiveListMixin, generic.ArchiveIndexView):
    """
    日記の一覧
    """

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        # print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '最近の日記'
        # print(context)
        return context


class DiaryDetail(generic.DetailView):
    model = Diary

    def get_object(self, queryset=None):
        diary = super().get_object()
        if diary.created_at <= timezone.now():
            return diary
        return Http404


class DiaryCategoryList(ArchiveListMixin, generic.ArchiveIndexView):
    """
    カテゴリーの一覧
    """

    def get_queryset(self):
        self.category = category = get_object_or_404(
            Category, pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=category).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = f"「{self.category.name}」カテゴリの日記"
        return context


class DiaryYearList(ArchiveListMixin, generic.YearArchiveView):
    """
    年別のアーカイブリスト
    """

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = f"{self.kwargs['year']}年の日記"
        return context


class DiaryMonthList(ArchiveListMixin, generic.MonthArchiveView):
    """
    月別のアーカイブリスト
    """
    month_format = "%m"

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = f"{self.kwargs['year']}年{self.kwargs['month']}月の日記"
        return context


class DiarySearchList(ArchiveListMixin, generic.ArchiveIndexView):
    """
    検索結果の一覧を表示する
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        self.request.form = form = DiarySearchForm(self.request.GET)
        form.is_valid()
        self.key_word = key_word = form.cleaned_data["key_word"]
        if key_word:
            queryset = queryset.filter(
                Q(title__icontains=key_word) | Q(text__icontains=key_word))
        return queryset.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = f"「{self.key_word}」の検索結果"
        return context
