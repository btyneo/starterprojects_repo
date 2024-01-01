import datetime
import random
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk
from weather_app import WeatherClass
import re


# make different color schemes depending on the time of day; morning/afternoon, evening, night --> 3 different color schemes
# add different images of backgrounds depending on rain/sun/clear/etc

# styles

def regex(str):
    re.compile = (r'')


def create_image(loc):
    image = Image.open(fr"C:\Users\hamza\Downloads\pics\{loc}")
    imagetk = ImageTk.PhotoImage(image)
    return imagetk


def create_image_resize(loc, dimensions):
    image = Image.open(fr"C:\Users\hamza\Downloads\pics\{loc}").resize(dimensions)
    imagetk = ImageTk.PhotoImage(image)
    return imagetk


def display_next_weather_info(cityname, weather_object, baseframe):
    # creating images for the weather displays
    sunny = create_image_resize('sunny.png', (70, 40))
    rain = create_image_resize('rain.png', (70, 40))
    fog = create_image_resize('fog.png', (70, 40))
    clear = create_image_resize('clear.png', (70, 40))
    thunderstorm = create_image_resize('thunderstorm.png', (70, 40))
    snow = create_image_resize('snow.png', (70, 40))

    nexttext_style = ttk.Style()
    nexttext_style.configure("next.TLabel",
                             foreground='#e9eff5', background='#76d0f5',  # Background color
                             font=('Merriweather', 16), relief='ridge')
    nextweather_bg = create_image_resize('gradient2.png', (900, 200))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    currentdatetime = datetime.datetime.now()
    currentday = currentdatetime.strftime('%A')
    index = (days.index(currentday) + 1)
    weather_object.getNextWeather(cityname)

    # nextdays canvas
    nextweather_canvas = tk.Canvas(baseframe, borderwidth=0, highlightthickness=0, background='black', height=200)
    nextweather_canvas.grid(row=0, rowspan=2, column=0, columnspan=5, padx=90, pady=25, sticky='swe')
    bg_display = tk.Label(nextweather_canvas, borderwidth=0, highlightthickness=0, image=nextweather_bg)
    bg_display.image = nextweather_bg
    bg_display.grid(sticky='nsew')

    x = 0
    xcoord = 30
    ycoord = 60
    ycoord2 = 5
    xcoord2 = 45
    while x <= 3:
        if index > 6:
            index = 0

        nextweather_label = ttk.Label(nextweather_canvas, style="next.TLabel",
                                      text=f' {days[index]}: \n\n {[weather_object.nextWeatherDict[days[index]][0]]},'
                                           f'\n\n{[weather_object.nextWeatherDict[days[index]][1]]}')
        nextweather_label.place(x=xcoord, y=ycoord)
        # adding symbol pics
        weather_next = [weather_object.nextWeatherDict[days[index]][0]]
        if weather_next in [['clear'], ['Clear'], ['Clouds'], ['Cloudy']]:
            image = clear
        elif weather_next in [['sunny'], ['Sunny'], ['hot'], ['Hot']]:
            image = sunny
        elif weather_next in [['Rain'], ['Raining'], ['Drizzle'], ['Heavy rain'], ['Heavy Rain']]:
            image = rain
        elif weather_next in [['Snow'], ['Hail']]:
            image = snow
        elif weather_next in [['Storm'], ['Thunderstorm']]:
            image = thunderstorm
        elif weather_next in [['Mist'], ['Fog'], ['Haze'], ['Smoke']]:
            image = fog
        else:
            image = sunny

        label_pic = tk.Label(nextweather_canvas, image=image, borderwidth=0, highlightthickness=0, background="#87CEEB")
        label_pic.image = image
        label_pic.place(x=xcoord2, y=ycoord2)

        # add showing functionality here

        index += 1
        x += 1
        xcoord += 250
        xcoord2 += 250


