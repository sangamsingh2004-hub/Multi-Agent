import wikipedia
import requests

class WikiAgent:
    def __init__(self):
        pass

    def get_info(self, query):
        try:
            return wikipedia.summary(query, sentences=2)
        except wikipedia.exceptions.DisambiguationError:
            return "Multiple results found. Please be more specific."
        except wikipedia.exceptions.PageError:
            return "No information found."

class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"Weather in {city}: {weather}, Temperature: {temp}°C"
        else:
            return "Failed to retrieve weather data. (Check API key or city name)"
            
class Controller:
    def __init__(self, wiki_agent, weather_agent):
        self.wiki_agent = wiki_agent
        self.weather_agent = weather_agent

    def route_query(self, query):
        q_lower = query.lower()

        if q_lower.startswith("who") or q_lower.startswith("what"):
            return self.wiki_agent.get_info(query)

        if "weather" in q_lower:
            words = query.split()

            remove_words = ["weather", "in", "of", "is", "the", "tell", "me"]
            city_words = [w for w in words if w.lower() not in remove_words]

            if len(city_words) == 0:
                return "Please specify a city."

            city = " ".join(city_words)
            return self.weather_agent.get_weather(city)

        return "Sorry, I didn't understand your query."


if __name__ == "__main__":
    wiki_agent = WikiAgent()

    weather_agent = WeatherAgent("359abc4c5edae28da772b69aafc02cda")

    controller = Controller(wiki_agent, weather_agent)

    queries = [
        "Who is Elon Musk?",
        "What is Python programming?",
        "Weather in London",
        "Tell me weather of New York",
        "London weather"
    ]

    for query in queries:
        print(f"Query: {query}")
        print(controller.route_query(query))
        print()