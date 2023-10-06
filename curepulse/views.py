from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
import json
from .forms import *
from .classes.class_user_auth import UserAuth
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .CurePulse.DataLoader.ResultsLoader import MongoDBLoader

DATA_LOADER = MongoDBLoader()

class LogInPage(TemplateView):
    template_name = "login.html"

    def post(self, request, **kwargs):
        User = UserAuth.authenticateUser(request)
        if User:
            if request.user.is_authenticated:
                print("User is authenticated")
            return redirect('/ratings')
        else:
            messages.error(request, "Incorrect username or password.")
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LogOutUser(TemplateView):
    template_name = "login.html"

    def get(self, request, **kwargs):
        UserAuth.logoutuser(request)
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterUser(TemplateView):
    template_name = "register.html"

    def post(self, request, **kwargs):
        User = UserAuth.registerUser(request)
        if User:
            return redirect('login')
        else:
            messages.error(request, "Username is not avialable.")
            return redirect('mam_register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['toggle'] = False
        context['data'] = True
        return context
    
    def post(self, request, **kwargs):
        form  = ScoreForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            score = form.cleaned_data['score']
            score_dict = {
                '1': 'Agent_Accent_Score',
                '2': 'Agent_Tone_Scores',
                '3': 'Agent_Text_Scores',
                '4': 'Client_Tone_Scores',
                '5': 'Client_Text_Scores'
            }

            try:
                date = date.strftime('%Y-%m-%d')
                data = json.dumps(DATA_LOADER.get_data(date, score_dict[score]))
                return render(request, 'index.html', {'json_data': data, 'toggle': False, 'data' : False, 'type': score != '1'})
            except:
                return render(request, 'index.html', {'toggle': True})
        return HttpResponse("Invalid Form")
    
class DataPoint(TemplateView):
    template_name = "datapoint.html"
    
    def get(self, request, **kwargs):
        data_param = request.GET.get('data')
        if data_param:
            data = json.loads(data_param)
            call_id = data.get('ID')
            data = DATA_LOADER.get_data_point(call_id)
            return render(request, 'datapoint.html', {'data': data})
        return HttpResponse("Invalid Request")