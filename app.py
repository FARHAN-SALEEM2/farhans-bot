from flask import Flask, request, render_template
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
from_number = os.environ["TWILIO_WHATSAPP_NUMBER"]

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    numbers = request.form['numbers']
    msg = request.form['message']
    results = []

    for number in numbers.split(','):
        number = number.strip()
        try:
            message = client.messages.create(
                from_='whatsapp:' + from_number,
                to='whatsapp:' + number,
                body=msg
            )
            results.append(f"✅ Sent to {number}: {message.sid}")
        except Exception as e:
            results.append(f"❌ Error sending to {number}: {str(e)}")

    return "<br>".join(results)

@app.route("/incoming", methods=['POST'])
def incoming():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    # FAQ / Knowledge base
    faqs = {
        "who is farhan saleem" : "founder of me ! aperson who blindly believes in himself ",
        "hours": "Our working hours are 9 AM to 6 PM, Monday to Friday.",
        "price": "Prices start from $10. For details, visit our website.",
        "shipping": "We offer free shipping on orders above $50.",
        "return": "You can return products within 30 days of purchase.",
        "order": "To place an order, please tell me the product name.",
        "farhan loves who": "Farhan loves a girl named Minahil Akhter. She's from the Computer Science department at UOL"
    }

    # Keyword matching
    for keyword, answer in faqs.items():
        if keyword in incoming_msg:
            msg.body(answer)
            break
    else:
        msg.body("Sorry, I didn't understand that. Try asking about hours, price, shipping, return, or order.")

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
