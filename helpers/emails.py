import os
from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv


def send_email(sendgrid_key, message_content, from_email, to_email):
    """Sends an email containing the contents in `message_content` to the specified email.

    Args:
        sendgrid_key (str): The SendGrid API Key.
        message_content (dict): Contains a 'subject' and 'html_content' field for the Mail() parameters.
        from_email (str): The email address the message is sent by.
        to_email (str): The email address that will receive the message.

    Returns:
        None

    """
    try:
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=message_content['subject'],
            html_content=message_content['html_content']
        )
    except KeyError as key:
        print(f'KeyError: {key} is a required field needed to send the email message!')
        return

    try:
        sg = SendGridAPIClient(sendgrid_key)
        response = sg.send(message)

        print(f'Email was sent to {to_email}!')
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as err:
        print(err)


def get_scs_email_template(swagcode_data):
    expire_time = swagcode_data['expire_time'].strftime("%I:%M %p")
    num_sb = swagcode_data['num_sb']
    swagcode = swagcode_data['swagcode']

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="font-family: Roboto,Helvetica,Arial,sans-serif;">
        <p style="text-align: center; margin: 0">
            SwagCode (<strong>{num_sb} SBs</strong>) is valid until <strong>{expire_time}</strong> CST
        </p>
        <div style="text-align: center">
            <div style="line-height: 60px; font-weight: bold; height:25px">
            </div>
            {
                f'<a href={swagcode["value"]} target="_blank" style="font-size: large; color:#339FBA">Click Here to Get the Swag Code</a>' 
                if swagcode['type'] == 'dynamic' 
                else 
                f'<h3>{swagcode["value"]}</h3>'
            }
            <p style="margin: 0; margin-top: 10px; margin-bottom: 10px">
                Visit the <a href="http://sc-s.com/" target="_blank">Swag Code Spoiler</a> official website for other swag code details. Go to SwagBucks to claim your free SB. 
            </p>
            <a href="https://www.swagbucks.com/" 
               style="background-color:#FFFFFF; 
                        border:2px solid #339fba; 
                        border-radius:5px; color:#339FBA; 
                        display:inline-block; font-size:14px; 
                        font-weight:bold; letter-spacing:0; 
                        line-height:normal; 
                        padding:6px 13px 6px 13px; 
                        text-align:center; text-decoration:none" 
               target="_blank">
                Swagbucks
            </a>
            <p style="font-size:12px; line-height:20px;">
                <a href="unsubscribe" target="_blank" style="">
                Unsubscribe
                </a>
            </p>
        </div>
    </body>
    </html>
    """


if __name__ == '__main__':
    load_dotenv()
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    main_email = os.environ.get('PERSONAL_EMAIL')

    # swagcode = {
    #     'type': 'dynamic',
    #     'value': 'https://www.swagbucks.com/p/offer-page/?id=5781'
    # }
    swagcode = {
        'type': 'static',
        'value': 'FREESharjo3p'
    }
    swagcode_data = {
        'expire_time': datetime.utcnow(),
        'num_sb': 8,
        'swagcode': swagcode
    }
    content = {
        'subject': 'New SwagCode Available!',
        'html_content': get_scs_email_template(swagcode_data)
    }
    send_email(sendgrid_api_key, content, main_email, main_email)
