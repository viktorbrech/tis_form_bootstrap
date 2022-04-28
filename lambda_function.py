import json
from urllib.request import Request, urlopen

######
### This is deployed on AWS Lambda, and configured to receive CORS requests with GET method.
### Its purporse is to receive form submissions from the browser, apply backend validation, then send them to v3 Forms API.
######

def lambda_handler(event, context):
    # apply custom form field validation here
    try:
        prefix = event["queryStringParameters"]["email"].split("@")[0].lower()
        assert prefix != "info"
    except:
        return {
            'statusCode': 422,
            'body': json.dumps("Cannot use these form field values.")
        }
    # end of form validation
    
    #url = "https://webhook.site/21300906-9473-4fa4-ab8a-41fc8e805311"
    url = "https://api.hsforms.com/submissions/v3/integration/submit/3967897/febc3c34-1ed7-4cdc-852e-ec8b1624ad81"
    
    all_names = event["queryStringParameters"]["name"].split()
    if len(all_names) == 2:
        first_name = all_names[0]
        last_name = all_names[1]
    else:
        first_name = event["queryStringParameters"]["name"]
        last_name = ""
    
    body = {
        "fields": [
            {
                "name": "firstname",
                "value": first_name
            },
            {
                "name": "lastname",
                "value": last_name
            },
            {
                "name": "email",
                "value": event["queryStringParameters"]["email"]
            },
            {
                "name": "contact_us_issue",
                "value": event["queryStringParameters"]["issue"]
            }
        ],
        "context": {
            "pageUri": event["queryStringParameters"]["pageuri"],
            "pageName": event["queryStringParameters"]["pagename"]
        },
        "legalConsentOptions": {
            "consent": {
                "consentToProcess": True,
                "text": "",
                "communications": [
                    {
                        "value": event["queryStringParameters"]["consent"],
                        "subscriptionTypeId": 4546887,
                        "text": "One-To-One Communication"
                    }
                ]
            }
        }
    }
    if "hubspotutk" in event["queryStringParameters"]:
        body["context"]["hutk"] = event["queryStringParameters"]["hubspotutk"]
    req = Request(url, json.dumps(body).encode("ascii"), {"Content-Type": "application/json"})
    
    if urlopen(req).status > 299:
        return {
            'statusCode': 422,
            'body': json.dumps("Cannot submit form.")
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("OK")
        }
