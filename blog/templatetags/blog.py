from atexit import register
# カスタムテンプレートを作成する

from urllib import parse
from django import template
from django.shortcuts import resolve_url
from django.utils.html import *
from django.db.models import Count
from blog.models import Category, Diary
from blog.forms import DiarySearchForm
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
import markdown
from markdownx.settings import (
    MARKDOWNX_MARKDOWN_EXTENSIONS,
    MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
)
from markdown.extensions import Extension

register = template.Library()


@register.simple_tag
def get_return_link(request):
    # 最新日記の一覧
    top_page = resolve_url('blog:list')
    # 全ページのURL
    referer = request.environ.get('HTTP_REFERER')

    if referer:

        # リファラがある場合、前回ページが自分のサイト内であれば、そこに戻す
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc:
            return referer

    return top_page


# カテゴリ一覧をすべてのページに配置するために、タグを作成する
@register.inclusion_tag('blog/includes/category_links.html')
def render_category_links():
    # annotateで日記数を表示
    return {
        'category_list': Category.objects.annotate(diary_count=Count('diary'))
    }


# 月別アーカイブの作成
@register.inclusion_tag('blog/includes/month_links.html')
def render_month_links():
    return {
        "dates": Diary.objects.published().dates("created_at", "month", order="DESC"),
    }


# 検索フォームタグ
@register.inclusion_tag('blog/includes/search_form.html')
def render_search_form(request):
    if hasattr(request, "form"):
        form = request.form
    else:
        form = DiarySearchForm(request.GET)

    return {"search_form": form}


# GETパラメータの一部を置き換えるタグ
@register.simple_tag
def url_replace(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


# マークダウンをhtmlに変換する
@register.filter
def markdown_to_html(text):
    return mark_safe(markdownify(text))


class EscapeHtml(Extension):
    def extendMarkdown(self, md) -> None:
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')
