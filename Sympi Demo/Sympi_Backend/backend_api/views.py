from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q,Count,Avg,F
from django.contrib.flatpages.models import FlatPage
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail

from .serializers import OrganizerSerializer,CategorySerializer,EventSerializer,ParticipantSerializer,ParticipantEventEnrollmentSerializer,OrganizerDashboardSerializer,EventRatingSerializer,ParticipantFavoriteEventSerializer,ParticipantDashboardSerializer,NotificationSerializer,QuizSerializer,QuestionSerializer,EventQuizSerializer,AttempQuizSerializer,FaqSerializer,FlatPagesSerializer,ContactSerializer,OrganizerParticipantChatSerializer,SponsorSerializer,ScientificMaterialSerializer,ParticipantAssignmentSerializer 
from . import models

from random import randint


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 8

class OrganizerList(generics.ListCreateAPIView):
	queryset=models.Organizer.objects.all()
	serializer_class=OrganizerSerializer

	def get_queryset(self):
		if 'popular' in self.request.GET:
			sql="SELECT *,COUNT(c.id) as total_events FROM backend_api_organizer as t INNER JOIN backend_api_event as c ON c.organizer_id=t.id GROUP BY t.id ORDER BY total_events desc"
			return models.Organizer.objects.raw(sql)



class OrganizerDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Organizer.objects.all()
	serializer_class=OrganizerSerializer
	# permission_classes=[permissions.IsAuthenticated]

class OrganizerDashboard(generics.RetrieveAPIView):
	queryset=models.Organizer.objects.all()
	serializer_class=OrganizerDashboardSerializer




@csrf_exempt
def organizer_login(request):
	email=request.POST['email']
	password=request.POST['password']
	try:
		organizerData=models.Organizer.objects.get(email=email,password=password)
	except models.Organizer.DoesNotExist:
		organizerData=None
	if organizerData:
		if not organizerData.verify_status:
			return JsonResponse({'bool':False,'msg':'Account is not verified!!'})
		else:
			if organizerData.login_via_otp:
				# Send OTP Email
				otp_digit=randint(100000,999999)
				send_mail(
					'Verify Account',
					'Please verify your account',
					'catarina85d@gmail.com',
					[organizerData.email],
					fail_silently=False,
					html_message=f'<p>Your OTP is </p><p>{otp_digit}</p>'
				)
				organizerData.otp_digit=otp_digit
				organizerData.save()
				return JsonResponse({'bool':True,'organizer_id':organizerData.id,'login_via_otp':True})
			else:
				return JsonResponse({'bool':True,'organizer_id':organizerData.id,'login_via_otp':False})
	else:
		return JsonResponse({'bool':False,'msg':'Invalid Email Or Password!!!!'})

@csrf_exempt
def verify_organizer_via_otp(request,organizer_id):
	otp_digit=request.POST.get('otp_digit')
	verify=models.Organizer.objects.filter(id=organizer_id,otp_digit=otp_digit).first()
	if verify:
		models.Organizer.objects.filter(id=organizer_id,otp_digit=otp_digit).update(verify_status=True)
		return JsonResponse({'bool':True,'organizer_id':verify.id})
	else:
		return JsonResponse({'bool':False,'msg':'Please enter valid 6 digit OTP'})


class CategoryList(generics.ListCreateAPIView):
	queryset=models.EventCategory.objects.all()
	serializer_class=CategorySerializer

