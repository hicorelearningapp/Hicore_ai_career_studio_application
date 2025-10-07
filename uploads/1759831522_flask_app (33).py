from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

COMPANY_EMAIL = 'vyokesh344@gmail.com'
EMAIL_PASSWORD = 'xpwv jwqm aeaf pkzv'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        message = request.form.get('message')

        msg = MIMEMultipart('related')
        msg['Subject'] = f'New Contact Us Message from {name}'
        msg['From'] = COMPANY_EMAIL
        msg['To'] = COMPANY_EMAIL

        html_content = f"""
        <html>
        <body style="font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #eef2f7; margin:0; padding:0;">
            <table width="100%" cellpadding="0" cellspacing="0" style="padding: 40px 0;">
                <tr>
                    <td align="center">
                        <table width="650" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 6px 25px rgba(0,0,0,0.1);">

                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(90deg, #1E3A8A, #3B82F6); padding: 25px; text-align: center;">
                                    <img src="cid:logo_image" alt="Hicore Soft" style="width: 150px; height: 50px; margin-bottom: 10px;">
                                    <h2 style="color: #ffffff; font-size: 24px; margin: 0;">New Contact Us Submission</h2>
                                </td>
                            </tr>

                            <!-- Body -->
                            <tr>
                                <td style="padding: 35px; color: #333333; font-size: 16px; line-height: 1.6;">
                                    <p>Hello Team,</p>
                                    <p>You have received a new message via your website's Contact Us form. Details are as follows:</p>

                                    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 20px; border-collapse: collapse; font-size: 15px;">
                                        <tr style="background-color: #f9fafb;">
                                            <td style="padding: 14px; font-weight: bold; width: 160px;">Name</td>
                                            <td style="padding: 14px;">{name}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 14px; font-weight: bold;">Email</td>
                                            <td style="padding: 14px;">{email}</td>
                                        </tr>
                                        <tr style="background-color: #f9fafb;">
                                            <td style="padding: 14px; font-weight: bold;">Phone Number</td>
                                            <td style="padding: 14px;">{phone_number}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 14px; font-weight: bold;">Message</td>
                                            <td style="padding: 14px;">{message}</td>
                                        </tr>
                                    </table>

                                    <p style="margin-top: 30px; font-size: 14px; color: #555555;">
                                        This message was automatically generated from your website's Contact Us form.
                                    </p>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f1f3f7; padding: 25px; text-align: center; font-size: 13px; color: #777777;">
                                    &copy; 2025 Hicore Soft. All rights reserved.
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        # Attach uploaded logo image
        logo_path = os.path.join(app.root_path, "static", "hicoresoft.png")

        with open(logo_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<logo_image>')
            img.add_header('Content-Disposition', 'inline', filename='logo.png')
            msg.attach(img)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(COMPANY_EMAIL, EMAIL_PASSWORD)
        server.sendmail(COMPANY_EMAIL, COMPANY_EMAIL, msg.as_string())
        server.quit()

        return {"status": "success", "message": "Email sent successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == '__main__':
    app.run(debug=True)
