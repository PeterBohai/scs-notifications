import os
import json

from dotenv import load_dotenv

from helpers import scs_scraper, emails, tweets

load_dotenv()

USER_USERNAME = 'swagcodespoiler'
USER_ID = 137060402
TIME_FRAME_MINUTES = 15
PERSONAL_EMAIL = os.environ.get('PERSONAL_EMAIL')

SENDGRID_KEY = os.environ.get('SENDGRID_API_KEY')
TWITTER_API_BEARER = os.environ.get('TWITTER_BEARER_TOKEN')


def main():
    recent_tweets = tweets.get_recent_tweets(user_id=USER_ID, bearer_token=TWITTER_API_BEARER)
    print(json.dumps(recent_tweets, indent=2, sort_keys=True))

    new_tweet = tweets.check_for_new_tweet(recent_tweets, time_frame_minutes=TIME_FRAME_MINUTES)

    if new_tweet:
        print('Parsing tweet...')
        new_tweet_data = tweets.parse_tweet(new_tweet)
        print('Extracting Swag Code value from sc-s.com...')
        swagcode = scs_scraper.extract_swagcode(new_tweet_data['scs_url'])
        swagcode_data = {
            'swagcode': swagcode,
            **new_tweet_data
        }
        print('Creating email template...')
        message_content = {
            'subject': 'New SwagCode Available!',
            'html_content': emails.get_scs_email_template(swagcode_data)
        }
        print('Sending email...')
        emails.send_email(SENDGRID_KEY, message_content, PERSONAL_EMAIL, PERSONAL_EMAIL)
    else:
        print('No new tweets!')


def lambda_handler(event, context):
    """Entry point function that will be executed by AWS Lambda."""
    print('Starting Swag Code Spoiler Notification Checker...')
    main()
    return {
        'statusCode': 200,
        'body': json.dumps('Completed successfully!')
    }
