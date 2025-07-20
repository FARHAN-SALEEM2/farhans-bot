from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/incoming", methods=["POST"])
def incoming_sms():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hello" in incoming_msg:
        msg.body("Hi there! 👋 How can I help you today?")
    else:
        msg.body("Sorry, I didn't understand that.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔥 Render will inject PORT
    app.run(debug=True, host="0.0.0.0", port=port)  # ✅ Bind to all IPs
