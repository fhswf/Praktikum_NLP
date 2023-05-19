# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pyowm.owm import OWM
import pytz
import requests


class ActionTime(Action):
    def name(self) -> Text:
        return "action_time"
    
    def get_time_in_city(self, city: str) -> str:
        geolocator = Nominatim(user_agent="city_timezone_locator")
        location = geolocator.geocode(city)

        if not location:
            raise ValueError(f"Location not found for {city}")

        timezone_finder = TimezoneFinder()
        timezone_name = timezone_finder.timezone_at(lng=location.longitude, lat=location.latitude)

        if not timezone_name:
            raise ValueError(f"Timezone not found for {city}")

        timezone = pytz.timezone(timezone_name)
        current_time = datetime.now(timezone)
        time_str = current_time.strftime("%I:%M %p %Z on %A, %B %d, %Y")

        return f"The current time in {city} is {time_str}"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.latest_message['entities'])
        cities = list(map(lambda x: x['value'], 
                      filter(lambda x: x['entity'] == 'GPE', tracker.latest_message['entities'])))
        city = cities[0] if cities else "Iserlohn"
        time = self.get_time_in_city(city)
        
        dispatcher.utter_message(text=time)
        return []

    
class ActionWeather(Action):
    def __init__(self):
        Action.__init__(self)
        self.owm = OWM('70cc3025706fcdbd8a7631b8104b8340')
        self.mgr = self.owm.weather_manager()
        
    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.latest_message['entities'])
        cities = list(map(lambda x: x['value'], 
                      filter(lambda x: x['entity'] == 'GPE', tracker.latest_message['entities'])))
        city = cities[0] if cities else "Iserlohn"
        
        
        observation = self.mgr.weather_at_place(city)
        temperature = observation.weather.temperature('celsius')['temp']
        status = observation.weather.detailed_status
        icon = observation.weather.weather_icon_url()
        print(observation.weather, dir(observation.weather))
        
        dispatcher.utter_message(text=f"in {city}, it is {temperature}° and {status}", image=icon)
        return []
    
class ActionJoke(Action):
    
    def name(self) -> Text:
        return "action_joke"
    
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
        response = requests.get(url)
        
        dispatcher.utter_message(text=f"'{response.json()['joke']}'")
        return []        