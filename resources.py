from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from home.models import Player, ChooseTeamModel, TeamModel


class PlayerResource(resources.ModelResource):
    team = fields.Field(

        column_name='team',
        attribute='team',
        widget=ForeignKeyWidget(TeamModel, 'name')

    )

    class Meta:
        model = Player
        fields = (
            'id', 'name', 'age', 'position', 'team', 'price_value', 'ball_skills', 'passing', 'shooting', 'defence',
            'physical',
            'mental', 'goalkeeper', 'overall_avg')
        export_order = (
            'id', 'name', 'age', 'position', 'team', 'price_value', 'ball_skills', 'passing', 'shooting', 'defence',
            'physical',
            'mental', 'goalkeeper''overall_avg')


class TeamResource(resources.ModelResource):
    class Meta:
        model = TeamModel
        fields = ('id', 'name', 'manager')
        export_order = ('id', 'name', 'manager')
