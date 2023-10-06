from django import forms

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ScoreForm(forms.Form):
    date = forms.DateField(label='Date', widget=forms.SelectDateWidget(years=range(2019, 2023)))
    score = forms.ChoiceField(label='Score', choices=[(1, 'Agent Accent Score'), (2, 'Agent Tone Score'), (3, 'Agent Text Score'), (4, 'Client Tone Score'), (5, 'Client Text Score')])