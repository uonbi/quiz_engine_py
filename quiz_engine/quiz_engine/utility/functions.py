# Import the helper gateway class
from .AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

#django specific imports
from django.conf import settings

#application specific imports


def send_message(phone_number, message, short_code):
	'''A function to send messages using Pythons AficasTalkingGateway'''

	username = settings.AFRICAS_TALKING['USERNAME']
	apikey   = settings.AFRICAS_TALKING['API_KEY']

	# Create a new instance of our awesome gateway class
	gateway = AfricasTalkingGateway(username, apikey)

	# Any gateway errors will be captured by our custom Exception class below, 
	# so wrap the call in a try-catch block
	try:
    	# Thats it, hit send and we'll take care of the rest. 
    	recipient = gateway.sendMessage(phone_number, message, short_code)
    	return recipient
        	# recipient['number']
         #   	recipient['status'],
        	# recipient['messageId'],
        	# recipient['cost'])
	except AfricasTalkingGatewayException, e:
    	print('Encountered an error while sending: {0}'.format(str(e)))
