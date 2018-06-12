from django.shortcuts import render
from django.views.generic import View

from core.models import Match, Prediction


class PredictionView(View):
    @staticmethod
    def _template_name():
        return 'predictions.html'

    @staticmethod
    def _predictions_saved_template_name():
        return 'predictions_saved.html'

    def get(self, request):
            # aca esta el jugador, use it wisely
            player_name = request.GET['player']

            if Prediction.objects.filter(_predictor=player_name).exists():
                return render(request, self._predictions_saved_template_name())

            matches = Match.objects.all()

            group_zone_matches = {}
            for match in matches:
                group_name = match.group().group_name()
                if group_name in group_zone_matches:
                    group_zone_matches[group_name].append(match)
                else:
                    group_zone_matches[group_name] = [match]

            return render(request, self._template_name(),
                          {'group_zone_matches': sorted(group_zone_matches.items(), key=lambda item: item[0]),
                           'player_name': player_name})

    def post(self, request):
        player_name = request.GET['player']

        matches = Match.objects.all()
        for match in matches:
            user_prediction = request.POST.getlist(str(match.id))
            Prediction.new_with(predictor=player_name, home_team_goals=user_prediction[0],
                                visiting_team_goals=user_prediction[1], match=match)

        return render(request, self._predictions_saved_template_name())
