from django.urls import include, path

from participants.models import Adjudicator, Coach, Speaker, Team, TournamentInstitution

from . import views
from .models import IndependentAdjudicatorApplication


urlpatterns = [
    path('institutions/', include([
        path('', views.InstitutionRegistrationTableView.as_view(), name='reg-institution-list'),
        path('questions/',
            views.CustomQuestionFormsetView.as_view(question_model=TournamentInstitution, success_url='reg-institution-list'),
            name='reg-institution-questions'),
        path('coaches/questions/',
            views.CustomQuestionFormsetView.as_view(question_model=Coach, success_url='reg-institution-list'),
            name='reg-coach-questions'),
    ])),
    path('teams/', include([
        path('', views.TeamRegistrationTableView.as_view(), name='reg-team-list'),
        path('<int:pk>/confirm/', views.ConfirmTeamRegistrationView.as_view(), name='reg-team-confirm'),
        path('questions/',
            views.CustomQuestionFormsetView.as_view(question_model=Team, success_url='reg-team-list'),
            name='reg-team-questions'),
    ])),
    path('adjudicators/', include([
        path('', views.AdjudicatorRegistrationTableView.as_view(), name='reg-adjudicator-list'),
        path('<int:pk>/confirm/', views.ConfirmAdjudicatorRegistrationView.as_view(), name='reg-adjudicator-confirm'),
        path('questions/',
            views.CustomQuestionFormsetView.as_view(question_model=Adjudicator, success_url='reg-adjudicator-list'),
            name='reg-adjudicator-questions'),
    ])),
    path('speakers/questions/',
        views.CustomQuestionFormsetView.as_view(question_model=Speaker, success_url='reg-team-list'),
        name='reg-speaker-questions'),
    path('independent-adjudicators/', include([
        path('', views.IndependentAdjudicatorApplicationTableView.as_view(), name='reg-independent-adj-list'),
        path('questions/',
            views.CustomQuestionFormsetView.as_view(
                question_model=IndependentAdjudicatorApplication,
                success_url='reg-independent-adj-list',
            ),
            name='reg-independent-adj-questions'),
    ])),
]