def display_weather_info(cityname, weathercanvas, baseimagelabel, baseframe):
    # images
    # rain, clouds, sunny, clear, fog, thunderstorm, snow
    rain = create_image('rain.jpg')
    baseimage = create_image('initial_bg.jpg')
    clouds = create_image('clouds.jpg')
    sunny = create_image('sunny.jpg')
    thunderstorm = create_image('thunderstorm.jpg')
    snow = create_image('snow.jpg')
    smoke = create_image('smoke.jpg')

    currenttext_style = ttk.Style()
    currenttext_style.configure("current.TLabel",
                                foreground='black', background='#d49f26',  # Background color
                                font=('Segoe UI', 13), relief='sunken')

    weather_object = WeatherClass()
    weatherinfo = weather_object.getCurrentWeather(cityname)

    # changing bg depending on weather

    if str(weatherinfo['weather']).lower() in ['rain', 'thunderstorm', 'storm', 'rain clouds', 'drizzle', 'raining']:
        image = rain
    elif str(weatherinfo['weather']).lower() in ['clear', 'clear sky', 'clouds', 'cloud']:
        rand = random.randint(0, 2)
        if rand == 0:
            image = clouds
        else:
            image = sunny
    elif str(weatherinfo['weather']).lower() in ['snow', 'hail']:
        image = snow
    elif str(weatherinfo['weather']).lower() in ['smoke', 'haze', 'fog', 'mist']:
        image = smoke
    else:
        rand = random.randint(0, 2)
        if rand == 0:
            image = clouds
        else:
            image = smoke

    baseimagelabel.configure(image=image)
    baseimagelabel.image = image

    # country, city
    location_text = ttk.Label(weathercanvas,
                              text=f"{cityname.upper()}, {weatherinfo['country']}",
                              borderwidth=0, background="#d49f26", foreground='white', style='current.TLabel')

    location_text.place(x=130, y=5)

    # weather and temp
    weather_text = ttk.Label(weathercanvas,
                             text=f"Weather: {weatherinfo['weather']}                Temperature : {weatherinfo['temp']}",
                             borderwidth=0, background="#d49f26", foreground='white', style='current.TLabel')

    weather_text.place(x=5, y=40)
    # temp min temp max
    temp_text = ttk.Label(weathercanvas,
                          text=f"Temp Min: {weatherinfo['temp_min']}                Temp Max : {weatherinfo['temp_max']}",
                          borderwidth=0, background="#d49f26", foreground='white', style='current.TLabel')

    temp_text.place(x=5, y=80)

    # you can add sunset etc here too but i was having trouble with timezones so for now i added visibility and wind_speed instead
    # visiblity_
    visibility_text = ttk.Label(weathercanvas,
                                text=f"Visibility: {weatherinfo['visibility']}             Wind Speed : {weatherinfo['wind_speed']}",
                                borderwidth=0, background="#d49f26", foreground='white', style='current.TLabel')

    visibility_text.place(x=7, y=120)

    def restart():
        inputcity()
        baseframe.destroy()



    def onenter_graph(event):
        graph_button.configure(image=graph_image2)
        graph_button.image = graph_image2

    def onleave_graph(event):
        graph_button.configure(image=graph_image)
        graph_button.image = graph_image

    def onenter_search(event):
        search_button.configure(image=search_image2)
        search_button.image = search_image2

    def onleave_search(event):
        search_button.configure(image=search_image)
        search_button.image = search_image

    # implementing search buttons(goes back to maincode) and button for graph
    graph_image = create_image_resize('graph.png', (40, 30))
    graph_image2 = create_image_resize('graph2.png', (40, 30))
    graph_button = tk.Label(baseframe, borderwidth=0, highlightthickness=0, image=graph_image)
    graph_button.image = graph_image
    graph_button.place(x=729, y=160)
    graph_button.bind("<Enter>", onenter_graph)
    graph_button.bind("<Leave>", onleave_graph)

    search_image = create_image_resize('search.png', (40, 30))
    search_image2 = create_image_resize('search2.png', (40, 30))
    search_button = tk.Label(baseframe, borderwidth=0, highlightthickness=0, image=search_image)
    search_button.image = search_image
    search_button.place(x=313, y=160)
    search_button.bind("<Enter>", onenter_search)
    search_button.bind("<Leave>", onleave_search)

    # calling function for next 6 days forecast
    display_next_weather_info(cityname, weather_object, baseframe)
    graph_button.bind("<Button-1>", lambda event: weather_object.implementTempGraph(cityname))
    search_button.bind("<Button-1>", lambda event: restart())


