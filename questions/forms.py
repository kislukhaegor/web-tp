from django import forms

from question.models import Question

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PassswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '!' in username:
            raise forms.ValidationError('without !')
        return username

    def clean_Tag(self):
        tags_str = self.cleanned_data.get('tags')
        return [tag.strip() for tag in tags_str.split('.')]


class QuestionForm(forms.ModelForm):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'long'})

        class Meta:
            model = Question
            exclude = 'is_active'
