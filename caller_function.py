from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

#number must have plus in front
def call_user(number_):
	account_sid = 'ACb7fbf2db900d9b942e6e0a44386f3438'
	auth_token = '8944858c7672456fe0d84e8e4b88510e'
	client = Client(account_sid, auth_token)
	call = client.calls.create(
    	                    #url='call.xml',
        	                to=number_,
            	            from_='+19386665757'
	                    )

	print(call.sid)

call_user('+18016967027')
