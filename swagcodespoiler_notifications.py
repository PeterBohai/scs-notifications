import os
import json
from datetime import datetime

import requests
from dotenv import load_dotenv
from dateutil import tz
from dateutil.parser import isoparse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

USER_USERNAME = 'swagcodespoiler'
USER_ID = 137060402
TIME_FRAME_MINUTES = 30
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
    return {'tweet.fields': 'created_at', 'max_results': 20}


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


def convert_from_utc(datetime_utc, to_zone='America/Chicago'):
    to_tz = tz.gettz(to_zone)
    datetime_converted = datetime_utc.astimezone(to_tz)
    return datetime_converted


def check_for_new_tweets(tweets):
    """Returns a list of new Tweets, if none, return empty list."""
    one_minute = 60
    new_tweets = []

    for tweet in tweets:
        tweet_timestamp = tweet['created_at']

        tweet_datetime_utc = isoparse(tweet_timestamp)
        now_datetime_utc = datetime.utcnow().replace(tzinfo=tz.gettz('UTC'))

        time_frame_seconds = TIME_FRAME_MINUTES * one_minute
        if (now_datetime_utc - tweet_datetime_utc).seconds <= time_frame_seconds:
            new_tweets.append(tweet)
            print('New Swag Code!')

    return new_tweets


def send_email(tweets, from_email=PERSONAL_EMAIL, to_email=PERSONAL_EMAIL):
    num_tweets = len(tweets)

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='New SwagCode Available!',
        html_content=f'<h3 style="margin-bottom:12px">{num_tweets} new Swag Code{"" if num_tweets == 1 else "s"} recently got posted!</h3>'
                     f'<a href="https://sc-s.com/" style="appearance:button;text-decoration:none;color:initial;border-style:outset;padding:5px;border-radius:10px">Go to <strong>Swag Code Spoiler</strong></a>'
                     f'<div style="height:20px"></div>'
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


def main():
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    url = create_url()
    headers = create_headers(bearer_token)
    params = get_params()

    response_data = connect_to_endpoint(url, headers, params)

    # print(json.dumps(response_data, indent=2, sort_keys=True))

    recent_tweets = response_data['data']
    new_tweets = check_for_new_tweets(recent_tweets)

    if new_tweets:
        print('New tweets found, sending email notification...')
        send_email(new_tweets)
    print('No New tweets found.')


def lambda_handler(event, context):
    """Entry point function that will be executed by AWS Lambda."""
    print('Starting Swag Code Spoiler Notification Checker...')
    main()
    return {
        'statusCode': 200,
        'body': json.dumps('Completed successfully!')
    }
