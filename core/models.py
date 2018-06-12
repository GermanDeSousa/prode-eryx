from django.db import models


class Match(models.Model):
    _date = models.DateTimeField(max_length=255)
    _home_team = models.CharField(max_length=255)
    _visiting_team = models.CharField(max_length=255)
    _group = models.ForeignKey('Group', related_name='matches', on_delete=models.CASCADE)

    @classmethod
    def new_with(cls, date, home_team, visiting_team, group):
        match = cls(_date=date, _home_team=home_team, _visiting_team=visiting_team, _group=group)
        match.full_clean()
        match.save()

        return match

    def date(self):
        return self._date.strftime('%d/%m/%Y %H:%M')

    def home_team(self):
        return self._home_team

    def visiting_team(self):
        return self._visiting_team

    def group(self):
        return self._group


class Group(models.Model):
    ALL_GROUPS = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'))

    _group_name = models.CharField(choices=ALL_GROUPS, max_length=1)

    @classmethod
    def get_or_create(cls, group_name):
        try:
            return cls.objects.get(_group_name=group_name)
        except Group.DoesNotExist:
            group = cls(_group_name=group_name)

            group.full_clean()
            group.save()

            return group

    def group_name(self):
        return self._group_name


class Prediction(models.Model):
    _predictor = models.CharField(max_length=255)
    _home_team_goals = models.PositiveSmallIntegerField()
    _visiting_team_goals = models.PositiveSmallIntegerField()
    _match = models.ForeignKey('Match', related_name='predictions', on_delete=models.CASCADE)

    @classmethod
    def new_with(cls, predictor, home_team_goals, visiting_team_goals, match):
        prediction = cls(_predictor=predictor, _home_team_goals=home_team_goals,
                         _visiting_team_goals=visiting_team_goals, _match=match)

        prediction.full_clean()
        prediction.save()

    def predictor(self):
        return self._predictor

    def home_team_goals(self):
        return self._home_team_goals

    def visiting_team_goals(self):
        return self._visiting_team_goals

    def match(self):
        return self._match

    def is_draw(self):
        return self._home_team_goals == self._visiting_team_goals

    def winning_team(self):
        if self.is_draw():
            return None

        if self._visiting_team_goals > self._home_team_goals:
            return self.match().visiting_team()
        else:
            return self.match().home_team()
