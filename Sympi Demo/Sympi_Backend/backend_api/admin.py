from django.contrib import admin
from . import models

admin.site.register(models.Organizer)
admin.site.register(models.EventCategory)
admin.site.register(models.Event)
admin.site.register(models.Sponsor)
admin.site.register(models.Participant)
admin.site.register(models.ParticipantEventEnrollment)
admin.site.register(models.EventRating)
admin.site.register(models.ParticipantFavoriteEvent)
admin.site.register(models.ParticipantAssignment)

class NotificationAdmin(admin.ModelAdmin):
    list_display=['id','notif_subject', 'notif_for', 'notifiread_status']
admin.site.register(models.Notification,NotificationAdmin)

admin.site.register(models.Quiz)
admin.site.register(models.QuizQuestions)
admin.site.register(models.EventQuiz)
admin.site.register(models.AttempQuiz)
admin.site.register(models.ScientificMaterial)

admin.site.register(models.FAQ)