from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.

from django.views.generic import TemplateView, View
from django.shortcuts import render
from questions.models import *

from django.http import HttpResponseNotFound


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.get_most_popular(8)
        context['members'] = ["Il'ya Saneev", 'Adolf Hitler', 'Jesus Christ']
        context['user'] = User.objects.all()[0]
        return context


class PaginatedView(BaseView):
    objs_in_page = 20

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page') or 1
        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_page(self, objs):
        return Paginator(objs, self.objs_in_page).get_page(self.page)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class IndexView(PaginatedView):
    template_name = "index.html"
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.model.objects.all()
        context['questions'] = self.get_page(questions)
        return context

class HotQuestionsView(PaginatedView):
    template_name = "hot_questions.html"
    model = Question

    def get_context_data(self, **kwargs):
        questions = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context['questions'] = self.get_page(questions)
        return context

class TagView(PaginatedView):
    template_name = "tags.html"
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.model.by_tag.get(context['tag_name'])
        if not questions:
            raise HttpResponseNotFound

        context['questions'] = self.get_page(questions)
        return context

class QuestionView(PaginatedView):
    template_name = "question.html"
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            question = self.model.objects.filter(id=context['question_id'])[0]
        except IndexError:
            raise HttpResponseNotFound
        context['answers'] = self.get_page(question.answers.all())
        context['question'] = question
        return context


class SignInView(BaseView):
    template_name = "login.html"


class SignUpView(BaseView):
    template_name = "signup.html"


class SettingsView(BaseView):
    template_name = "settings.html"


class AskView(BaseView):
    template_name = "ask.html"

