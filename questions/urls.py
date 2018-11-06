from django.urls import path, re_path
from questions.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='home_page'),
    path('hot/', HotQuestionsView.as_view(), name='hot_page'),
    path('tag/<str:tag_name>/', TagView.as_view(), name='tag_page'),
    path('login/', SignInView.as_view(), name='singin_page'),
    path('signup/', SignUpView.as_view(), name='signup_page'),
    path('settings/', SettingsView.as_view(), name='settings_page'),
    path('ask/', AskView.as_view(), name='ask_page'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question_page'),
]