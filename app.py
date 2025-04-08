from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__)

# PayU Configuration
MERCHANT_KEY = "6QA8BW"
MERCHANT_SALT = "IeBXlDTODKlw4JgClMn69BhsbZjrqULT"
PAYU_BASE_URL = "https://secure.payu.in/_payment"  # Use production URL

users = []

@app.route('/')
def home():
    return render_template('index.html')  # ✅ Correctly renders the HTML form

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # your existing form logic here...
    return jsonify({'message': 'User registered (mock response)'})

    if not data or 'mobile' not in data or len(data['mobile']) != 10:
        return jsonify({'error': 'Invalid registration data'}), 400

    txnid = f"TXN{len(users)+1}"
    amount = "20.00"
    productinfo = "Krishi Community Subscription"
    firstname = data.get('name', 'Farmer')
    email = data.get('email', 'test@example.com')
    phone = data['mobile']
    surl = request.url_root + "payment_success"
    furl = request.url_root + "payment_failure"

    # Create hash string
    hash_string = f"{MERCHANT_KEY}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{MERCHANT_SALT}"
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()

    # Store user
    users.append(data)

    # Auto-submit HTML form
    form_html = f"""
    <html>
        <body onload="document.forms[0].submit()">
            <form action="{PAYU_BASE_URL}" method="post">
                <input type="hidden" name="key" value="{MERCHANT_KEY}">
                <input type="hidden" name="txnid" value="{txnid}">
                <input type="hidden" name="amount" value="{amount}">
                <input type="hidden" name="productinfo" value="{productinfo}">
                <input type="hidden" name="firstname" value="{firstname}">
                <input type="hidden" name="email" value="{email}">
                <input type="hidden" name="phone" value="{phone}">
                <input type="hidden" name="surl" value="{surl}">
                <input type="hidden" name="furl" value="{furl}">
                <input type="hidden" name="hash" value="{hashh}">
            </form>
        </body>
    </html>
    """
    return render_template_string(form_html)

@app.route('/payment_success')
def payment_success():
    return "✅ Payment Successful! You’ll receive your KRISHI tokens soon."

@app.route('/payment_failure')
def payment_failure():
    return "❌ Payment Failed. Please try again."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
