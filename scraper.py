import requests
from bs4 import BeautifulSoup


def get_weather_data(city):
    """Fetches weather data for the given city from a search engine.

    Args:
        city (str): The city to scrape weather data for.

    Returns:
        dict: A dictionary containing scraped weather information (if successful),
             or None if scraping fails.

    Raises:
        Exception: If an unexpected error occurs during scraping.
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    language = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers["User-Agent"] = user_agent
    session.headers["Accept-Language"] = language
    session.headers["Content-Language"] = language

    try:
        city = city.replace(" ", "+")
        url = f"https://www.google.com/search?q=weather+in+{city}"
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.content, "html.parser")

        # Implement your specific data extraction logic here
        weather = {}
        region_element = soup.find("span", attrs={"class": "BBwThe"})
        if region_element:
            weather["region"] = region_element.text.strip()

        dayhour_element = soup.find("div", attrs={"id": "wob_dts"})
        if dayhour_element:
            weather["dayhour"] = dayhour_element.text.strip()

        status_element = soup.find("span", attrs={"id": "wob_dc"})
        if status_element:
            weather["status"] = status_element.text.strip()

        temp_element = soup.find("span", attrs={"id": "wob_tm"})
        if temp_element:
            weather["temp"] = temp_element.text.strip()

        humidity_element = soup.find("span", attrs={"id": "wob_hm"})
        if humidity_element:
            weather["humidity"] = humidity_element.text.strip()

        wind_element = soup.find("span", attrs={"id": "wob_ws"})
        if wind_element:
            weather["wind"] = wind_element.text.strip()

        return weather

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None  # Indicate scraping failure


if __name__ == "__main__":
    city = input("Enter city name: ")
    weather_data = get_weather_data(city)

    if weather_data:
        print("Weather data:")
        for key, value in weather_data.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("Failed to scrape weather data.")
