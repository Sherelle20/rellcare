from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('consultation/', consultation, name='consultation'),
    path('statistics/', statistics, name='statistics'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('ask/', ask, name='ask'),
    path('ask/q/<int:id>/', question, name='question'),
    path('ask/notanswered/', unanswered, name='question.unanswered'),
    path('ask/me/', me, name='ask.me'),
    path('ask/me/reponses', myReponses, name='ask.me.reponses'),
    path('us/', us, name='us'),
    path('logout/', logout, name='logout'),
]

