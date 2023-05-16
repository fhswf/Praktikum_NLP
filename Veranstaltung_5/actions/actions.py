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
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


class ActionHelloWorld(Action):
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
