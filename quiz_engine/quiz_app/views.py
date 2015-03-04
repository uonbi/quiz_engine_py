#standard lib imports
import re

#django specific imports
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

#application specific imports
from .models import ReceivedMessagesModel
from .models import MemberModel
from .models import QuizModel
from .models import SentMessagesModel
from .models import SubmissionModel
from quiz_engine.utility.functions import send_message

# Create your views here.
@require_POST
@csrf_exempt
def treasure_hunt(request):
	'''
	The function that is executed when a request is sent from the callback url
	keyed in at the AfricasTalking API
	'''

	keyword = 'jaribu' #Keyword assigned to us by AfricasTalking

	#get the post data sent
	phone_number = request.POST.get('from')
	short_code  = request.POST.get('to')
	text = request.POST.get('text')
	link_id = request.POST.get('linkId')
	time_received = request.POST.get('date')
	message_id = request.POST.get('id')

	#save to db
	ReceivedMessagesModel.objects.create(phone_number = phone_number, short_code = short_code,
										text = text, linkid = link_id, time_received = time_received, 
										message_id = message_id )

	#check if the word jaribu is in the message
	if keyword in text.lower():
		#check if number is already registered
		try:
			member = MemberModel.objects.get(phone_number = phone_number)
			current_question = member.quiz_count
			print('{0} {1}'.format(text, current_question))
			#get the question and check if the submitted answer is correct
			try:
				text_1 = re.sub(keyword, '' ,text.lower()).replace(' ','').replace('.', '')
				quiz = QuizModel.objects.get(pk = current_question, answer__icontains = text_1)
				#log the submission
				SubmissionModel.objects.create(user = member, quiz = quiz,
													answer = text, status = "C")
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
				else:
					# inform user challenge is over
					message = "Bravo. Here is the key to the treasure chest."
					response = send_message(phone_number, message, short_code)
					SentMessagesModel.objects.create(short_code = short_code, status = response['status'], phone_number = response['number'],
													 message_id = response['messageId'], cost = response['cost'], message = message)

			except QuizModel.DoesNotExist:
				#wrong answer
			
				quiz = QuizModel.objects.get(pk = current_question)
				#log the submission
				SubmissionModel.objects.create(user = member, quiz = quiz,
													answer = text, status = "W")
				message = "Wrong Answer. Try Again. {0}".format(quiz.question)
				response = send_message(phone_number, message, short_code)
				SentMessagesModel.objects.create(short_code = short_code, status = response['status'], phone_number = response['number'],
													 message_id = response['messageId'], cost = response['cost'], message = message)
				

		except MemberModel.DoesNotExist:
			#get name
			name = re.sub(keyword, '' ,text.lower()).replace(' ','').replace('.', '')
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

			except QuizModel.DoesNotExist:
				print("The queried question deont exist.")
			
	return HttpResponse('Success', status = 200)


