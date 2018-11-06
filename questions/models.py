# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Sum

# Create your models here.


class User(AbstractUser):
    upload = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    nickname = models.CharField(max_length=40, verbose_name=u"Никнейм")

 
class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
 
    def likes(self):
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0
 

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
 
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
 
    vote = models.SmallIntegerField(verbose_name=u"Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name=u"Пользователь", on_delete=models.CASCADE)
 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
 
    objects = LikeDislikeManager()


class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_most_popular(self, count):
        return self.get_queryset().annotate(num_question=models.Count('questions')).order_by('-num_question')[:count]


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка")
    objects = TagManager()

    def __str__(self):
        return self.title


class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_answers(self):
        return 


class QuestionTagManager(QuestionManager):
    @staticmethod
    def get_tag_by_title(tag):
        return Tag.objects.filter(title=tag)

    def get(self, tag):
        tags = QuestionTagManager.get_tag_by_title(tag)
        return self.get_queryset().filter(tags__in=tags) if len(tags) else None


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    rating = models.IntegerField(default=0)
    votes = GenericRelation(LikeDislike, related_query_name='questions')
    objects = QuestionManager()
    by_tag = QuestionTagManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=120, verbose_name=u"Ответ на вопрос")
    is_correct = models.BooleanField(default=False, verbose_name=u"Корректность ответа")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность ответа")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания ответа")
    votes = GenericRelation(LikeDislike, related_query_name='asnwers')

    class Meta:
        ordering = ['-create_date']