# Event
class EventList(generics.ListCreateAPIView):
	queryset = models.Event.objects.all()
	serializer_class = EventSerializer
	pagination_class=StandardResultsSetPagination

	def get_queryset(self):
		qs=super().get_queryset()
		if 'result' in self.request.GET:
			limit=int(self.request.GET['result'])
			qs=models.Event.objects.all().order_by('-id')[:limit]

		if 'category' in self.request.GET:
			category=self.request.GET['category']
			category=models.EventCategory.objects.filter(id=category).first()
			qs=models.Event.objects.filter(category=category)

		#if 'skill_name' in self.request.GET and 'organizer' in self.request.GET:
		#	skill_name=self.request.GET['skill_name']
		#	organizer=self.request.GET['organizer']
		#	organizer=models.Organizer.objects.filter(id=organizer).first()
		#	qs=models.Course.objects.filter(techs__icontains=skill_name,organizer=organizer)

		elif 'searchstring' in self.kwargs:
			search=self.kwargs['searchstring']
			if search:
				qs=models.Event.objects.filter(Q(title__icontains=search))


		#elif 'participantId' in self.kwargs:
		#	participant_id=self.kwargs['participantId']
		#	participant = models.Participant.objects.get(pk=participant_id)
		#	print(participant.interested_categories)
		#	queries = [Q(techs__iendswith=value) for value in participant.interested_categories]
		#	query = queries.pop()
		#	for item in queries:
		#		query |= item
		#	qs=models.Event.objects.filter(query)
		#	return qs

		return qs

class EventDetailView(generics.RetrieveAPIView):
	queryset=models.Event.objects.all()
	serializer_class=EventSerializer


# Specific Organizer Event
class OrganizerEventList(generics.ListCreateAPIView):
	serializer_class=EventSerializer

	def get_queryset(self):
		organizer_id = self.kwargs['organizer_id']
		organizer = models.Organizer.objects.get(pk=organizer_id)
		return models.Event.objects.filter(organizer=organizer)


# Specific Organizer Event
class OrganizerEventDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Event.objects.all()
	serializer_class=EventSerializer

# Event Sponsors
class EventSponsorList(generics.ListCreateAPIView):
	serializer_class = SponsorSerializer

	def get_queryset(self):
		event_id=self.kwargs['event_id']
		event = models.Event.objects.get(pk=event_id)
		return models.Sponsor.objects.filter(event=event)
	
class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Sponsor.objects.all()
	serializer_class = SponsorSerializer


# Participant Data
class ParticipantList(generics.ListCreateAPIView):
	queryset=models.Participant.objects.all()
	serializer_class=ParticipantSerializer

class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Participant.objects.all()
	serializer_class=ParticipantSerializer
	# permission_classes=[permissions.IsAuthenticated]

class ParticipantDashboard(generics.RetrieveAPIView):
	queryset=models.Participant.objects.all()
	serializer_class=ParticipantDashboardSerializer


@csrf_exempt
def participant_login(request):
	email=request.POST['email']
	password=request.POST['password']
	try:
		participantData=models.Participant.objects.get(email=email,password=password)
	except models.Participant.DoesNotExist:
		participantData=None
	if participantData:
		if not participantData.verify_status:
			return JsonResponse({'bool':False,'msg':'Account is not verified!!'})
		else:
			if participantData.login_via_otp:
				# Send OTP Email
				otp_digit=randint(100000,999999)
				send_mail(
					'Verify Account',
					'Please verify your account',
					'catarina85d@gmail.com',
					[participantData.email],
					fail_silently=False,
					html_message=f'<p>Your OTP is </p><p>{otp_digit}</p>'
				)
				participantData.otp_digit=otp_digit
				participantData.save()
				return JsonResponse({'bool':True,'participant_id':participantData.id,'login_via_otp':True})
			else:
				return JsonResponse({'bool':True,'participant_id':participantData.id,'login_via_otp':False})
	else:
		return JsonResponse({'bool':False,'msg':'Invalid Email Or Password!!!!'})

@csrf_exempt
def verify_participant_via_otp(request,participant_id):
	otp_digit=request.POST.get('otp_digit')
	verify=models.Participant.objects.filter(id=participant_id,otp_digit=otp_digit).first()
	if verify:
		models.Participant.objects.filter(id=participant_id,otp_digit=otp_digit).update(verify_status=True)
		return JsonResponse({'bool':True,'participant_id':verify.id})
	else:
		return JsonResponse({'bool':False})


class ParticipantEnrollEventList(generics.ListCreateAPIView):
	queryset=models.ParticipantEventEnrollment.objects.all()
	serializer_class=ParticipantEventEnrollmentSerializer

