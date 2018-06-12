from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from calculator.calculator import calculate_score
from core.models import Prediction


class Home(View):
    @staticmethod
    def _template_name():
        return 'home.html'

    def get(self, request):
        players_results = []

        for player_name in settings.PLAYERS_NAME:
            score = calculate_score(Prediction.objects.filter(_predictor=player_name))
            players_results.append({'name': player_name, 'score': score})

        return render(request, self._template_name(),
                      {'players_results': sorted(players_results, key=lambda result: -result['score'])})

