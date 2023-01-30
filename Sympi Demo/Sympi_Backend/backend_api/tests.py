# TESTING MODELS ----------------------------------------------------
import unittest
from django.test import TestCase
from models import *

class OrganizerTestCase(TestCase):
    def setUp(self):
        Organizer.objects.create(full_name="Test User", email="test@example.com", password="testpassword", mobile_no="123456789", about_me="This is a test user.")
 
    def test_total_organizer_events(self):
        """Test total events for a organizer"""
        test_organizer = Organizer.objects.get(full_name="Test User")
        self.assertEqual(test_organizer.total_organizer_events(), 0)
 
    def test_total_organizer_sponsors(self):
        """Test total sponsors for a organizer"""
        test_organizer = Organizer.objects.get(full_name="Test User")
        self.assertEqual(test_organizer.total_organizer_sponsors(), 0)
 
    def test_total_organizer_participants(self):
        """Test total participants for a organizer"""
        test_organizer = Organizer.objects.get(full_name="Test User")
        self.assertEqual(test_organizer.total_organizer_participants(), 0)
 
if __name__ == '__main__':
    unittest.main()

# TESTING URLs ----------------------------------------------------
from django.urls import path
from . import views

class UrlPatternsTestCase(unittest.TestCase):
    def test_organizer_urls(self):
        self.assertEqual(path('', views.EventList.as_view(), name='event_list'), '/')
        self.assertEqual(path('organizer/', views.OrganizerList.as_view(), name='organizer_list'), '/organizer/')
        self.assertEqual(path('organizer/dashboard/<int:pk>/', views.OrganizerDashboard.as_view()), '/organizer/dashboard/<int:pk>/')
        self.assertEqual(path('organizer/<int:pk>/', views.OrganizerDetail.as_view()), '/organizer/<int:pk>/')
        self.assertEqual(path('organizer/change-password/<int:organizer_id>/', views.organizer_change_password), '/organizer/change-password/<int:organizer_id>/')
        self.assertEqual(path('organizer-login',views.organizer_login), '/organizer-login')
        self.assertEqual(path('popular-organizers/', views.OrganizerList.as_view()), '/popular-organizers/')
        self.assertEqual(path('verify-organizer/<int:organizer_id>/', views.verify_organizer_via_otp), '/verify-organizer/<int:organizer_id>/')
    
    def test_category_urls(self):
        self.assertEqual(path('category/', views.CategoryList.as_view()), '/category/')
    
    def test_event_urls(self):
        self.assertEqual(path('event/', views.EventList.as_view()), '/event/')
        self.assertEqual(path('popular-events/', views.EventRatingList.as_view()), '/popular-events/')
        self.assertEqual(path('search-event/<str:searchstring>', views.EventList.as_view()), '/search-event/<str:searchstring>')
        self.assertEqual(path('update-view/<int:event_id>', views.update_view), '/update-view/<int:event_id>')
        self.assertEqual(path('event/<int:pk>/', views.EventDetailView.as_view()), '/event/<int:pk>/')
    
    def test_event_sponsors_urls(self):
        self.assertEqual(path('event-sponsors/<int:event_id>', views.EventSponsorList.as_view()), '/event-sponsors/<int:event_id>')
        self.assertEqual(path('sponsor/<int:pk>', views.SponsorDetailView.as_view()), '/sponsor/<int:pk>')
    
    def test_organizer_events_urls(self):
        self.assertEqual(path('organizer-events/<int:organizer_id>', views.OrganizerEventList.as_view()), '/organizer-events/<int:organizer_id>')
        self.assertEqual(path('organizer-event-detail/<int:pk>', views.OrganizerEventDetail.as_view()), '/organizer-event-detail/<int:pk>')
    
    def test_participant_testimonial_urls(self):
        self.assertEqual(path('participant-testimonial/', views.EventRatingList.as_view()), '/participant-testimonial/')
    
    def test_participant_urls(self):
        self.assertEqual(path('participant/', views.ParticipantList.as_view()), '/participant/')
        self.assertEqual(path('verify-participant/<int:participant_id>/', views.verify_participant_via_otp), '/verify-participant/<int:participant_id>/')
        self.assertEqual(path('organizer-forgot-password/', views.organizer_forgot_password), '/organizer-forgot-password/')
        self.assertEqual(path('organizer-change-password/<int:organizer_id>/', views.organizer_change_password), '/organizer-change-password/<int:organizer_id>/')
        self.assertEqual(path('user-forgot-password/', views.user_forgot_password), '/user-forgot-password/')
        self.assertEqual(path('user-change-password/<int:participant_id>/', views.user_change_password), '/user-change-password/<int:participant_id>/')
        self.assertEqual(path('participant/<int:pk>/', views.ParticipantDetail.as_view()), '/participant/<int:pk>/')
        self.assertEqual(path('participant/dashboard/<int:pk>/', views.ParticipantDashboard.as_view()), '/participant/dashboard/<int:pk>/')
        self.assertEqual(path('participant/change-password/<int:participant_id>/', views.participant_change_password), '/participant/change-password/<int:participant_id>/')
        self.assertEqual(path('participant-login',views.participant_login), '/participant-login')
        self.assertEqual(path('participant-enroll-event/', views.ParticipantEnrollEventList.as_view()), '/participant-enroll-event/')
        self.assertEqual(path('participant/fetch-all-notifications/<int:participant_id>/', views.NotificationList.as_view()), '/participant/fetch-all-notifications/<int:participant_id>/')
        self.assertEqual(path('save-notification/', views.NotificationList.as_view()), '/save-notification/')
    
    def test_quiz_urls(self):
        self.assertEqual(path('quiz/', views.QuizList.as_view()), '/quiz/')
        self.assertEqual(path('organizer-quiz/<int:organizer_id>', views.OrganizerQuizList.as_view()), '/organizer-quiz/<int:organizer_id>')
        self.assertEqual(path('organizer-quiz-detail/<int:pk>', views.OrganizerQuizDetail.as_view()), '/organizer-quiz-detail/<int:pk>')
        self.assertEqual(path('quiz/<int:pk>', views.QuizDetailView.as_view()), '/quiz/<int:pk>')
        self.assertEqual(path('quiz-questions/<int:quiz_id>', views.QuizQuestionList.as_view()), '/quiz-questions/<int:quiz_id>')
        self.assertEqual(path('quiz-questions/<int:quiz_id>/<int:limit>', views.QuizQuestionList.as_view()), '/quiz-questions/<int:quiz_id>/<int:limit>')
        self.assertEqual(path('fetch-quiz-assign-status/<int:quiz_id>/<int:event_id>',views.fetch_quiz_assign_status), '/fetch-quiz-assign-status/<int:quiz_id>/<int:event_id>')
        self.assertEqual(path('quiz-assign-event/', views.EventQuizList.as_view()), '/quiz-assign-event/')

