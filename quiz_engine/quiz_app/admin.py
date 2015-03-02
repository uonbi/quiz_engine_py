from django.contrib import admin


#application specific imports
from .models import QuizModel
from .models import MemberModel
from .models import SubmissionModel
from .models import SentMessagesModel
from .models import ReceivedMessagesModel

# Register your models here.

admin.site.register(QuizModel)
admin.site.register(MemberModel)
admin.site.register(SubmissionModel)
admin.site.register(SentMessagesModel)
admin.site.register(ReceivedMessagesModel)