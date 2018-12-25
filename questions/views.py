from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from questions.models import *

from django.http import HttpResponseNotFound


def get_base_context():
    context = {}
    context['tags'] = Tag.objects.get_most_popular(8)
    context['members'] = User.objects.order_by('-rating')[:8]
    context['user'] = User.objects.all()[0]
    return context


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context().items())
        return context


class IndexView(ListView):
    template_name = "index.html"
    paginate_by = 10
    model = Question
    queryset = model.objects.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context().items())
        return context


class HotQuestionsView(ListView):
    template_name = "hot_questions.html"
    model = Question
    paginate_by = 20
    queryset = model.objects.get_most_hot()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context().items())
        return context



class TagView(ListView):
    template_name = "tags.html"
    model = Question
    paginate_by = 20

    def get_queryset(self):
        return self.model.by_tag.get(self.kwargs['tag_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context())
        return context


class QuestionView(ListView):
    template_name = "question.html"
    model = Question
    paginate_by = 20



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.model.objects.get_by_id(self.kwargs['question_id'])
        context['question'] = question
        queryset = question.answers.all()[::-1]
        context.update(get_base_context())
        return context


class SignInView(BaseView):
    template_name = "login.html"


class SignUpView(BaseView):
    template_name = "signup.html"


class SettingsView(BaseView):
    template_name = "settings.html"


class AskView(BaseView):
    template_name = "ask.html"

