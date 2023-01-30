from rest_framework import serializers
from rest_framework.response import Response
from . import models
from django.contrib.flatpages.models import FlatPage
from django.core.mail import send_mail


class OrganizerSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Organizer
		fields=['id','full_name','email','password','mobile_no','otp_digit','login_via_otp','profile_img', 'about_me', 'organizer_events','total_organizer_events','facebook_url','linkedin_url','instagram_url','website_url']

	def __init__(self, *args, **kwargs):
		super(OrganizerSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 1

	def create(self, validate_data):
		email=self.validated_data['email']
		otp_digit=self.validated_data['otp_digit']
		instance = super(OrganizerSerializer, self).create(validate_data)
		send_mail(
			'Verify Account',
			'Please verify your account',
			'catarina85d@gmail.com',
			[email],
			fail_silently=False,
			html_message=f'<p>Your OTP is </p><p>{otp_digit}</p>'
		)
		return instance
		
		

class OrganizerDashboardSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Organizer
		fields=['total_organizer_events','total_organizer_participants','total_organizer_sponsors'] #'total_organizer_sponsors'

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model=models.EventCategory
		fields=['id','title','category_img','description','total_events']


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Event
		fields=[
			'id',
			'category',
			'organizer',
			'title',
			'date_start',
			'date_end',
			'description',
			'featured_img',
			#'techs',
			'event_sponsors',
			#'related_videos',
			#'tech_list',
			'total_enrolled_participants',
			'event_rating'
		]
	def __init__(self, *args, **kwargs):
		super(EventSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2


class SponsorSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Sponsor
		fields=['id','event','title','description','video','remarks']

	def __init__(self, *args, **kwargs):
		super(SponsorSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 1

class ParticipantSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Participant
		fields=['id','full_name','email','password','username','login_via_otp','login_via_otp','interested_categories','otp_digit','profile_img']
	
	def create(self, validate_data):
		email=self.validated_data['email']
		otp_digit=self.validated_data['otp_digit']
		instance = super(ParticipantSerializer, self).create(validate_data)
		send_mail(
			'Verify Account',
			'Please verify your account',
			'sympiplataform@gmail.com',
			[email],
			fail_silently=False,
			html_message=f'<p>Your OTP is </p><p>{otp_digit}</p>'
		)
		return instance

	def __init__(self, *args, **kwargs):
		super(ParticipantSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class ParticipantEventEnrollmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.ParticipantEventEnrollment
		fields=['id','event','participant','enrolled_time']
	def __init__(self, *args, **kwargs):
		super(ParticipantEventEnrollmentSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class ParticipantFavoriteEventSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.ParticipantFavoriteEvent
		fields=['id','event','participant','status']
	def __init__(self, *args, **kwargs):
		super(ParticipantFavoriteEventSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class EventRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.EventRating
		fields=['id','event','participant','rating','reviews','review_time']

	def __init__(self, *args, **kwargs):
		super(EventRatingSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2


class ParticipantAssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.ParticipantAssignment
		fields=[
			'id',
			'organizer',
			'participant',
			'title',
			'detail',
			'participant_status',
			'add_time'
		]
	def __init__(self, *args, **kwargs):
		super(ParticipantAssignmentSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class ParticipantDashboardSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Participant
		fields=['enrolled_events','favorite_events','complete_assignments','pending_assignments'] #'complete_assignments','pending_assignments'

class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Notification
		fields=['organizer','participant','notif_subject','notif_for']

	def __init__(self, *args, **kwargs):
		super(NotificationSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2


class QuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Quiz
		fields=[
			'id',
			'organizer',
			'title',
			'detail',
			'add_time',
		]
	def __init__(self, *args, **kwargs):
		super(QuizSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.QuizQuestions
		fields=['id','quiz','questions','ans1','ans2','ans3','ans4','right_ans']

	def __init__(self, *args, **kwargs):
		super(QuestionSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 1

class EventQuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.EventQuiz
		fields=['id','organizer','event','quiz','add_time']
	def __init__(self, *args, **kwargs):
		super(EventQuizSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class AttempQuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.AttempQuiz
		fields=['id','participant','quiz','question','right_ans','add_time']
	def __init__(self, *args, **kwargs):
		super(AttempQuizSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 2

class ScientificMaterialSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.ScientificMaterial
		fields=['id','event','title','description','upload','remarks']

	def __init__(self, *args, **kwargs):
		super(ScientificMaterialSerializer, self).__init__(*args, **kwargs)
		request = self.context.get('request')
		self.Meta.depth = 0
		if request and request.method == 'GET':
			self.Meta.depth = 1

class FaqSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.FAQ
		fields=['question','answer']

class FlatPagesSerializer(serializers.ModelSerializer):
	class Meta:
		model=FlatPage
		fields=['id','title','content','url']

class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Contact
		fields=['id','full_name','email','query_txt']

class OrganizerParticipantChatSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.OrganizerParticipantChat
		fields=['id','organizer','participant','msg_from','msg_text','msg_time']
		
	def to_representation(self, instance):
		representation = super(OrganizerParticipantChatSerializer, self).to_representation(instance)
		representation['msg_time'] = instance.msg_time.strftime("%Y-%m-%d %H:%M")
		return representation