def inputcity():
    global root
    # root.withdraw() hides the root window
    root.withdraw()
    style_input = ttk.Style()
    style_input.configure("Rounded.TEntry", padding=10, borderwidth=5, relief="flat", background="black",
                          foreground="black", font=('Segoe UI', 14))
    style_text = ttk.Style()
    style_text.configure("text.TLabel",
                         foreground='black', background='#87ceeb',  # Background color
                         font=('Segoe UI', 14), relief='flat')
    style_button = ttk.Style()
    style_button.configure("button.TButton", background="#967bb6", foreground="black", border=0, highlighthtickness=0,
                           relief='raised', font=('Segoe UI', 14))
    input_window = tk.Toplevel()
    input_window.geometry('400x300')
    input_window.resizable(False, False)
    input_window.title('WeatherApp | By HamTech')
    input_window.configure(background='#87ceeb', borderwidth=1, highlightthickness=2, highlightcolor='navy blue')

    # adding small weather symbol

    weather_img = create_image_resize('cloud.png', (100, 70))
    weather_symbol = ttk.Label(input_window, image=weather_img, background='#87ceeb')
    weather_symbol.image = weather_img
    weather_symbol.place(x=40, y=40)
    input_label = ttk.Label(input_window, text='\n\n\nCity Name: ', style='text.TLabel')
    input_label.pack()
    input_box = ttk.Entry(input_window, style='Rounded.TEntry', width=50)
    input_box.pack(pady=10, padx=10)

    # whenever i closed the inputwindow without typing anything, since root is hidden i couldnt type in powershell
    # so i binded this on_window_close function which checks if nothing is returned from inputbox then exit code
    def on_window_close():
        if input_box.get() == "" or not input_box.get():
            exit()

    input_window.protocol("WM_DELETE_WINDOW", on_window_close)

    def getcity_launchapp():
        city1 = input_box.get()
        launch_app(city1)
        input_window.destroy()

    enter_button = ttk.Button(input_window, text='Enter', style='button.TButton', command=getcity_launchapp)
    enter_button.pack(side='bottom', pady=30)


def launch_app(cityname):
    # create a basic canvas to have everything on

    # root.deiconify() shows the hidden root window
    root.deiconify()

    baseframe = tk.Frame(root, bd=0, highlightthickness=0)
    baseframe.grid(column=0, columnspan=3, row=0, rowspan=6, sticky='nsew')

    # setting image of basecanvas

    baseimage = create_image('initial_bg.jpg')
    baseimagelabel = tk.Label(baseframe, image=baseimage, bd=0, highlightthickness=0)
    baseimagelabel.image = baseimage
    baseimagelabel.grid(sticky='nsew')

    # make columns/rows expandable
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    currentweather = tk.Canvas(baseframe, borderwidth=0, highlightthickness=0, bg='#d49f26', height=150)
    currentweather.grid(row=0, column=0, columnspan=1, sticky='n', pady=40)  # Adjust padx and pady
    display_weather_info(cityname, currentweather, baseimagelabel, baseframe)


root = tk.Tk()
root.geometry("1080x450")
root.resizable(False, False)
root.title('WeatherApp | By HamTech')
root.configure()

city = inputcity()

if __name__ == '__main__':
    root.mainloop()
