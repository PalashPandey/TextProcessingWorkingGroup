from flask import Flask, request, session
from datetime import datetime
from datetime import time
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/homepage", methods=['GET', 'POST'])
def voice():
	"""Respond to incoming phone calls with a menu of options"""
	# global caller_phone_number

	caller_phone_number = request.values['From']
	session['caller_phone_number'] = caller_phone_number	

	# Start our TwiML response
	resp = VoiceResponse()
	resp.say('If you are calling from the hospital or if this is an urgent situation please call ' + clinic_phone_number + ' . If this is an emergency call 911.'  )
	resp.say('Welcome to ' + company_name +'! This is the automated appointment scheduling system. Let\'s continue!.'  )
	
	gather_tree = Gather(num_digits=1, action='/landline_or_mobile', input='dtmf' , actionOnEmptyResult="true")
	gather_tree.say('If you are calling from a Landline press 1. If you are calling from a mobile phone press 2. ')
	resp.append(gather_tree)

	# If the user doesn't select an option, redirect them into a loop
	resp.redirect('/voice')

	return str(resp)



if __name__ == "__main__":
	app.run(debug=True, port=9000)
