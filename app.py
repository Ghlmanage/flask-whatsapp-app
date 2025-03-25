from flask import Flask, request
from twilio.rest import Client
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

client = Client(account_sid, auth_token)

@app.route('/')
def home():
    return "🎉 Your Flask App is working perfectly!"

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')

    response = openai.ChatCompletion.create(
        model='gpt-4-turbo-preview',
        messages=[
            {"role": "system", "content": "You're a helpful virtual assistant."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply = response.choices[0].message.content

    client.messages.create(
        body=reply,
        from_=twilio_whatsapp_number,
        to=sender
    )

    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

