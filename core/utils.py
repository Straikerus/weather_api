from collections import defaultdict

def format_weather(weather_rows):
    formatted_weather_dict = defaultdict(list)
    for row in weather_rows:
        weather_info = {
            'source': row.source,
            'temperature': row.temperature,
            'datetime': row.date
        }
        formatted_weather_dict[row.name].append(weather_info)
    return formatted_weather_dict
