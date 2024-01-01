import requests
import numpy as np
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import json
import matplotlib.pyplot as plt
from matplotlib import style
import datetime
from dotenv import load_dotenv
import os

# weather_app

load_dotenv()
api_key = os.getenv('weather_api_key')


class WeatherClass():
    def __init__(self):
        self.api_key = api_key
        self.baseurl = "http://api.openweathermap.org/data/2.5/weather?"
        self.baseurl2 = "http://api.openweathermap.org/data/2.5/forecast?"
        self.weatherDict = {}
        # nextWeatherDict will be day : [temp, weather]
        self.nextWeatherDict = {}
        self.currentdatetime = datetime.datetime.now()
        self.currentday = self.currentdatetime.strftime('%A')
        self.graph_data = {}

    def getCurrentWeather(self, city_name):
        url = f"{self.baseurl}q={city_name}&appid={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # self.weatherDict.update({})
                self.weatherDict.update({'weather': data['weather'][0]['main']})
                self.weatherDict.update({'weather_desc': data['weather'][0]['description']})
                self.weatherDict.update({'temp': str(round(float(data['main']['temp']) - 273.15, 1)) + '°C'})
                self.weatherDict.update({'temp_min': str(round(float(data['main']['temp_min']) - 273.15, 1)) + '°C'})
                self.weatherDict.update({'temp_max': str(round(float(data['main']['temp_max']) - 273.15, 1)) + '°C'})
                self.weatherDict.update({'pressure': data['main']['pressure']})
                self.weatherDict.update({'coordinate1': data['coord']['lon']})
                self.weatherDict.update({'coordinate2': data['coord']['lat']})
                self.weatherDict.update({'timezone': data['timezone']})
                self.weatherDict.update({'visibility': str(round(float(data['visibility']) / 1000, 2)) + 'km'})
                self.weatherDict.update({'wind_speed': str(data['wind']['speed']) + 'm/s'})
                self.weatherDict.update({'country': data['sys']['country']})
                self.weatherDict.update(
                    {'sunrise': datetime.datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')})
                self.weatherDict.update(
                    {'sunset': datetime.datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')})

                return self.weatherDict


            else:
                print("Error getting response from server!")
                exit()

        except Exception as e:
            print("An error occured", str(e))
            exit()

    def extract_day_data(self, data):
        for days in data['list']:
            weather = days['weather'][0]['main']
            temp = days['main']['temp']
            date = days['dt_txt']
            date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            day = date_time.strftime('%A')

            weatherinfo = [weather, str(round(float(temp) - 273.15, 1)) + '°C']
            if day not in self.nextWeatherDict.keys():
                self.nextWeatherDict.update({day: weatherinfo})
                self.graph_data.update({day[0:3]: round(float(temp) - 273.15, 1)})

    def getNextWeather(self, cityname):
        url = f"{self.baseurl2}q={cityname}&appid={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.extract_day_data(data)

            else:
                print('Error')

        except Exception as e:
            return 'Error occured'

    def implementTempGraph(self, cityname):
        xaxis = self.graph_data.keys()
        yaxis = self.graph_data.values()
        yaxis_scale = range(len(yaxis))
        # plt graph configuration
        style.use('dark_background')
        plt.figure(figsize=(5, 5))
        plt.title(f"6 Day Forecast [{cityname.upper()}]")
        plt.xlabel('Days Of The Week')
        plt.ylabel('Temperature (In °C)')
        plt.tight_layout()
        plt.plot(xaxis, yaxis, c='yellow', linestyle="--")
        plt.show()
        # plt.plot(xaxis, yaxis)
        # plt.show()
