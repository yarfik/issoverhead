import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -7.708540
MY_LONG = 110.375510
EMAIL_FROM = "yarfikardiansyah@gmail.com"
EMAIL_PASS = ""
EMAIL_TO = "yarfik@gmail.com"


def is_iss_spotted():
    res = requests.get(url="http://api.open-notify.org/iss-now.json")
    res.raise_for_status()
    dt = res.json()

    iss_latitude = float(dt["iss_position"]["latitude"])
    iss_longitude = float(dt["iss_position"]["longitude"])
    print(iss_latitude, iss_longitude)
    return (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5) and (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5)


def is_dark(lat, lang):
    parameters = {
        "lat": lat,
        "lng": lang,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = (int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 7) % 24
    sunset = (int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 7) % 24

    time_now = datetime.now()
    current_hour = time_now.hour
    return current_hour <= sunrise or current_hour >= sunset


def send_email():
    content = f"Subject:LOOK UP! The ISS is over you!\n\nIf you wanna see the ISS, it is the time. Currently it is roaming over your region!"
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as conn:
        conn.starttls()
        conn.login(EMAIL_FROM, EMAIL_PASS)
        conn.sendmail(
            from_addr=EMAIL_FROM,
            to_addrs=EMAIL_TO,
            msg=content
        )


while True:
    time.sleep(60)
    if is_dark(MY_LAT, MY_LONG) and is_iss_spotted():
        send_email()