class ParticipantFavoriteEventList(generics.ListCreateAPIView):
	queryset=models.ParticipantFavoriteEvent.objects.all()
	serializer_class=ParticipantFavoriteEventSerializer

	def get_queryset(self):
		if 'participant_id' in self.kwargs:
			participant_id=self.kwargs['participant_id']
			participant = models.Participant.objects.get(pk=participant_id)
			return models.ParticipantFavoriteEvent.objects.filter(participant=participant).distinct()

def fetch_enroll_status(request,participant_id,event_id):
	participant=models.Participant.objects.filter(id=participant_id).first()
	event=models.Event.objects.filter(id=event_id).first()
	enrollStatus=models.ParticipantEventEnrollment.objects.filter(event=event,participant=participant).count()
	if enrollStatus:
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})

def fetch_favorite_status(request,participant_id,event_id):
	participant=models.Participant.objects.filter(id=participant_id).first()
	event=models.Event.objects.filter(id=event_id).first()
	favoriteStatus=models.ParticipantFavoriteEvent.objects.filter(event=event,participant=participant).first()
	if favoriteStatus and favoriteStatus.status == True:
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})

def remove_favorite_event(request,event_id,participant_id):
	participant=models.Participant.objects.filter(id=participant_id).first()
	event=models.Event.objects.filter(id=event_id).first()
	favoriteStatus=models.ParticipantFavoriteEvent.objects.filter(event=event,participant=participant).delete()
	if favoriteStatus:
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})


class EnrolledParticipantList(generics.ListAPIView):
	queryset=models.ParticipantEventEnrollment.objects.all()
	serializer_class=ParticipantEventEnrollmentSerializer

	def get_queryset(self):
		if 'event_id' in self.kwargs:
			event_id=self.kwargs['event_id']
			event = models.Event.objects.get(pk=event_id)
			return models.ParticipantEventEnrollment.objects.filter(event=event)
		elif 'organizer_id' in self.kwargs:
			organizer_id=self.kwargs['organizer_id']
			organizer = models.Organizer.objects.get(pk=organizer_id)
			return models.ParticipantEventEnrollment.objects.filter(event__organizer=organizer).distinct()
		elif 'participant_id' in self.kwargs:
			participant_id=self.kwargs['participant_id']
			participant = models.Participant.objects.get(pk=participant_id)
			return models.ParticipantEventEnrollment.objects.filter(participant=participant).distinct()

class MyOrganizerList(generics.ListAPIView):
	queryset=models.Event.objects.all()
	serializer_class=EventSerializer

	def get_queryset(self):
		if 'participant_id' in self.kwargs:
			participant_id=self.kwargs['participant_id']
			sql=f"SELECT * FROM backend_api_event as c,backend_api_participanteventenrollment as e,backend_api_organizer as t WHERE c.organizer_id=t.id AND e.event_id=c.id AND e.participant_id={participant_id} GROUP BY c.organizer_id"
			qs=models.Event.objects.raw(sql)
			print(qs)
			return qs

class EventRatingList(generics.ListCreateAPIView):
	queryset=models.EventRating.objects.all()
	serializer_class=EventRatingSerializer

	def get_queryset(self):
		if 'popular' in self.request.GET:
			sql="SELECT *,AVG(cr.rating) as avg_rating FROM backend_api_eventrating as cr INNER JOIN backend_api_event as c ON cr.event_id=c.id GROUP BY c.id ORDER BY avg_rating desc LIMIT 4"
			return models.EventRating.objects.raw(sql)
		if 'all' in self.request.GET:
			sql="SELECT *,AVG(cr.rating) as avg_rating FROM backend_api_eventrating as cr INNER JOIN backend_api_event as c ON cr.event_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
			return models.EventRating.objects.raw(sql)
		return models.EventRating.objects.filter(event__isnull=False).order_by('-rating')



def fetch_rating_status(request,participant_id,event_id):
	participant=models.Participant.objects.filter(id=participant_id).first()
	event=models.Event.objects.filter(id=event_id).first()
	ratingStatus=models.EventRating.objects.filter(event=event,participant=participant).count()
	if ratingStatus:
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})


