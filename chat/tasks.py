from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from chat.models import Person, Earthquake, EarthquakeRecord, Location
from chat.constant.location import CITYS
import re
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync
import requests

from datetime import datetime

from decouple import config

import json


@shared_task
def my_task():
    try:
        # Perform database operation
        response = requests.get(
            f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={config("TOKEN1")}&AreaName=%E5%AE%9C%E8%98%AD%E7%B8%A3"
        )

        data = response.json()

        so_far_eq = Earthquake.objects.latest("id")
        so_far_eq_id = so_far_eq.earthquake_number

        latest_eq = data["records"]["Earthquake"][0]

        if latest_eq is not None:
            if latest_eq["EarthquakeNo"] > so_far_eq_id:

                latest_eq_id = latest_eq["EarthquakeNo"]
                new_eq = {
                    "location_desc": latest_eq["EarthquakeInfo"]["Epicenter"][
                        "Location"
                    ],
                    "earthquake_number": latest_eq_id,
                    "magnitude": latest_eq["EarthquakeInfo"]["EarthquakeMagnitude"][
                        "MagnitudeValue"
                    ],
                    "occur_time": datetime.strptime(
                        latest_eq["EarthquakeInfo"]["OriginTime"], "%Y-%m-%d %H:%M:%S"
                    ),
                    "depth": latest_eq["EarthquakeInfo"]["FocalDepth"],
                }

                new_earthquake = Earthquake.objects.create(**new_eq)

                shaking_areas = latest_eq["Intensity"]["ShakingArea"]

                # empty groups and then will notify the clients..
                groups_info = []
                for area in shaking_areas:
                    county = area["CountyName"]


                    intensity = int(re.findall(r"\d+", area["AreaIntensity"])[0])
                    if county in CITYS:
                        group_name = f"{CITYS.index(county)}_group"
                        group_message = {
                            "type": "notification",
                            "message": json.dumps({
                                "intensity": intensity,
                                "eq_center": new_eq["location_desc"],
                                "eq_center_magnitude": new_eq["magnitude"],
                                "occur_time": latest_eq["EarthquakeInfo"]["OriginTime"],
                                "depth": new_eq["depth"],
                                "location": county,
                            }),
                        }

                        groups_info.append(
                            {
                                "name": group_name,
                                "message": group_message,
                            }
                        )

                        location = Location.objects.get(name=county)

                        new_record = {
                            "l_id": location,
                            "intensity":  intensity,
                            "e_id": new_earthquake,
                        }

                        EarthquakeRecord.objects.create(**new_record)

                # send to the socket

                print(groups_info)
                channel_layer = get_channel_layer()

                for group in groups_info:
                    print("name: ", group["name"])
                    async_to_sync(channel_layer.group_send)(
                        group["name"], group["message"]
                    )

    except Exception as e:
        # Log the error
        print(f"An error occurred: {e}")
    # get the remote data => by request
    # save the data into the database
