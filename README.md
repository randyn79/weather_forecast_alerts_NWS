# weather_forecast_alerts_NWS
Uses the National Weather Service API to obtain the current weather alerts and forecast for my area and sends an email with this information.

## get_forecast()
Gets the weather forecast from the National Weather Service API.  The grid listed is for my local area.  For more information on changing this, see the official documentation at https://www.weather.gov/documentation/services-web-api.

## get_alerts()
Gets the active weather alerts from the National Weather Service API for my area.  You will need to enter your latitude and longitude in the params to change this to your area.  See the official documentation at https://www.weather.gov/documentation/services-web-api.

NOTE: This was written when there were several active alerts.  I will have to test the behavior again when there are no active alerts.
* UPDATE (17 Jan 2022) - When there are no active alerts, the output is blank, however since there is a header it looks a little odd.  May either try to return "None" for the value or leave the header off.

## gmail_forecast_text()
Sends the forecast and weather alerts as a text gmail.  For this to work the sender_email Gmail settings has to be set to allow less secure apps.  At the time of this writing in order to enable this you also have to turn off 2 factor authentication if you have it enabled.  For testing purposes it may be better to create a test GMail account instead of changing the settings on your primary account.
