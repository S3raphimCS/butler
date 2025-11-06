from django.urls import path

from butler_core.api.v1.bot.views import BotWebHookView


urlpatterns = [
    path('webhook/', BotWebHookView.as_view()),
]