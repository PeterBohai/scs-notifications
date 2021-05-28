import re
from json import dumps
from datetime import datetime

from dateutil import tz
import dateutil.parser
import requests


def get_params():
    # Tweet Field options include: attachments, author_id, context_annotations, conversation_id, created_at, entities,
    # geo, id, in_reply_to_user_id, lang, non_public_metrics, organic_metrics, possibly_sensitive,
    # promoted_metrics, public_metrics, referenced_tweets, source, text, and withheld
    return {
        'tweet.fields': 'created_at',
        'max_results': 5
    }


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


def get_recent_tweets(user_id, bearer_token):
    url = f'https://api.twitter.com/2/users/{user_id}/tweets'
    headers = create_headers(bearer_token)
    params = get_params()

    response_data = connect_to_endpoint(url, headers, params)

    return response_data['data']


def check_for_new_tweet(tweets, time_frame_minutes=15):
    """Returns a new Tweet if available. If not, return None"""
    one_minute = 60

    for tweet in tweets:
        tweet_timestamp = tweet['created_at']

        tweet_datetime_utc = dateutil.parser.isoparse(tweet_timestamp)
        now_datetime_utc = datetime.utcnow().replace(tzinfo=tz.gettz('UTC'))

        time_frame_seconds = time_frame_minutes * one_minute
        if (now_datetime_utc - tweet_datetime_utc).total_seconds() <= time_frame_seconds:
            print(f'New tweet: {dumps(tweet, indent=2)}')
            return tweet
    return None


def parse_tweet(tweet):
    """Returns a dictionary containing information about the number of SBs rewarded and the Swag Code expiry time."""

    print('Parsing tweet....')

    m = re.match(
        r".*(?P<num_sb>\d+)[\w\s]+(?P<expire_time>\d\d:\d\d \w\w [A-Z]+)\.[\w\s]+: (?P<scs_url>.*)",
        tweet['text'])

    tweet_data = m.groupdict()
    tzinfos = {
        'PDT': tz.gettz('America/Los Angeles'),
        'CST': tz.gettz('America/Chicago')
    }
    expire_time_pdt = dateutil.parser.parse(tweet_data['expire_time'], tzinfos=tzinfos)
    expire_time_local = expire_time_pdt.astimezone(tzinfos['CST'])

    swagcode_data = {
        'num_sb': tweet_data['num_sb'],
        'expire_time': expire_time_local,
        'scs_url': tweet_data['scs_url']
    }
    return swagcode_data


if __name__ == '__main__':
    example_tweet = {
        "created_at": "2021-05-25T23:57:42.000Z",
        "id": "1397341135173918722",
        "text": "There's a new #SwagCode out! It's worth 5 SBs and expires at 07:30 PM PDT. Get it here: https://t.co/VAUSRcHKqT"
    }
    print(parse_tweet(example_tweet))