# TESTING SERIALIZERS ----------------------------------------------------
from serializers import OrganizerSerializer

class TestOrganizerSerializer(TestCase):

	def setUp(self):
		self.organizer_serializer = OrganizerSerializer()

	def test_meta(self):
		self.assertEqual(self.organizer_serializer.Meta.model, models.Organizer)
		self.assertEqual(len(self.organizer_serializer.Meta.fields),13)
		self.assertEqual(self.organizer_serializer.Meta.depth, 0)
		
	def test_create(self):
		self.assertEqual(self.organizer_serializer.create(validate_data), instance)

if __name__ == '__main__':
	unittest.main()
        
# TESTING VIEWS ----------------------------------------------------
from unittest import mock
from unittest.mock import patch

from .views import StandardResultsSetPagination, OrganizerList, OrganizerDetail, OrganizerDashboard, organizer_login

@patch('backend_api.views.models.Organizer.objects.get')
@patch('backend_api.views.send_mail')
@patch('backend_api.views.randint')
class OrganizerLoginTestCase(TestCase):
    def setUp(self):
        self.organizerData = mock.Mock()
        self.organizerData.verify_status = True
        self.organizerData.login_via_otp = True
        self.organizerData.id = 1
        self.organizerData.otp_digit = 123456

    def test_organizer_login_success(self, randint_mock, send_mail_mock, get_mock):
        randint_mock.return_value = 123456
        get_mock.return_value = self.organizerData

        response = organizer_login(mock.Mock(POST={'email': 'test@example.com', 'password': 'test'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'bool': True, 'organizer_id': 1, 'login_via_otp': True})
        self.assertTrue(randint_mock.called)
        self.assertTrue(send_mail_mock.called)
        self.assertTrue(get_mock.called)
        self.assertEqual(self.organizerData.otp_digit, 123456)

    def test_organizer_login_failed_not_verified(self, randint_mock, send_mail_mock, get_mock):
        self.organizerData.verify_status = False
        get_mock.return_value = self.organizerData

        response = organizer_login(mock.Mock(POST={'email': 'test@example.com', 'password': 'test'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'bool': False, 'msg': 'Account is not verified!!'})
        self.assertFalse(randint_mock.called)
        self.assertFalse(send_mail_mock.called)
        self.assertTrue(get_mock.called)
        self.assertEqual(self.organizerData.otp_digit, None)

    def test_organizer_login_failed_invalid_credentials(self, randint_mock, send_mail_mock, get_mock):
        get_mock.side_effect = models.Organizer.DoesNotExist()

        response = organizer_login(mock.Mock(POST={'email': 'test@example.com', 'password': 'test'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'bool': False, 'msg': 'Invalid Email Or Password!!!!'})
        self.assertFalse(randint_mock.called)
        self.assertFalse(send_mail_mock.called)
        self.assertTrue(get_mock.called)

class StandardResultsSetPaginationTestCase(TestCase):
    def setUp(self):
        self.paginator = StandardResultsSetPagination()

    def test_page_size_value(self):
        self.assertEqual(self.paginator.page_size, 8)

    def test_page_size_query_param(self):
        self.assertEqual(self.paginator.page_size_query_param, 'page_size')

    def test_max_page_size(self):
        self.assertEqual(self.paginator.max_page_size, 8)

class OrganizerListTestCase(TestCase):
    def setUp(self):
        self.view = OrganizerList()

    def test_queryset_value(self):
        self.assertEqual(self.view.queryset.all().count(), 0)

    def test_serializer_class_value(self):
        self.assertEqual(self.view.serializer_class, OrganizerSerializer)

class OrganizerDetailTestCase(TestCase):
    def setUp(self):
        self.view = OrganizerDetail()

    def test_queryset_value(self):
        self.assertEqual(self.view.queryset.all().count(), 0)

    def test_serializer_class_value(self):
        self.assertEqual(self.view.serializer_class, OrganizerSerializer)

class OrganizerDashboardTestCase(TestCase):
    def setUp(self):
        self.view = OrganizerDashboard()

    def test_queryset_value(self):
        self.assertEqual(self.view.queryset.all().count(), 0)

    def test_serializer_class_value(self):
        self.assertEqual(self.view.serializer_class, OrganizerDashboardSerializer)