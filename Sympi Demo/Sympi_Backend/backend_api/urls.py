from django.urls import path
from . import views

urlpatterns = [
    # Organizer
    path('', views.EventList.as_view(), name='event_list'),
    path('organizer/', views.OrganizerList.as_view(), name='organizer_list'),
    path('organizer/dashboard/<int:pk>/', views.OrganizerDashboard.as_view()),
    path('organizer/<int:pk>/', views.OrganizerDetail.as_view()),
    path('organizer/change-password/<int:organizer_id>/', views.organizer_change_password),
    path('organizer-login',views.organizer_login),
    path('popular-organizers/', views.OrganizerList.as_view()),
    path('verify-organizer/<int:organizer_id>/', views.verify_organizer_via_otp),
    # Category
    path('category/', views.CategoryList.as_view()),
    # Event
    path('event/', views.EventList.as_view()),
    path('popular-events/', views.EventRatingList.as_view()),
    path('search-event/<str:searchstring>', views.EventList.as_view()),
    path('update-view/<int:event_id>', views.update_view),
    # Event Detail
    path('event/<int:pk>/', views.EventDetailView.as_view()),

    # Specific Event Sponsor
    path('event-sponsors/<int:event_id>', views.EventSponsorList.as_view()),
    # Specific Sponsor
    path('sponsor/<int:pk>', views.SponsorDetailView.as_view()),                                                        

    # Organizer Events
    path('organizer-events/<int:organizer_id>', views.OrganizerEventList.as_view()),
    # Event Detail
    path('organizer-event-detail/<int:pk>', views.OrganizerEventDetail.as_view()),

    # Participant Testimonial
    path('participant-testimonial/', views.EventRatingList.as_view()),

    # Participant
    path('participant/', views.ParticipantList.as_view()),
    path('verify-participant/<int:participant_id>/', views.verify_participant_via_otp),
    path('organizer-forgot-password/', views.organizer_forgot_password),
    path('organizer-change-password/<int:organizer_id>/', views.organizer_change_password),
    path('user-forgot-password/', views.user_forgot_password),
    path('user-change-password/<int:participant_id>/', views.user_change_password),
    path('participant/<int:pk>/', views.ParticipantDetail.as_view()),
    path('participant/dashboard/<int:pk>/', views.ParticipantDashboard.as_view()),
    path('participant/change-password/<int:participant_id>/', views.participant_change_password),
    path('participant-login',views.participant_login),
    path('participant-enroll-event/', views.ParticipantEnrollEventList.as_view()),
    path('fetch-enroll-status/<int:participant_id>/<int:event_id>',views.fetch_enroll_status),
    path('fetch-all-enrolled-participants/<int:organizer_id>', views.EnrolledParticipantList.as_view()),
    path('fetch-enrolled-participants/<int:event_id>', views.EnrolledParticipantList.as_view()),
    path('fetch-enrolled-events/<int:participant_id>', views.EnrolledParticipantList.as_view()),
    path('fetch-recommended-events/<int:participantId>', views.EventList.as_view()),
    path('event-rating/', views.EventRatingList.as_view()),
    path('fetch-rating-status/<int:participant_id>/<int:event_id>',views.fetch_rating_status),
    path('participant-add-favorite-event/', views.ParticipantFavoriteEventList.as_view()),
    path('participant-remove-favorite-event/<int:event_id>/<int:participant_id>', views.remove_favorite_event),
    path('fetch-favorite-status/<int:participant_id>/<int:event_id>',views.fetch_favorite_status),
    path('fetch-favorite-events/<int:participant_id>', views.ParticipantFavoriteEventList.as_view()),
    path('participant-assignment/<int:organizer_id>/<int:participant_id>', views.AssignmentList.as_view()),
    path('my-assignments/<int:participant_id>', views.MyAssignmentList.as_view()),
    path('update-assignment/<int:pk>', views.UpdateAssignment.as_view()),
    path('participant/fetch-all-notifications/<int:participant_id>/', views.NotificationList.as_view()),
    path('save-notification/', views.NotificationList.as_view()),

    # Quiz Start
    path('quiz/', views.QuizList.as_view()),
    path('organizer-quiz/<int:organizer_id>', views.OrganizerQuizList.as_view()),
    path('organizer-quiz-detail/<int:pk>', views.OrganizerQuizDetail.as_view()),
    path('quiz/<int:pk>', views.QuizDetailView.as_view()),
    path('quiz-questions/<int:quiz_id>', views.QuizQuestionList.as_view()),
    path('quiz-questions/<int:quiz_id>/<int:limit>', views.QuizQuestionList.as_view()),
    path('fetch-quiz-assign-status/<int:quiz_id>/<int:event_id>',views.fetch_quiz_assign_status),
    path('quiz-assign-event/', views.EventQuizList.as_view()),
    path('fetch-assigned-quiz/<int:event_id>', views.EventQuizList.as_view()),
    path('attempt-quiz/', views.AttemptQuizList.as_view()),
    path('attempted-quiz/<int:quiz_id>', views.AttemptQuizList.as_view()),
    path('fetch-quiz-result/<int:quiz_id>/<int:participant_id>', views.fetch_quiz_result),
    path('quiz-questions/<int:quiz_id>/next-question/<int:question_id>', views.QuizQuestionList.as_view()),
    path('fetch-quiz-attempt-status/<int:quiz_id>/<int:participant_id>',views.fetch_quiz_attempt_status),

    # Scientific Materials
    path('scientific-materials/<int:event_id>', views.ScientificMaterialList.as_view()),
    path('scientific-material/<int:pk>', views.ScientificMaterialDetailView.as_view()),
    path('user/scientific-materials/<int:event_id>', views.ScientificMaterialList.as_view()),
                                                                                          
    # FAQs
    path('faq/', views.FaqList.as_view()),

    path('pages/', views.FlatPagesList.as_view()),
    path('pages/<int:pk>/<str:page_slug>/', views.FlatPagesDetail.as_view()),

    path('contact/', views.ContactList.as_view()),

    path('send-message/<int:organizer_id>/<int:participant_id>', views.save_organizer_participant_msg),
    path('get-messages/<int:organizer_id>/<int:participant_id>', views.MessageList().as_view()),

    path('send-group-message/<int:organizer_id>', views.save_organizer_participant_group_msg),
    path('send-group-message-from-participant/<int:participant_id>', views.save_organizer_participant_group_msg_from_participant),

    path('fetch-my-organizers/<int:participant_id>', views.MyOrganizerList.as_view()),
]
