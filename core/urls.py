from django.conf.urls import url

from core.views.predictions import PredictionView
from core.views.home import Home

urlpatterns = [
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^zona-de-grupos/$', PredictionView.as_view(), name='group_zone_games'),
]