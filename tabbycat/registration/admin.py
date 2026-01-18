from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType

from utils.admin import ModelAdmin

from .models import Answer, Invitation, Question


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


class AnswerInline(GenericTabularInline):
    model = Answer
    fields = ('question', 'answer')
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(for_content_type=ContentType.objects.get_for_model(self.parent_model))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
