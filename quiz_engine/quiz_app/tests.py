#django specific imports
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

#application specific imports
from .factories_tests import QuizModelFactory
from .factories_tests import MemberModelFactory
from .models import QuizModel
from .models import MemberModel
from .models import SentMessagesModel
from .models import ReceivedMessagesModel
from .models import SubmissionModel

# Create your tests here.

class TreasureHuntViewTest(TestCase):

	def setUp(self):
		#create the questions
		self.short_code = 22384

	def test_post_only(self):
		'''A test to check that only post requests are allowed from
		the callbackurl''' 
		response = self.client.get(reverse('treasure_hunt'))
		self.assertEqual(response.status_code, 405)
		post_data = {}
		post_data['from'] = '+254720106472'
		post_data['to']  = self.short_code
		post_data['text'] = 'Jaribu'
		post_data['linkId'] = 'link_id'
		post_data['date'] = timezone.now()
		post_data['id'] = '123456'
		response = self.client.post(reverse('treasure_hunt'), data = post_data)
		self.assertEqual(response.status_code, 200)

	def test_register_new_user(self):
		'''A test to check that a user sending the word 
		jaribu in a string is registered'''	
		question1 = QuizModelFactory()
		keyword = 'jaribu john'
		post_data = {}
		post_data['from'] = '+254720106472'
		post_data['to']  = self.short_code
		post_data['text'] = 'Jaribu John'
		post_data['linkId'] = 'link_id'
		post_data['date'] = timezone.now()
		post_data['id'] = '123456'
		#emulate a message from Africas Talking API
		response = self.client.post(reverse('treasure_hunt'), data = post_data)
		self.assertContains(response, "Success", status_code = 200)
		member = MemberModel.objects.get(phone_number = post_data['from'])
		self.assertEqual(member.name, 'John')
		self.assertEqual(member.quiz_count, 0)
		self.assertTrue(SentMessagesModel.objects.get(phone_number = post_data['from']))
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = post_data['from'], text = post_data['text']))


	def test_correct_answer(self):
		'''
		A test to check if the correct answer is submitted
		that the quiz count is updated and the next question is sent'''
		#questions
		question1 = QuizModelFactory()
		question2 = QuizModelFactory()
		#create a user on question 1
		phone_number = '+254720106472'
		user = MemberModelFactory(phone_number = phone_number, quiz_count = 1)
		#answer
		post_data = {}
		post_data['from'] = phone_number
		post_data['to']  = self.short_code
		post_data['text'] = "jaribu {0}".format(question1.answer)
		post_data['linkId'] = 'link_id'
		post_data['date'] = timezone.now()
		post_data['id'] = '123456'

		self.client.post(reverse('treasure_hunt'), post_data)
		#submission models
		self.assertTrue(SubmissionModel.objects.get(status = 'C', user = user,
			quiz = QuizModel.objects.get(pk =1)))
		#received models
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))

		self.assertEqual(MemberModel.objects.get(pk = user.pk).quiz_count, 2)
		#check message sent is for the second question
		self.assertTrue(SentMessagesModel.objects.get(message = question2.question, phone_number = phone_number))


	def test_wrong_answer(self):
		'''A test to check if the wrong answer is submitted that the same question is repeated and 
		quiz_count is not updated'''
		question1 = QuizModelFactory()
		#we shall use question one as a sample
		#create a user on question 1
		phone_number = '+254720106472'
		user = MemberModelFactory(phone_number = phone_number, quiz_count = 1)
		#answer
		post_data = {}
		post_data['from'] = phone_number
		post_data['to']  = self.short_code
		post_data['text'] = "jaribu wrong_answer"
		post_data['linkId'] = 'link_id'
		post_data['date'] = timezone.now()
		post_data['id'] = '123456'

		self.client.post(reverse('treasure_hunt'), post_data)
		#submission models
		self.assertTrue(SubmissionModel.objects.get(status = 'W', user = user,
	 													quiz = QuizModel.objects.get(pk =1)))
		#received models
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))
		self.assertEqual(MemberModel.objects.get(pk = user.pk).quiz_count, 1)
		#check message sent is for the second question
		message = "Wrong Answer. Try Again. {0}".format(question1.question)
		self.assertTrue(SentMessagesModel.objects.get(message = message, phone_number = phone_number))
	

	def test_last_question(self):
		'''A test to show that when the questions are
		completed the treasure hunt comes to an end'''

		'''A test to check if the wrong answer is submitted that the same question is repeated and 
		quiz_count is not updated'''

		question1 = QuizModelFactory()
		question2 = QuizModelFactory()
		question3 = QuizModelFactory()
		question4 = QuizModelFactory()
		question5 = QuizModelFactory()
		question6 = QuizModelFactory()
		question7 = QuizModelFactory()

		#we shall use question one as a sample
		#create a user on question 1
		phone_number = '+254720106472'
		user = MemberModelFactory(phone_number = phone_number, quiz_count = 7)
		#answer
		post_data = {}
		post_data['from'] = phone_number
		post_data['to']  = self.short_code
		post_data['text'] = "jaribu {0}".format(question7.answer)
		post_data['linkId'] = 'link_id'
		post_data['date'] = timezone.now()
		post_data['id'] = '123456'

		self.client.post(reverse('treasure_hunt'), post_data)
		#submission models
		self.assertTrue(SubmissionModel.objects.get(status = 'C', user = user,
	 								quiz = QuizModel.objects.get(pk =7)))
		#received models
		self.assertTrue(ReceivedMessagesModel.objects.get(phone_number = phone_number, text = post_data['text']))
		self.assertEqual(MemberModel.objects.get(pk = user.pk).quiz_count, 8)
		#check message sent is for the second question
		message = "Bravo. Here is the key to the treasure chest."
		self.assertTrue(SentMessagesModel.objects.get(message = message, phone_number = phone_number))









