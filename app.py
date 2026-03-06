from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from sendgrid.helpers.mail import Mail as SendGridMail
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quote_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            service_type TEXT NOT NULL,
            details TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()


def cleanup_old_records():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM quote_requests 
        WHERE submitted_at < datetime('now', '-1 year')
    ''')
    conn.commit()
    conn.close()

cleanup_old_records()

# Send database data to email
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/schedule-a-quote')
def quote():
    return render_template('schedule-quote.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    location = request.form.get('location')
    service_type = request.form.get('service_type')
    details = request.form.get('details')

    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quote_requests (name, email, phone, location, service_type, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, location, service_type, details))
    conn.commit()
    conn.close()

    # Create an automated email template
    message = SendGridMail(
        from_email=BUSINESS_EMAIL,
        to_emails=BUSINESS_EMAIL,
        subject=f'New Quote Request from {name}',
        html_content=f'''
               <h2>New Quote Request</h2>
               <p><strong>Name:</strong> {name}</p>
               <p><strong>Email:</strong> {email}</p>
               <p><strong>Phone:</strong> {phone}</p>
               <p><strong>Location:</strong> {location}</p>
               <p><strong>Service:</strong> {service_type}</p>
               <p><strong>Details:</strong> {details or 'None provided'}</p>
           '''
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(f'Email error: {e}')

    confirmation = SendGridMail(
        from_email=BUSINESS_EMAIL,
        to_emails=email,
        subject='We received your quote request!',
        html_content=f'''
            <h2>Thanks, {name}!</h2>
            <p>We've received your quote request and will get back to you as soon as possible.</p>
            <br>
            <p><strong>Here's what you submitted:</strong></p>
            <p><strong>Service:</strong> {service_type}</p>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Details:</strong> {details or 'None provided'}</p>
            <br>
            <p>If you have any questions in the meantime, feel free to call us at <strong>231-343-0895</strong>.</p>
            <p>— One Touch Siding</p>
        '''
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(confirmation)
    except Exception as e:
        print(f'Confirmation email error: {e}')

    return jsonify({'success': True, 'message': 'Quote received!'})

# Implement a event tab that updates with current giveaways and etc
if __name__ == '__main__':
    app.run()