@csrf_exempt
def organizer_change_password(request,organizer_id):
	password=request.POST['password']
	try:
		organizerData=models.Organizer.objects.get(id=organizer_id)
	except models.Organizer.DoesNotExist:
		organizerData=None
	if organizerData:
		models.Organizer.objects.filter(id=organizer_id).update(password=password)
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})



class AssignmentList(generics.ListCreateAPIView):
	queryset=models.ParticipantAssignment.objects.all()
	serializer_class=ParticipantAssignmentSerializer

	def get_queryset(self):
		participant_id=self.kwargs['participant_id']
		organizer_id=self.kwargs['organizer_id']
		participant = models.Participant.objects.get(pk=participant_id)
		organizer = models.Organizer.objects.get(pk=organizer_id)
		return models.ParticipantAssignment.objects.filter(participant=participant,organizer=organizer)


class MyAssignmentList(generics.ListCreateAPIView):
	queryset=models.ParticipantAssignment.objects.all()
	serializer_class=ParticipantAssignmentSerializer

	def get_queryset(self):
		participant_id=self.kwargs['participant_id']
		participant = models.Participant.objects.get(pk=participant_id)
		# Update Notifications
		models.Notification.objects.filter(participant=participant,notif_for='participant',notif_subject='assignment').update(notifiread_status=True)
		return models.ParticipantAssignment.objects.filter(participant=participant)

class UpdateAssignment(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.ParticipantAssignment.objects.all()
	serializer_class=ParticipantAssignmentSerializer

@csrf_exempt
def participant_change_password(request,participant_id):
	password=request.POST['password']
	try:
		participantData=models.Participant.objects.get(id=participant_id)
	except models.Organizer.DoesNotExist:
		participantData=None
	if participantData:
		models.Participant.objects.filter(id=participant_id).update(password=password)
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})


class NotificationList(generics.ListCreateAPIView):
	queryset=models.Notification.objects.all()
	serializer_class=NotificationSerializer

	def get_queryset(self):
		participant_id=self.kwargs['participant_id']
		participant = models.Participant.objects.get(pk=participant_id)
		return models.Notification.objects.filter(participant=participant,notif_for='participant',notif_subject='quiz',notifiread_status=False)

class QuizList(generics.ListCreateAPIView):
	queryset=models.Quiz.objects.all()
	serializer_class=QuizSerializer

# Specific Organizer Quiz
class OrganizerQuizList(generics.ListCreateAPIView):
	serializer_class=QuizSerializer

	def get_queryset(self):
		organizer_id = self.kwargs['organizer_id']
		organizer = models.Organizer.objects.get(pk=organizer_id)
		return models.Quiz.objects.filter(organizer=organizer)

class OrganizerQuizDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Quiz.objects.all()
	serializer_class=QuizSerializer

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Quiz.objects.all()
	serializer_class = QuizSerializer

class QuizQuestionList(generics.ListCreateAPIView):
	serializer_class = QuestionSerializer

	def get_queryset(self):
		quiz_id=self.kwargs['quiz_id']
		quiz = models.Quiz.objects.get(pk=quiz_id)
		if 'limit' in self.kwargs:
			return models.QuizQuestions.objects.filter(quiz=quiz).order_by('id')[:1]
		elif 'question_id' in self.kwargs:
			current_question=self.kwargs['question_id']
			return models.QuizQuestions.objects.filter(quiz=quiz,id__gt=current_question).order_by('id')[:1]
		else:
			return models.QuizQuestions.objects.filter(quiz=quiz)

class EventQuizList(generics.ListCreateAPIView):
	queryset=models.EventQuiz.objects.all()
	serializer_class=EventQuizSerializer

	def get_queryset(self):
		if 'event_id' in self.kwargs:
			event_id=self.kwargs['event_id']
			event = models.Event.objects.get(pk=event_id)
			return models.EventQuiz.objects.filter(event=event)

def fetch_quiz_assign_status(request,quiz_id,event_id):
	quiz=models.Quiz.objects.filter(id=quiz_id).first()
	event=models.Event.objects.filter(id=event_id).first()
	assignStatus=models.EventQuiz.objects.filter(event=event,quiz=quiz).count()
	if assignStatus:
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})

