import requests
import json
import smtplib
import ssl


def get_forecast(base_url: str, headers: dict) -> list:
    '''Gets the weather forecast from the National Weather Service API https://www.weather.gov/documentation/services-web-api'''
    url = base_url + '/gridpoints/FFC/45,94/forecast' # Grid here(45,94) must be obtained with lat/lon from the API site if being changed.
    response = requests.get(url, headers=headers)
    nws_response = response.json()
    forecasts = []
   
    for i in nws_response['properties']['periods']:
        forecast_text = f'''
====================================
{i['name']} -
Temp: {i['temperature']} {i['temperatureUnit']}  |  Wind: {i['windSpeed']} {i['windDirection']}

{i['shortForecast']}

{i['detailedForecast']}
------------------------------------'''
        forecasts.append(forecast_text)
    return forecasts
   

def get_alerts(base_url: str, headers: dict) -> list:
    '''Gets weather alerts from the National Weather Service API https://www.weather.gov/documentation/services-web-api'''
    url = base_url + '/alerts/active'
    params = ('point=<ENTER LATITUDE>,<ENTER LONGITUDE>') #Enter LAT and LON
    response = requests.get(url, headers=headers, params=params)
    nws_response = response.json()
    alerts = []
    for i in nws_response['features']:
        alert_text = f'''
====================================
{i['properties']['severity']} ALERT - {i['properties']['certainty']} - {i['properties']['urgency']}
====================================
Event: {i['properties']['event']}

Alert: {i['properties']['headline']}

Description:
{i['properties']['description']}
'''
        alerts.append(alert_text)
    return alerts

def gmail_forecast_text(alerts, forecasts):
    '''Sends a text email for the weather alerts and forecast to a designated email address.  Please
see the Readme file for more information on what is required by Google for this to work, as you may
want to use a different method of doing this.'''
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender_email = '<ENTER SENDER EMAIL>' #Enter sender email address
    receiver_email = '<ENTER RECEIVER EMAIL>' #Enter receiver email address
    password = input('Enter password: ')

    alert_header = ['''
************************************
************************************
ALERTS
************************************
************************************''']
    forecast_header = ['''
************************************
************************************
FORECAST
************************************
************************************''']

    message_list = alert_header + alerts + forecast_header + forecasts
    message_text = str()
    for i in message_list:
        message_text += i

    message = f"""\
Subject: Weather Forecast
Here is your weather forecast and alerts.
{message_text}"""

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    
base_url = 'https://api.weather.gov'
headers = {'User-Agent': '<ENTER APP NAME>, <ENTER YOUR CONTACT EMAIL>'}

if __name__ == "__main__":
    forecasts = get_forecast(base_url, headers)
    alerts = get_alerts(base_url, headers)
    gmail_forecast_text(alerts, forecasts)
