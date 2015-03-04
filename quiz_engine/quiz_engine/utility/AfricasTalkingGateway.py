import urllib.request, urllib.parse, urllib.error
import json

class AfricasTalkingGatewayException(Exception):
    pass

class AfricasTalkingGateway:
    
    def __init__(self, username_, apiKey_):
        self.username = username_
        self.apiKey   = apiKey_
        self.SMSURLString   = "https://api.africastalking.com/version1/messaging"
        self.VoiceURLString = "https://voice.africastalking.com/call"

    def sendMessage(self, to_, message_, from_ = None, bulkSMSMode_ = 1, enqueue_ = 0, keyword_ = None, linkId_ = None):

        '''
        The optional from_ parameter should be populated with the value of a shortcode or alphanumeric that is 
        registered with us 

        The optional bulkSMSMode_ parameter will be used by the Mobile Service Provider to determine who gets billed for a 
        message sent using a Mobile-Terminated ShortCode. The default value is 1 (which means that 
        you, the sender, gets charged). This parameter will be ignored for messages sent using 
        alphanumerics or Mobile-Originated shortcodes.

        The optional enqueue_ parameter is useful when sending a lot of messages at once where speed is of the essence

        The optional keyword_ is used to specify which subscription product to use to send messages for premium rated short codes

        The optional linkId_ parameter is pecified when responding to an on-demand content request on a premium rated short code

        '''
	
        if len(to_) == 0 or len(message_) == 0:
            raise AfricasTalkingGatewayException("Please provide both to_ and message_ parameters")

        values = {'username' : self.username,
                    'to'       : to_,
                    'message'  : message_ }

        if not from_ is None :
            values["from"]        = from_
            values["bulkSMSMode"] = bulkSMSMode_

        if enqueue_ > 0:
            values["enqueue"] = enqueue_

        if not keyword_ is None:
            values["keyword"] = keyword_

        if not linkId_ is None:
            values["linkId"] = linkId_

        headers = {'Accept' : 'application/json',
                        'apikey' : self.apiKey }

        try:
            data = urllib.parse.urlencode(values)
            request  = urllib.request.Request(self.SMSURLString, data.encode('utf-8'), headers=headers)
            response = urllib.request.urlopen(request)
            the_page = response.read()

        except urllib.error.HTTPError as e:
            the_page = e.read()
            decoded  = json.loads(the_page.decode('utf-8'))
            raise AfricasTalkingGatewayException(decoded['SMSMessageData']['Message'])

        else:
            decoded  = json.loads(the_page.decode('utf-8'))
            recipients = decoded['SMSMessageData']['Recipients']
            return recipients
    
 #    def fetchMessages(self, lastReceivedId_):
	
	# url     = "%s?username=%s&lastReceivedId=%s" % (self.SMSURLString, self.username, lastReceivedId_)
	# headers = {'Accept' : 'application/json',
	# 	   'apikey' : self.apiKey }
	
 #        try:
 #            request  = urllib2.Request(url, headers=headers)
 #            response = urllib2.urlopen(request)
 #            the_page = response.read()
        
 #        except urllib2.HTTPError as e:
            
 #            the_page = e.read()
 #            decoded  = json.loads(the_page)
 #            raise AfricasTalkingGatewayException(decoded['SMSMessageData']['Message'])
        
 #        else:
            
 #            decoded  = json.loads(the_page)
 #            messages = decoded['SMSMessageData']['Messages']
        
 #            return messages
        
 #    def call(self, from_, to_):
	# values = {'username' : self.username,
	# 	  'from'     : from_,
 #                  'to'       : to_ }
        
	# headers = {'Accept' : 'application/json',
 #                   'apikey' : self.apiKey }
        
 #        try:
 #            data     = urllib.urlencode(values)
 #            request  = urllib2.Request(self.VoiceURLString, data, headers=headers)
 #            response = urllib2.urlopen(request)
        
 #        except urllib2.HTTPError as e:
            
 #            the_page = e.read()
 #            decoded  = json.loads(the_page)
 #            raise AfricasTalkingGatewayException(decoded['ErrorMessage'])
            
