import requests


def points_by_windspeed(points, max_speed):
    return [(i.x, i.y) for i in points if get_wind_speed(i.x, i.y) > max_speed]


def get_wind_speed(lat, lon):
    session = requests.Session()
    response = session.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=wind_speed_10m_max&forecast_days=1&wind_speed_unit=ms"
    )
    if response.ok:
        return response.json()["daily"]["wind_speed_10m_max"][0]
