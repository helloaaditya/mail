from flask import Flask, request, render_template, jsonify
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = '1a9b8958cf2ab665fe14284558ab408f'  # Required for flashing messages

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.internix.tech', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f'Email sent to {recipient_email}')
            return True  # Return True if email sent successfully
    except Exception as e:
        print(f'Failed to send email to {recipient_email}: {e}')
        return False  # Return False if there was an error

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    file = request.files['file']
    email_list = pd.read_excel(file, engine='openpyxl')['Email'].tolist()  # Ensure 'Email' is the column name in your Excel file
    sender_email = request.form['sender_email']
    sender_password = request.form['sender_password']
    subject = request.form['subject']
    body = request.form['body']
    
    sent_count = 0  # Initialize the counter for sent emails
    failed_count = 0  # Initialize the counter for failed emails

    for recipient_email in email_list:
        if send_email(sender_email, sender_password, recipient_email, subject, body):
            sent_count += 1  # Increment the counter for each successfully sent email
        else:
            failed_count += 1  # Increment the counter for each failed email

    return jsonify(success_count=sent_count, failure_count=failed_count)

if __name__ == '__main__':
    app.run(debug=True)
