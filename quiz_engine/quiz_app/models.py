from django.db import models



#fiels choices
ASSESSMENT = (
		('C','Correct'),
		('W','Wrong'),
	)

# Create your models here.

class MemberModel(models.Model):
	'''
	A model to store the user details
	'''

	name = models.CharField(max_length = 50, default = '')
	phone_number = models.CharField(max_length = 20, default = '')
	quiz_count = models.IntegerField(default = 0)

class QuizModel(models.Model):
	'''
	A model to store the question and answer
	'''

	question = models.CharField(max_length = 255, default = '')
	answer = models.CharField(max_length = 50, default = '')

class SubmissionModel(models.Model):
	'''
	All trials are stored here
	'''		
	user = models.ForeignKey(MemberModel)
	quiz = models.ForeignKey(QuizModel)
	submission_date = models.DateTimeField(auto_now_add = True)
	answer = models.CharField(max_length = 50, default = '')
	status = models.CharField(max_length = 10, choices = ASSESSMENT)

class SentMessagesModel(models.Model):
	'''
	Keep the sent messages for logging purposes
	'''

	phone_number = models.CharField(max_length = 20, default = '')
	short_code = models.CharField(max_length = 10, default = '' ,
		help_text = "The shortcode that is used to reply the message")
	status = models.CharField(max_length = 50, default = '',
		help_text = "Store the status of the sent message")
	message_id = models.CharField(max_length = 255, default = '')
	cost = models.FloatField(default = 0)

class ReceivedMessages(models.Model):
	'''
	A record of the messages received from AfricasTalking API...
	Kept for logging purposes
	'''

	phone_number = models.CharField(max_length = 20, default = '')
	short_code = models.CharField(max_length = 10, default = '')
	text = models.CharField(max_length = 255, default = '')
	linkid = models.CharField(max_length = 255, default = '')
	time_received = models.DateTimeField(help_text = 'The time the message was received at Africas Talking')
	message_id = models.CharField(max_length = 255, default = '')
















