from django.contrib import admin

from utils.admin import ModelAdmin

from .models import Answer, IndependentAdjudicatorApplication, Invitation, Question


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = ('question', 'answer', 'content_object')
    list_filter = ('question',)


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('name', 'tournament', 'for_content_type', 'answer_type')
    list_filter = ('tournament', 'for_content_type')


@admin.register(Invitation)
class InvitationAdmin(ModelAdmin):
    list_display = ('url_key', 'institution', 'team')


@admin.register(IndependentAdjudicatorApplication)
class IndependentAdjudicatorApplicationAdmin(ModelAdmin):
    list_display = ('adjudicator', 'adjudicator__tournament')
    list_filter = ('adjudicator__tournament',)
    search_fields = ('adjudicator__name', 'adjudicator__email')
