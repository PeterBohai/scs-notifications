# Swag Code Spoiler Notifications
This is an **AWS Lambda** function that will check for new Swag Codes posted on the 
[@swagcodespoiler](https://twitter.com/swagcodespoiler) Twitter account. The Lambda function is triggered via 
**AWS CloudWatch** as a scheduled Event, and it runs every 30 minutes from 1pm GMT to 11pm GMT.
Since Swag Codes are often only posted every hour at most, checking every 30 minutes is enough to guarantee that every new Tweet is 
caught in a timely manner.

## Dependencies and Services
#### Services and APIs
- [AWS Lambda](https://aws.amazon.com/lambda/)
    - Serverless service provided by AWS to run cron processes like this
- [AWS CloudWatch](https://aws.amazon.com/cloudwatch/)
    - Service provided by AWS to trigger Lambda functions (scheduled event in this case)
- [Twilio SendGrid](https://sendgrid.com/docs/)
    - For sending emails reliably (especially to Gmail without having to enter email credentials)
- [Twitter Developer API (v2)](https://developer.twitter.com/en/docs/twitter-api)
    - For getting tweet information from a Twitter user 
      (using the [User Tweet Timeline](https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/introduction) endpoint) 
    
#### Third-party Libraries
- [requests](https://pypi.org/project/requests/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)
- [python-dotenv](https://pypi.org/project/python-dateutil/)
- [sendgrid](https://pypi.org/project/sendgrid/)

Please check the `requirements.txt` for specific dependencies and versions used.

## Other Details
The scheduled event is specified using the following Cron expression:

8/30 13-23 ? * * *

## Bug Reports and Improvements
If you experience any bugs or see anything that can be improved or added, please feel free to [open an issue](https://github.com/PeterBohai/scs_notifications/issues) here or simply contact me through any of the methods below. Thanks in advance!

Email: peterbohai@gmail.com <br/>
Linkedin: www.linkedin.com/in/peterbohai
