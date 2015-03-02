#standard lib imports
import re

#django specific imports
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST

#application specific imports
from .models import ReceivedMessagesModel
from .models import MemberModel
from .models import QuizModel
from .models import SentMessagesModel
from quiz_engine.utility.functions import send_message

# Create your views here.
@require_POST
def treasure_hunt(request):
	'''
	The function that is executed when a request is sent from the callback url
	keyed in at the AfricasTalking API
	'''

	#get the post data sent
	phone_number = request.POST.get('from')
	short_code  = request.POST.get('to')
	text = request.POST.get('text')
	linkId = request.POST.get('linkId')
	time_received = request.POST.get('date')
	message_id = request.POST.get('id')

	#save to db
	ReceivedMessagesModel.objects.create(phone_number = phone_number, short_code = short_code,
										text = text, linkid = linkid, time_received = time_received, 
										message_id = message_id )

	#check if the word jaribu is in the message
	if 'jaribu' in text.lower():
		#check if number is already registered
		try:
			MemberModel.objects.get(phone_number = phone_number)

		except MemberModel.DoesNotExist:
			#get name
			name = re.sub('jaribu', '' ,text.lower()).replace(' ','').replace('.', '')
			name = name.title()
			#create the record
			member = MemberModel(phone_number = phone_number, name = name)
			member.save()
			try:
				quiz = QuizModel.objects.get(pk = 1)

				response = send_message(phone_number, quiz.question, short_code)
				member.quiz_count = 1
				member.save()
				#save the sent message
				SentMessagesModel.objects.create(short_code = short_code, status = response['status'], phone_number = response['number'],
													 message_id = response['messageId'], cost = response['cost'], message = quiz.question)
				break

			except QuizModel.DoesNotExist:
				print("The queried question deont exist.")

			
	else:
		#must be a solution to a question
		
		try:
			member = MemberModel.objects.get(phone_number = phone_number)
			#check the question the member is on
			current_question = member.quiz_count

		except MemberModel.DoesNotExist:
			print("Member doesnt exist")	

		#get the question and check if the submitted answer is correct
		try:
			quiz = QuizModel.objects.get(pk = current_question, answer__icontains = text)
			#increment to the next question
			member.quiz_count += 1
			member.save()
			if member.quiz_count <= QuizModel.objects.all().count():
				#send the next question
				quiz = QuizModel.objects.get(pk = member.quiz_count)
				response = send_message(phone_number, quiz.question, short_code)
				#log the message
				SentMessagesModel.objects.create(short_code = short_code, status = response['status'], phone_number = response['number'],
													 message_id = response['messageId'], cost = response['cost'], message = quiz.question)
		except QuizModel.DoesNotExist:
			quiz = QuizModel.objects.get(pk = current_question)
			message = "Wrong Answer. Try Again. {0}".format(quiz.question)
			response = send_message(phone_number, message, short_code)
			SentMessagesModel.objects.create(short_code = short_code, status = response['status'], phone_number = response['number'],
													 message_id = response['messageId'], cost = response['cost'], message = message)
			print("The queried question doesn't exist")		

					

	return HttpResponse('Success')


