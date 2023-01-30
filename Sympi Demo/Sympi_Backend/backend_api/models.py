from django.db import models
from django.core import serializers
import moviepy.editor

from django.core.mail import send_mail
import requests

# Organizer Model

 
class Organizer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    profile_img = models.ImageField(
        upload_to='organizer_profile_imgs/', null=True)
    about_me = models.TextField()
    verify_status = models.BooleanField(default=False)
    otp_digit = models.CharField(max_length=10, null=True)
    login_via_otp = models.BooleanField(default=False)

    facebook_url = models.URLField(null=True)
    linkedin_url = models.URLField(null=True)
    instagram_url = models.URLField(null=True)
    website_url = models.URLField(null=True)

    class Meta:
        verbose_name_plural = "1. Organizers"

    # def skill_list(self):
    # skill_list=self.skills.split(',')
    # return skill_list

    # Total Organizer Events
    def total_organizer_events(self):
        total_events = Event.objects.filter(organizer=self).count()
        return total_events

    # Total Organizer Sponsors
    def total_organizer_sponsors(self):
        total_sponsors = Sponsor.objects.filter(event__organizer=self).count()
        return total_sponsors

    # Total Organizer Participants
    def total_organizer_participants(self):
        total_participants = ParticipantEventEnrollment.objects.filter(
            event__organizer=self).count()
        return total_participants

# Event Category Model


class EventCategory(models.Model):
    title = models.CharField(max_length=150)
    category_img = models.ImageField(
        upload_to='event_category_imgs/', null=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "2. Event Categories"

    # Total event of this category
    def total_events(self):
        return Event.objects.filter(category=self).count()

    def __str__(self):
        return self.title

# Event Model


class Event(models.Model):
    category = models.ForeignKey(
        EventCategory, on_delete=models.CASCADE, related_name='category_events')
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name='organizer_events')
    title = models.CharField(max_length=150)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    description = models.TextField()
    featured_img = models.ImageField(upload_to='event_imgs/', null=True)
    event_views = models.BigIntegerField(default=0)

    class Meta:
        verbose_name_plural = "3. Events"

    #def related_videos(self):
    #    related_videos = Event.objects.filter(
    #        techs__icontains=self.techs).exclude(id=self.id)
    #    return serializers.serialize('json', related_videos)

    def total_enrolled_participants(self):
        total_enrolled_participants = ParticipantEventEnrollment.objects.filter(
            event=self).count()
        return total_enrolled_participants

    def event_rating(self):
        event_rating = EventRating.objects.filter(
            event=self).aggregate(avg_rating=models.Avg('rating'))
        return event_rating['avg_rating']

    def __str__(self):
        return self.title

# Sponsor Model


class Sponsor(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_sponsors')
    title = models.CharField(max_length=150)
    description = models.TextField()
    video = models.FileField(upload_to='sponsor_videos/', null=True)
    remarks = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "4. Sponsors"

# Participant Model


class Participant(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=200)
    interested_categories = models.TextField()
    profile_img = models.ImageField(
        upload_to='participant_profile_imgs/', null=True)
    verify_status = models.BooleanField(default=False)
    otp_digit = models.CharField(max_length=10, null=True)
    login_via_otp = models.BooleanField(default=False)

    facebook_url = models.URLField(null=True)
    linkedin_url = models.URLField(null=True)
    instagram_url = models.URLField(null=True)
    website_url = models.URLField(null=True)

    def __str__(self):
        return self.full_name

    # Total Enrolled Events
    def enrolled_events(self):
        enrolled_events = ParticipantEventEnrollment.objects.filter(
            participant=self).count()
        return enrolled_events

    # Total Favorite Events
    def favorite_events(self):
        favorite_events = ParticipantFavoriteEvent.objects.filter(
            participant=self).count()
        return favorite_events

    # Completed assignments
    def complete_assignments(self):
        complete_assignments = ParticipantAssignment.objects.filter(
            participant=self, participant_status=True).count()
        return complete_assignments

    # Pending assignments
    def pending_assignments(self):
        pending_assignments = ParticipantAssignment.objects.filter(
            participant=self, participant_status=False).count()
        return pending_assignments

    class Meta:
        verbose_name_plural = "5. Participants"

# Participant Event Enrollement


class ParticipantEventEnrollment(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='enrolled_events')
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name='enrolled_participant')
    enrolled_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "6. Enrolled Events"

    def __str__(self):
        return f"{self.event}-{self.participant}"


# Participant Favorite Event
class ParticipantFavoriteEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "7. Participant Favorite Events"

    def __str__(self):
        return f"{self.event}-{self.participant}"


# Event Rating and Reviews
class EventRating(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, null=True)
    rating = models.PositiveBigIntegerField(default=0)
    reviews = models.TextField(null=True)
    review_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event}-{self.participant}-{self.rating}"

    class Meta:
        verbose_name_plural = "8. Event Ratings"


# event Rating and Reviews
class ParticipantAssignment(models.Model):
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, null=True)
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True)
    participant_status = models.BooleanField(default=False, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "9. Participant Assignments"


# Notification Model
class Notification(models.Model):
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, null=True)
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, null=True)
    notif_subject = models.CharField(
        max_length=200, verbose_name='Notification Subject', null=True)
    notif_for = models.CharField(
        max_length=200, verbose_name='Notification For')
    notif_created_time = models.DateTimeField(auto_now_add=True)
    notifiread_status = models.BooleanField(
        default=False, verbose_name='Notification Status')

    class Meta:
        verbose_name_plural = "10. Notifications"

# Quiz Model


class Quiz(models.Model):
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    detail = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "11. Quiz"

# Quiz Questions Model


class QuizQuestions(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    questions = models.CharField(max_length=200)
    ans1 = models.CharField(max_length=200)
    ans2 = models.CharField(max_length=200)
    ans3 = models.CharField(max_length=200)
    ans4 = models.CharField(max_length=200)
    right_ans = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "12. Quiz Questions"

# Add Quiz to Event


class EventQuiz(models.Model):
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "13. Event Quiz"

# Atempt Quiz Question by Participant


class AttempQuiz(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(
        QuizQuestions, on_delete=models.CASCADE, null=True)
    right_ans = models.CharField(max_length=200, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "14. Attempted Questions"

# Scientific Material Model


class ScientificMaterial(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    upload = models.FileField(upload_to='scientific_materials/', null=True)
    remarks = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "15. Event Scientific Materials"

# FAQ Model


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name_plural = "16. FAQs"

# Contact Model
api_key = 'fcd70f25c0a2448780863f95cc549b60&email=sympiplataform@gmail.com'
api_url = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + api_key

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    query_txt = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.query_txt

    def save(self, *args, **kwargs):
        send_mail(
            'Contact Query',
            'Here is the message.',
            'sympiplataform@gmail.com',
            [self.email],
            fail_silently=False,
            html_message=f'<p>{self.full_name}</p><p>{self.query_txt}</p>'
        )
        return super(Contact, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "17. Contact Queries"


# Messages
class OrganizerParticipantChat(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    msg_text = models.TextField()
    msg_from = models.CharField(max_length=100)
    msg_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "18. Organizer Participant Messages"
