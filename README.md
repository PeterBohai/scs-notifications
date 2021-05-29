# Swag Code Spoiler Notifications
This is an **AWS Lambda** function that will check for new Swag Codes posted on the 
[@swagcodespoiler](https://twitter.com/swagcodespoiler) Twitter account and email out a notification. The Lambda function is triggered via 
**AWS CloudWatch** as a scheduled Event, and it runs every 15 minutes from 2pm GMT to 1am GMT.
This interval guarantees that every new Tweet is caught in a relatively timely manner.

The email displays the Swag Code (scraped from [sc-s.com](http://sc-s.com/)) directly if it is a static code or as a link that leads to the appropriate Swagbucks page if it is a dynamic code. 

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
    
#### Main Third-party Libraries
- [requests](https://pypi.org/project/requests/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)
- [python-dotenv](https://pypi.org/project/python-dateutil/)
- [sendgrid](https://pypi.org/project/sendgrid/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Please check the `requirements.txt` for specific dependencies and versions used.

## Other Details
The scheduled event is specified using the following Cron expression:

8/15 14-1 ? * * *

**An important point to note**: Although "lxml" is generally the suggested parser to use (see [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)), 
it is quite difficult to set up correctly in AWS Lambda. Simply installing "lxml" with the other libraries using pip and zipping it as a layer does not work.
The easiest workaround is to use Python's built-in HTML parser - "html.parser". The trade-off is a small decrease in parsing speed. To learn more about the different parsers that Beautiful Soup supports, please check the [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser).

## Bug Reports and Improvements
If you experience any bugs or see anything that can be improved or added, please feel free to [open an issue](https://github.com/PeterBohai/scs-notifications/issues) here or simply contact me through any of the methods below. Thanks in advance!

Email: peterbohai@gmail.com <br/>
Linkedin: [linkedin.com/in/peterbohai](www.linkedin.com/in/peterbohai)
