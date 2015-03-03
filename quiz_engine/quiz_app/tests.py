#django specific imports
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utilis import timezone

#application specific imports
from .factories_tests import QuizModelFactory
from .factories_tests import MemberModelFactory
from .models import QuizModel
from .models import MemberModel
from .models import SentMessagesModel
from .models import ReceivedMessagesModel

# Create your tests here.

class TreasureHuntViewTest(TestCase):

	def setUp(self):
		#create the questions
		self.question1 = QuizModelFactory()
		self.question2 = QuizModelFactory()
		self.question3 = QuizModelFactory()
		self.question4 = QuizModelFactory()
		self.question5 = QuizModelFactory()
		self.question6 = QuizModelFactory()
		self.question7 = QuizModelFactory()
		self.short_code = '12345'

	def post_only_test(self):
		'''A test to check that only post requests are allowed from
		the callbackurl'''

		response = self.client.get(reverse('treasure_hunt'))
		self.assertEqual(response.status_code, 404)
		post_data = {}
		post_data['phone_number'] = '+254720111111'
		post_data['short_code']  = self.short_code
		post_data['text'] = 'Jaribu'
		post_data['linkId'] = 'link_id'
		post_data['time_received'] = timezone.now()
		post_data['message_id'] = '123456'
		response = self.client.post(reverse('treasure_hunt'), data = post_data)
		self.assertEqual(response.status_code, 200)

	def register_new_user_test(self):
		'''A test to check that a user sending the word 
		jaribu in a string is registered'''	

		keyword = 'jaribu john'
		post_data = {}
		post_data['phone_number'] = '+254720106472'
		post_data['short_code']  = self.short_code
		post_data['text'] = 'Jaribu'
		post_data['linkId'] = 'link_id'
		post_data['time_received'] = timezone.now()
		post_data['message_id'] = '123456'
		#emulate a message from Africas Talking API
		response = self.client.post(reverse('treasure_hunt'), data = post_data)
		self.assertContains(response, "Success", status_code = 200)
		member = Member.objects.get(phone_number = phone_number)
		self.assertEqual(member.name 'John')
		self.assertEqual(member.quiz_count, 1)
		self.assertTrue(SentMessagesModel.objects.get(pk = phone_number))
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))


	def correct_answer_test(self):
		'''
		A test to check if the correct answer is submitted
		that the quiz count is updated and the next question is sent'''

		#create a user on question 1
		phone_number = '+254720106472'
		user = MemberModelFactory(phone_number = phone_number, quiz_count = 1)
		#answer
		post_data = {}
		post_data['phone_number'] = phone_number
		post_data['short_code']  = self.short_code
		post_data['text'] = "jaribu {0}".format(self.question1.answer)
		post_data['linkId'] = 'link_id'
		post_data['time_received'] = timezone.now()
		post_data['message_id'] = '123456'

		self.client.post(reverse('treasure_hunt'), post_data)
		#submission models
		self.assertTrue(SubmissionModel.objects.get(status = 'C', phone_number = phone_number))
		#received models
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))
		self.assertEqual(MemberModel.objects.get(pk = user.pk), 2)
		#check message sent is for the second question
		self.assertTrue(SentMessagesModel.objects.get(message = self.question2.question, phone_number = phone_number))


	def wrong_answer_text(self):
		'''A test to check if the wrong answer is submitted that the same question is repeated and 
		quiz_count is not updated'''

		#we shall use question one as a sample
		#create a user on question 1
		phone_number = '+254720106472'
		user = MemberModelFactory(phone_number = phone_number, quiz_count = 1)
		#answer
		post_data = {}
		post_data['phone_number'] = phone_number
		post_data['short_code']  = self.short_code
		post_data['text'] = "jaribu wrong_answer"
		post_data['linkId'] = 'link_id'
		post_data['time_received'] = timezone.now()
		post_data['message_id'] = '123456'

		self.client.post(reverse('treasure_hunt'), post_data)
		#submission models
		self.assertTrue(SubmissionModel.objects.get(status = 'W', phone_number = phone_number))
		#received models
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))
		self.assertEqual(MemberModel.objects.get(pk = user.pk), 1)
		#check message sent is for the second question
		message = "Wrong Answer. Try Again. {0}".format(self.question1.question)
		self.assertTrue(SentMessagesModel.objects.get(message = message, phone_number = phone_number))
	

	def last_question_test(self):
		'''A test to show that when the questions are
		completed the treasure hunt comes to an end'''

		'''A test to check if the wrong answer is submitted that the same question is repeated and 
		quiz_count is not updated'''

		#we shall use question one as a sample
		#create a user on question 1
		phone_number = '+254720106472'
		user = MemberModelFactory(phone_number = phone_number, quiz_count = 7)
		#answer
		post_data = {}
		post_data['phone_number'] = phone_number
		post_data['short_code']  = self.short_code
		post_data['text'] = "jaribu {0}".format(self.question7.answer)
		post_data['linkId'] = 'link_id'
		post_data['time_received'] = timezone.now()
		post_data['message_id'] = '123456'

		self.client.post(reverse('treasure_hunt'), post_data)
		#submission models
		self.assertTrue(SubmissionModel.objects.get(status = 'C', phone_number = phone_number))
		#received models
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))
		self.assertEqual(MemberModel.objects.get(pk = user.pk), 8)
		#check message sent is for the second question
		message = "Bravo. Here is the key to the treasure chest."
		self.assertTrue(SentMessagesModel.objects.get(message = message, phone_number = phone_number))









