import os
import re
import json
from datetime import datetime

import requests
from dotenv import load_dotenv
from dateutil import tz
import dateutil.parser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

USER_USERNAME = 'swagcodespoiler'
USER_ID = 137060402
TIME_FRAME_MINUTES = 15
PERSONAL_EMAIL = os.environ.get('PERSONAL_EMAIL')


def create_url():
    user_id = USER_ID
    return f'https://api.twitter.com/2/users/{user_id}/tweets'


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {'tweet.fields': 'created_at', 'max_results': 5}


def create_headers(bearer_token):
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request('GET', url, headers=headers, params=params)
    print(f'{response.status_code} - Response Status Code')

    if response.status_code != 200:
        raise Exception(f'Request returned an error: {response.status_code} - {response.text}')

    return response.json()


def check_for_new_tweet(tweets):
    """Returns a new Tweet if available. If not, return None"""
    one_minute = 60

    for tweet in tweets:
        print(tweet)
        tweet_timestamp = tweet['created_at']

        tweet_datetime_utc = dateutil.parser.isoparse(tweet_timestamp)
        now_datetime_utc = datetime.utcnow().replace(tzinfo=tz.gettz('UTC'))

        time_frame_seconds = TIME_FRAME_MINUTES * one_minute
        if (now_datetime_utc - tweet_datetime_utc).total_seconds() <= time_frame_seconds:
            return tweet
    return None


def send_email(tweet_data, from_email=PERSONAL_EMAIL, to_email=PERSONAL_EMAIL):
    expire_time = tweet_data['expire_time'].strftime("%I:%M %p")
    num_sb = tweet_data['num_sb']

    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <body style="font-family: Roboto,Helvetica,Arial,sans-serif;">
            <p style="text-align: center; margin: 0">
                SwagCode (<strong>{num_sb} SBs</strong>) is valid until <strong>{expire_time}</strong> CST
            </p>
            <div style="text-align: center">
                <div style="line-height: 60px; font-weight: bold; height:25px">
                    
                </div>
                <a href="http://sc-s.com/" 
                   style="background-color:#333333; border:1px solid #333333; border-radius:3px; color:#ffffff; display:inline-block; font-size:14px; font-weight:normal; letter-spacing:0px; line-height:normal; padding:6px 13px 6px 13px; text-align:center; text-decoration:none;" 
                   target="_blank">
                    sc-s.com
                </a>
                <p style="margin: 0; margin-top: 10px; margin-bottom: 10px">
                    Visit the Swag Code Spoiler official website above for the swag code details. Go to SwagBucks to claim your free SB. 
                </p>
                <a href="https://www.swagbucks.com/" 
                   style="background-color:#FFFFFF; border:2px solid #339fba; border-radius:5px; color:#339FBA; display:inline-block; font-size:14px; font-weight:bold; letter-spacing:0; line-height:normal; padding:6px 13px 6px 13px; text-align:center; text-decoration:none" 
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

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='New SwagCode Available!',
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)

        print(f'Email sent to {to_email}!')
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def parse_tweet(tweet):
    """Returns a dictionary containing information about the number of SBs rewarded and the Swag Code expiry time."""

    print('Parsing tweet....')

    m = re.match(r".* (?P<num_sb>\d+) SBs and expires at (?P<expire_time>\d\d:\d\d \w\w \w\w\w)", tweet['text'])
    tweet_data = m.groupdict()

    tzinfos = {
        'PDT': tz.gettz('America/Los Angeles'),
        'CST': tz.gettz('America/Chicago')
    }
    expire_time_pdt = dateutil.parser.parse(tweet_data['expire_time'], tzinfos=tzinfos)
    expire_time_local = expire_time_pdt.astimezone(tzinfos['CST'])

    swagcode_data = {
        'num_sb': tweet_data['num_sb'],
        'expire_time': expire_time_local
    }
    print('Parsed tweet: ', swagcode_data)
    return swagcode_data


def main():
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    url = create_url()
    headers = create_headers(bearer_token)
    params = get_params()

    response_data = connect_to_endpoint(url, headers, params)

    # print(json.dumps(response_data, indent=2, sort_keys=True))

    recent_tweets = response_data['data']
    new_tweet = check_for_new_tweet(recent_tweets)

    if new_tweet:
        print('New tweets found, sending email notification...')
        new_tweet_data = parse_tweet(new_tweet)
        send_email(new_tweet_data)

    print('No New tweets found.')


def lambda_handler(event, context):
    """Entry point function that will be executed by AWS Lambda."""
    print('Starting Swag Code Spoiler Notification Checker...')
    main()
    return {
        'statusCode': 200,
        'body': json.dumps('Completed successfully!')
    }
