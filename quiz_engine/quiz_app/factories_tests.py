#Creates the models to be used on testing using factory_boy

#factory_boy imports
import factory
from factory.django import DjangoModelFactory


#application specific imports
from .models import QuizModel
from .models import MemberModel



#quizmodel factory
class QuizModelFactory(DjangoModelFactory):

	class Meta:
		model = QuizModel
		#django_get_or_create = ('question',)

	question = 	factory.Sequence(lambda n: 'question%d' % n)
	answer = factory.Sequence(lambda n: 'answer%d' % n)

class MemberModelFactory(DjangoModelFactory):

	class Meta:
		model = MemberModel
		#django_get_or_create = ('phone_number',)

	name = factory.Sequence(lambda n:'John Doe%d' % n)
	phone_number = factory.Sequence(lambda n: '+25472100000%d' % n)	
	quiz_count = 0	