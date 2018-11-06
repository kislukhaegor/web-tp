from django.contrib import admin

from questions.models import User, Question, Tag, Answer, LikeDislike
from django.contrib.contenttypes.admin import GenericStackedInline


class UserAdmin(admin.ModelAdmin):
	fields = ['email', 'username', 'nickname', 'upload']


class LikeInlineAdmin(GenericStackedInline):
	model = LikeDislike


class AnswerInlineAdmin(admin.TabularInline):
	model = Answer


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    filter_horizontal = ('tags',)
    inlines = [AnswerInlineAdmin, LikeInlineAdmin]

admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag)
admin.site.register(Answer)
# Register your models here.
