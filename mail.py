import smtplib
from email.message import EmailMessage

def send_mail():
    msg = EmailMessage()
    
    msg['Subject'] = '⚠️ Unauthorized Person Detected'
    msg['From'] = 'sakshir132004@gmail.com'   # 👈 YOUR EMAIL
    msg['To'] = 'latesukanya2@gmail.com' # 👈 RECEIVER EMAIL

    msg.set_content('Alert! Unauthorized person detected in Military System.')

    # Attach image
    try:
        with open('unauthorized.jpg', 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename='unauthorized.jpg')
    except:
        print("Image not found")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('sakshir132004@gmail.com', 'whvr ijjz beyg ijpm')  # 👈 PASSWORD
            smtp.send_message(msg)
            print("Mail Sent Successfully")
    except Exception as e:
        print("Mail Failed:", e)

send_mail()