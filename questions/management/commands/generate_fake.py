from django.core.management.base import BaseCommand, CommandError
from questions.models import *
from faker import Faker
from random import randint, choice
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Generate fake data'

    def add_arguments(self, parser):
        parser.add_argument('-u', help='count of users',
                            action='store', type=int, dest='users', default=0)

        parser.add_argument('-t', help='count of tags',
                            action='store', type=int, dest='tags', default=0)

        parser.add_argument('-q', help='count of questions',
                            action='store', type=int, dest='questions', default=0)

        parser.add_argument('-l', help='count of likes',
                            action='store', type=int, dest='likes', default=0)


    def generate_tags(self, count):
        if not count:
            return

        tags = []
        tag_len = 0
        while tag_len != count:
            try:
                tags.append(Tag(title=self.fake.word().lower()))
            except:
                pass
            else:
                len += 1

        Tag.objects.bulk_create(tags, batch_size=100000)

    def generate_users(self, count):
        if not count:
            return

        users = []
        user_len = 0
        while user_len != count:
            try:
                username = self.fake.user_name()
                nickname = self.fake.name()
                email = self.fake.email()
                password = self.fake.password()
                rating = randint(-10, 1000)
                user = User(username=username,
                            nickname=nickname,
                            email=email,
                            password=password,
                            rating=rating)
                user.clean_fields()
                user.clean()
                user.validate_unique()
                user.full_clean()
            except Exception:
                pass
            else:
                users.append(user)
                user_len += 1


        User.objects.bulk_create(users, batch_size=10000)

    def generate_answers(self, question, count, users=None, tags=None):
        if not count:
            return

        answers = []
        asnwers_len = 0
        if not users:
            users = list(User.objects.all()[1:])
        if not tags:
            tags = list(Tag.objects.all())
        while answers_len != count:
            user = self.fake.random_element(users)
            text = self.fake.text(200)
            try:
                answer = Answer(author=user,
                                Question=question,
                                text=text)
                answer.clean_fields()
                answer.clean()
                answer.validate_unique()
                answer.full_clean()
            except Exception:
                pass
            else:
                answers.append(answer)
                answers_len += 1

        Answer.objects.bulk_create(answers, batch_size=10000)


    def generate_questions(self, count, users=None, tags=None):
        if not count:
            return

        questions = []
        question_len = 0
        if not users:
            users = list(User.objects.all()[1:])
        if not tags:
            tags = list(Tag.objects.all())
        while question_len != count:
            try:
                user =  self.fake.random_element(users)
                tags_to_add = self.fake.random_sample(tags, length=randint(1, min(len(tags), 3)))
                title = self.fake.text(30).rstrip()
                text = self.fake.text(200)
                q = Question(author=user,
                             title=title,
                             text=text)
                q.clean_fields()
                q.clean()
                q.validate_unique()
                q.full_clean()
                for tag in tags_to_add:
                    q.tags.add(tag)
            
                questions.append(q)
            except:
                pass
            else:
                question_len += 1
                self.generate_answers(q, randint(1, 40), users, tags)

        Question.objects.bulk_create(questions, batch_size=10000)


    def generate_likes(self, count, questions=None, users=None, answers=None):
        if not count:
            return

        likes = []
        likes_len = 0
        if not users:
            users = list(User.objects.all()[1:])
        if not questions:
            questions = list(Question.objects.all())
        if not answers:
            answers = list(Answer.objects.all())

        a_model_type = ContentType.objects.get_for_model(Answer)
        q_model_type = ContentType.objects.get_for_model(Question)
        while likes_len != count:
            try:
                user = self.fake.random_element(users)
                question = self.fake.random_element(questions)
                like = LikeDislike(content_type=q_model_type,
                                         object_id=question.id,
                                         user=user,
                                         vote=choice((1, -1)))
                like.clean_fields()
                like.clean()
                like.validate_unique()
                like.full_clean()
            except Exception:
                pass
            else:
                likes.append(like)
                likes_len += 1
            finally:
                random_answers = self.fake.random_sample(answers, randint(0, len(answers)))
                for answer in random_answers:
                    try:
                        l = LikeDislike(content_type=a_model_type,
                                                 object_id=answer.id,
                                                 user=user,
                                                 vote=choice((1, -1)))
                        l.clean_fields()
                        l.clean()
                        l.validate_unique()
                        l.full_clean()
                    except Exception:
                        pass
                    else:
                        likes.append(l)
                        likes_len += 1

        LikeDislike.bulk_create(likes)

    def handle(self, *args, **options):
        self.fake = Faker()
        self.generate_tags(options['tags'])
        print('tags')
        self.generate_users(options['users'])
        print('users')
        users = User.objects.all()[1:]
        tags = list(Tag.objects.all())
        self.generate_questions(options['questions'], users, tags)
        print('questions')
        questions = list(Question.objects.all())
        answers = list(Answer.objects.all())
        self.generate_likes(options['likes'])
        print('likes')