class AttemptQuizList(generics.ListCreateAPIView):
	queryset=models.AttempQuiz.objects.all()
	serializer_class=AttempQuizSerializer

	def get_queryset(self):
		if 'quiz_id' in self.kwargs:
			quiz_id=self.kwargs['quiz_id']
			quiz = models.Quiz.objects.get(pk=quiz_id)
			return models.AttempQuiz.objects.raw(f'SELECT * FROM backend_api_attempquiz WHERE quiz_id={int(quiz_id)} GROUP by participant_id')

def fetch_quiz_attempt_status(request,quiz_id,participant_id):
	quiz=models.Quiz.objects.filter(id=quiz_id).first()
	participant=models.Participant.objects.filter(id=participant_id).first()
	attemptStatus=models.AttempQuiz.objects.filter(participant=participant,question__quiz=quiz).count()
	print(models.AttempQuiz.objects.filter(participant=participant,question__quiz=quiz).query)
	if attemptStatus > 0:
		return JsonResponse({'bool':True})
	else:
		return JsonResponse({'bool':False})


def fetch_quiz_result(request,quiz_id,participant_id):
	quiz=models.Quiz.objects.filter(id=quiz_id).first()
	participant=models.Participant.objects.filter(id=participant_id).first()
	total_questions=models.QuizQuestions.objects.filter(quiz=quiz).count()
	total_attempted_questions=models.AttempQuiz.objects.filter(quiz=quiz,participant=participant).values('participant').count()
	attempted_questions=models.AttempQuiz.objects.filter(quiz=quiz,participant=participant)

	total_correct_questions=0
	for attempt in attempted_questions:
		if attempt.right_ans == attempt.question.right_ans:
			total_correct_questions+=1

	return JsonResponse({'total_questions':total_questions,'total_attempted_questions':total_attempted_questions,'total_correct_questions':total_correct_questions})


class ScientificMaterialList(generics.ListCreateAPIView):
	serializer_class = ScientificMaterialSerializer

	def get_queryset(self):
		event_id=self.kwargs['event_id']
		event = models.Event.objects.get(pk=event_id)
		return models.ScientificMaterial.objects.filter(event=event)

class ScientificMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.ScientificMaterial.objects.all()
	serializer_class = ScientificMaterialSerializer

def update_view(request,event_id):
	queryset=models.Event.objects.filter(pk=event_id).first()
	queryset.event_views+=1
	queryset.save()
	return JsonResponse({'views':queryset.event_views})


def fetch_participant_testimonial(request,quiz_id,participant_id):
	quiz=models.Quiz.objects.filter(id=quiz_id).first()
	participant=models.Participant.objects.filter(id=participant_id).first()
	total_questions=models.QuizQuestions.objects.filter(quiz=quiz).count()
	total_attempted_questions=models.AttempQuiz.objects.filter(quiz=quiz,participant=participant).values('participant').count()
	return JsonResponse({'total_questions':total_questions,'total_attempted_questions':total_attempted_questions})


class FaqList(generics.ListAPIView):
	queryset=models.FAQ.objects.all()
	serializer_class=FaqSerializer

class FlatPagesList(generics.ListAPIView):
	queryset=	FlatPage.objects.all()
	serializer_class=FlatPagesSerializer

class FlatPagesDetail(generics.RetrieveAPIView):
	queryset=	FlatPage.objects.all()
	serializer_class=FlatPagesSerializer

class ContactList(generics.ListCreateAPIView):
	queryset=models.Contact.objects.all()
	serializer_class=ContactSerializer


@csrf_exempt
def organizer_forgot_password(request):
	email=request.POST.get('email')
	verify=models.Organizer.objects.filter(email=email).first()
	if verify:
		link=f"http://localhost:3000/organizer-change-password/{verify.id}/"
		send_mail(
			'Verify Account',
			'Please verify your account',
			'catarina85d@gmail.com',
			[email],
			fail_silently=False,
			html_message=f'<p>Your OTP is </p><p>{link}</p>'
		)
		return JsonResponse({'bool':True,'msg':'Please check your email'})
	else:
		return JsonResponse({'bool':False,'msg':'Invalid Email!!'})

