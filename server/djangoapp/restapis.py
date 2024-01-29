import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        params=dict()
        api_key=None
        for k,v in kwargs.items():
            if k == 'api_key':
                api_key = v
            else:
                params[k] = v

        if api_key:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    #json_data = json.loads(response.text)
    json_data = response.text
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,**kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_by_id(url, dealerId=None):
    return get_dealers_from_cf(url, id=dealerId)

def get_dealers_by_state(url, state=None):
    return get_dealers_from_cf(url, state=state)


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    results = []
    json_result = get_request(url, dealerId = dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            #review_doc["sentiment"] = None
            review_doc["sentiment"] = analyze_review_sentiments(review_doc["review"])
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], sentiment=review_doc["sentiment"],
                                   id=review_doc["id"])
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

def analyze_review_sentiments(text):
    url = ''
    api_key = ''
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label=json.dumps(response, indent=2)

    try:
        label = response['sentiment']['document']['label']
    except:
        label = None

    return(label)