@csrf_exempt
def organizer_change_password(request,organizer_id):
	password=request.POST.get('password')
	verify=models.Organizer.objects.filter(id=organizer_id).first()
	if verify:
		models.Organizer.objects.filter(id=organizer_id).update(password=password)
		return JsonResponse({'bool':True,'msg':'Password has been changed'})
	else:
		return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})


@csrf_exempt
def user_forgot_password(request):
	email=request.POST.get('email')
	verify=models.Participant.objects.filter(email=email).first()
	if verify:
		link=f"http://localhost:3000/user-change-password/{verify.id}/"
		send_mail(
			'Verify Account',
			'Please verify your account',
			'catarina85d@gmail.com',
			[email],
			fail_silently=False,
			html_message=f'<p>Your OTP is </p><p>{link}</p>'
		)
		return JsonResponse({'bool':True,'msg':'Please check your email'})
	else:
		return JsonResponse({'bool':False,'msg':'Invalid Email!!'})

@csrf_exempt
def user_change_password(request,participant_id):
	password=request.POST.get('password')
	verify=models.Participant.objects.filter(id=participant_id).first()
	if verify:
		models.Participant.objects.filter(id=participant_id).update(password=password)
		return JsonResponse({'bool':True,'msg':'Password has been changed'})
	else:
		return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})


@csrf_exempt
def save_organizer_participant_msg(request,organizer_id,participant_id):
	organizer=models.Organizer.objects.get(id=organizer_id)
	participant=models.Participant.objects.get(id=participant_id)
	msg_text=request.POST.get('msg_text')
	msg_from=request.POST.get('msg_from')
	msgRes=models.OrganizerParticipantChat.objects.create(
		organizer=organizer,
		participant=participant,
		msg_text=msg_text,
		msg_from=msg_from,
	)
	if msgRes:
		msgs=models.OrganizerParticipantChat.objects.filter(organizer=organizer,participant=participant).count()
		return JsonResponse({'bool':True,'msg':'Message has been send','total_msg':msgs})
	else:
		return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})

class MessageList(generics.ListAPIView):
	queryset=models.OrganizerParticipantChat.objects.all()
	serializer_class=OrganizerParticipantChatSerializer

	def get_queryset(self):
		organizer_id=self.kwargs['organizer_id']
		participant_id=self.kwargs['participant_id']
		organizer = models.Organizer.objects.get(pk=organizer_id)
		participant = models.Participant.objects.get(pk=participant_id)
		return models.OrganizerParticipantChat.objects.filter(organizer=organizer,participant=participant).exclude(msg_text='')


@csrf_exempt
def save_organizer_participant_group_msg(request,organizer_id):
	organizer=models.Organizer.objects.get(id=organizer_id)
	msg_text=request.POST.get('msg_text')
	msg_from=request.POST.get('msg_from')

	enrolledList=models.ParticipantEventEnrollment.objects.filter(event__organizer=organizer).distinct()
	for enrolled in enrolledList:
		msgRes=models.OrganizerParticipantChat.objects.create(
			organizer=organizer,
			participant=enrolled.participant,
			msg_text=msg_text,
			msg_from=msg_from,
		)
	if msgRes:
		return JsonResponse({'bool':True,'msg':'Message has been send'})
	else:
		return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})

@csrf_exempt
def save_organizer_participant_group_msg_from_participant(request,participant_id):
	participant=models.Participant.objects.get(id=participant_id)
	msg_text=request.POST.get('msg_text')
	msg_from=request.POST.get('msg_from')

	sql=f"SELECT * FROM backend_api_event as c,backend_api_participanteventenrollment as e,backend_api_organizer as t WHERE c.organizer_id=t.id AND e.event_id=c.id AND e.participant_id={participant_id} GROUP BY c.organizer_id"
	qs=models.Event.objects.raw(sql)

	myEvents=qs
	for event in myEvents:
		msgRes=models.OrganizerParticipantChat.objects.create(
			organizer=event.organizer,
			participant=participant,
			msg_text=msg_text,
			msg_from=msg_from,
		)
	if msgRes:
		return JsonResponse({'bool':True,'msg':'Message has been send'})
	else:
		return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})