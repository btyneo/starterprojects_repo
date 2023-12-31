import time
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import sqlite3
import random
import requests
from io import BytesIO
from tkinter import filedialog
import winsound


def buttonsound():
    loc = r"C:\users\hamza\downloads\glitch.wav"
    winsound.PlaySound(loc, winsound.SND_FILENAME | winsound.SND_ASYNC)

def clicksound():
    loc = r"C:\users\hamza\downloads\click1.wav"
    winsound.PlaySound(loc, winsound.SND_FILENAME | winsound.SND_ASYNC)

def techsound():
    loc = r"C:\users\hamza\downloads\tech.wav"
    winsound.PlaySound(loc, winsound.SND_FILENAME | winsound.SND_ASYNC)

def swipesound():
    loc = r"C:\users\hamza\downloads\swipe.wav"
    winsound.PlaySound(loc, winsound.SND_FILENAME | winsound.SND_ASYNC)

criminals = []

courier_font_bold = ("Courier New", 9, "bold")
times_font_italic = ("Courier New", 9, "bold")
georgia_font_normal = ("Georgia", 8, "italic")
helv_font = ("Helvetica", 10, "italic")

new_font = ("Georgia", 14, "normal")

picchar = None


class criminal():
    # add methods to add/remove from the db later
    def __init__(self, name, alias, age, criminal_offence, status, imprisoned, pic):
        self.name = name
        self.alias = alias
        self.age = age
        self.criminal_offence = criminal_offence
        self.status = status
        self.imprisoned = imprisoned
        self.pic = pic


def addtodatabase(name, alias, age, criminal_offence, status, imprisoned, pic):
    connection = sqlite3.connect(r"C:\sqlite\bat_criminals.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO criminals VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (name, alias, age, criminal_offence, status, imprisoned, pic))
    connection.commit()
    connection.close()


def removefromdatabase(name):
    connection = sqlite3.connect(r"C:\sqlite\bat_criminals.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM criminals WHERE name = ?", (name,))
    connection.commit()
    connection.close()


def getinfo():
    global criminals
    conn = sqlite3.connect(r"C:\sqlite\bat_criminals.db")
    c = conn.cursor()
    c.execute("SELECT * FROM criminals")
    for row in c.fetchall():
        criminals.append(
            {"Name": row[0],
             "Alias": row[1],
             "Age": row[2],
             "Criminal Offence": row[3],
             "Status": row[4],
             "Imprisoned": row[5],
             "Pic": row[6]})

    conn.close()
    return criminals


def begin_program():
    buttonsound()
    # adding new images for show_criminalinfo function
    charbg_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\charbg.png").resize((800, 600))
    charbg_tk = ImageTk.PhotoImage(charbg_path)

    # def show_criminalinfo(name):
    #
    #
    #     char_frame.grid(row=0, column=0, sticky="ne", padx=50, pady=100)
    #     boxlabel.configure(image=charbg_tk)
    #     pic_frame.grid(row=0, column=0, sticky="nw", padx=30, pady=90)  # Place it in the top-right corner
    #
    #     name_label = ttk.Label(char_frame, text=f"Name:   {name}", width=50, borderwidth=0, background="")
    #     name_label.grid(pady=15)
    finalpath = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\pics\012.png").resize((800, 670))
    finaltk = ImageTk.PhotoImage(image=finalpath)

    def refresh():
        global criminals
        criminals = []
        criminals = getinfo()
        for button in buttons_frame.winfo_children():
            button.destroy()

        begin_program()

    home1 = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\home1.png").resize((100, 25))
    home1tk = ImageTk.PhotoImage(home1)
    homeglow = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\homeglow.png").resize((100, 25))
    homeglowtk = ImageTk.PhotoImage(homeglow)

    def show_criminalinfo(name, i):
        clicksound()
        def change(event):
            homebutton.config(image=homeglowtk)

        def changeback(event):
            homebutton.config(image=home1tk)

        # Clear existing labels
        for widget in char_frame.winfo_children():
            widget.destroy()
        for widget in pic_frame.winfo_children():
            widget.destroy()

        # boxlabel.configure(image=charbg_tk)

        # Display background image and configure frames

        # add_button.grid(row=2, column=0, pady=20, padx=20, sticky="w")
        # char_canvas.update_idletasks()
        addlabel.destroy()
        removelabel.destroy()

        homebutton = tk.Label(char_canvas, borderwidth=0, highlightthickness=0, image=home1tk)
        homebutton.place(x=690, y=20)
        homebutton.bind("<Button-1>", lambda event: refresh())

        homebutton.bind("<Enter>", change)
        homebutton.bind("<Leave>", changeback)

        char_frame.configure(highlightthickness=0, borderwidth=0, background="", width=630, height=300)
        char_frame.grid(row=0, column=0, sticky="ne", padx=30, pady=130)

        boxlabel.configure(image=finaltk)
        pic_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=100)
        pic_frame.config(height=400)

        # Display criminal information
        criminal_info = list1  # Replace this with your actual function to get info
        name_label = tk.Label(char_frame, text=f"Name:      {name}", width=31, borderwidth=0,
                              font=new_font, highlightthickness=0, background="#0c343d", foreground="cyan")
        name_label.pack(pady=15)
        alias_label = tk.Label(char_frame, text=f"Alias:      {criminals[i]['Alias']}", width=32, borderwidth=0,
                               font=new_font, highlightthickness=0, background="#0c343d", foreground="cyan")
        alias_label.pack(pady=15)
        age_label = tk.Label(char_frame, text=f"Age:      {criminals[i]['Age']}", width=32, borderwidth=0,
                             font=new_font, highlightthickness=0, background="#0c343d", foreground="cyan")
        age_label.pack(pady=15)
        criminalo_label = tk.Label(char_frame, text=f"Criminal Offence:     \n {criminals[i]['Criminal Offence']}",
                                   width=32, borderwidth=0,
                                   font=new_font, highlightthickness=0, background="#0c343d", foreground="cyan")
        criminalo_label.pack(pady=15)
        status_label = tk.Label(char_frame, text=f"Status:      {criminals[i]['Status']}", width=32, borderwidth=0,
                                font=new_font, highlightthickness=0, background="#0c343d", foreground="cyan")
        status_label.pack(pady=15)
        imprisoned_label = tk.Label(char_frame, text=f"Imprisoned:      {criminals[i]['Imprisoned']}", width=32,
                                    borderwidth=0,
                                    font=new_font, highlightthickness=0, background="#0c343d", foreground="cyan")
        imprisoned_label.pack(pady=15)

        picpath = criminals[i]['Pic']
        pic1 = Image.open(picpath).resize((pic_frame.winfo_reqwidth(), pic_frame.winfo_reqheight()))
        pic1tk = ImageTk.PhotoImage(pic1)

        pic_label = tk.Label(pic_frame, highlightthickness=0, borderwidth=0, image=pic1tk)
        pic_label.image = pic1tk
        pic_label.grid()

        # Create and display other labels for criminal information
        # Example:
        # age_label = ttk.Label(pic_frame, text=f"Age: {criminal_info['Age']}", style="customlabel")
        # age_label.pack(pady=10)
        # # Add more labels as needed for other information

    def limit_scroll(event):
        canvas_for_inner_frame.yview_scroll(-1 * int(event.delta / 120), "units")

        # Get the total height of the buttons
        # this basically means that total height = buttonsframe height + height for another button
        total_buttons_height = buttons_frame.winfo_height() + (buttons_frame.winfo_reqheight() // len(list1))

        # Set the scroll region based on the total height of the buttons
        canvas_for_inner_frame.configure(scrollregion=(0, 0, width_third, total_buttons_height))

    new_bgpath = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\newest.jpg")
    new_bg = ImageTk.PhotoImage(image=new_bgpath)

    global canvas
    canvas.destroy()
    canvas1 = tk.Canvas(root, width=1338, height=643, highlightthickness=0)
    canvas1.grid(column=0, columnspan=4, row=0, sticky="nsew")
    canvas1.columnconfigure(0, weight=1)
    canvas1.rowconfigure(0, weight=1)
    # setting bg image as a label
    bglabel = tk.Label(canvas1, image=new_bg)
    bglabel.image = new_bg
    bglabel.grid()

    # setting frames as sections inside this canvas
    # first namescanvas

    # here we create a frame which has the width of 1/3rd of the canvas and complete height of canvas, then we
    # do sticky='nw' so it forms on the left side. we also give some extra space by using padx pady
    width_third = canvas1.winfo_reqwidth() // 3  # Calculate 1/3rd of canvas width
    namescanvas = tk.Canvas(canvas1, width=width_third, height=canvas1.winfo_reqheight(), background="black",
                            highlightthickness=0, borderwidth=0)
    namescanvas.grid(column=0, row=0, sticky="nw", padx=25, pady=25)
    # Remove frame background color and border

    transparent_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\gradient.png").resize((450, 700))
    transparent_img = ImageTk.PhotoImage(transparent_path)

    # setting image for background

    transparencylabel = tk.Label(namescanvas, image=transparent_img, highlightthickness=0, borderwidth=0,
                                 background="black")
    transparencylabel.image = transparent_img
    transparencylabel.grid()
    # transparencylabel.place(x=0, y=0, relwidth=1, relheight=1)

    # getting info and displaying it
    heightneeded = namescanvas.winfo_reqheight()
    list1 = getinfo()
    list1[0]["Name"] = "Criminals: "
    # Create an inner frame for the buttons
    inner_frame = tk.Frame(namescanvas, borderwidth=0, highlightthickness=0, background="", width=width_third
                           , height=heightneeded)
    inner_frame.grid(row=0, column=0, sticky="nw", padx=15, pady=15)

    # Create a canvas for scrolling inside the inner frame
    canvas_for_inner_frame = tk.Canvas(inner_frame, borderwidth=0, highlightthickness=0, height=heightneeded)
    canvas_for_inner_frame.pack(side="left", fill="y", padx=20)

    # Create a frame to hold the buttons inside the canvas
    buttons_frame = tk.Frame(canvas_for_inner_frame, background="")

    # Add buttons to the buttons_frame
    for i, criminal in enumerate(list1):
        if i != 0:
            name1 = criminal["Name"]
            button = tk.Button(buttons_frame, text=name1, padx=10, pady=20, borderwidth=1, highlightthickness=0,
                               background="black",
                               foreground="white", width=width_third // 9, font=helv_font)
            button.grid(row=i, column=0, sticky="w")
            # button.bind_all("<Button-1>", lambda event, i=i: show_criminalinfo(i))
            button.bind("<Button-1>", lambda event, i=i, name=name1: show_criminalinfo(name, i))

    totalbuttonsheight = len(list1) * 21

    # right side of canvas
    char_canvas = tk.Canvas(root, width=(2 / 3) * root.winfo_width() - 100, height=root.winfo_height(),
                            highlightthickness=0, borderwidth=0, background="black")
    # Covering the right side of the window
    # image for canvas
    box_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\px1.png").resize((800, 600))
    boxtk = ImageTk.PhotoImage(box_path)

    boxlabel = tk.Label(char_canvas, image=boxtk, highlightthickness=0, borderwidth=0)
    boxlabel.image = boxtk
    boxlabel.grid()
    char_canvas.grid(row=0, column=1, sticky="ne", padx=40, pady=30)
    char_canvas.columnconfigure(0, weight=1)  # Make the content expand to fill the canvas horizontally

    # -------------------
    addglow = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\addstroke.png")
    addglowtk = ImageTk.PhotoImage(addglow)
    remglow = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\removehover.png")
    remglowtk = ImageTk.PhotoImage(remglow)
    insertbg = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\blurred.jpg").resize((748, 550))
    insertbgtk = ImageTk.PhotoImage(insertbg)

    def removefrom():
        clicksound()
        root2 = tk.Toplevel()
        root2.title("Inserting Data: ")
        root2.geometry("748x550")

        bg_label = tk.Label(root2, image=insertbgtk)
        bg_label.image = insertbgtk
        bg_label.place(relwidth=1, relheight=1)

        nameframe = tk.Frame(root2)
        nameframe.pack(pady=200)
        namelabel = tk.Label(nameframe, text="Enter Name To Remove: ", background="black", foreground="white",
                             font=georgia_font_normal)
        namelabel.pack(side="left")
        namebox = tk.Entry(nameframe, highlightcolor="grey", highlightthickness=1, background="black",
                           foreground="white",
                           width=40, borderwidth=0)
        namebox.pack(side="left")

        removebutton = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        removebutton.pack(pady=10)

        def remove1():
            nametoremove = namebox.get()
            print(nametoremove)
            removefromdatabase(nametoremove)
            time.sleep(1.8)
            swipesound()
            root2.destroy()
            refresh()

        remove_button = tk.Button(removebutton, text="Remove Character!",
                                  command=remove1)
        remove_button.pack(side="left")

        root2.mainloop()

    def insertinto():
        clicksound()
        global picchar
        status = False
        root2 = tk.Toplevel()
        root2.title("Inserting Data: ")
        root2.geometry("748x550")

        bg_label = tk.Label(root2, image=insertbgtk)
        bg_label.image = insertbgtk
        bg_label.place(relwidth=1, relheight=1)
        # frames; name,alias,age,criminal_offence,status,imprisoned,pic

        # 1

        insertframe1 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe1.pack(pady=25)
        namelabel = tk.Label(insertframe1, text="Name: ", font=georgia_font_normal, width=10, background="black",
                             foreground="white")
        namelabel.pack(side="left")
        inputbox1 = tk.Entry(insertframe1, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox1.pack(side="left")

        # 2

        insertframe2 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe2.pack(pady=25)
        namelabel1 = tk.Label(insertframe2, text="Alias: ", font=georgia_font_normal, width=10, background="black",
                              foreground="white")
        namelabel1.pack(side="left")
        inputbox2 = tk.Entry(insertframe2, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox2.pack(side="left")

        # 3
        insertframe3 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe3.pack(pady=25)
        namelabel2 = tk.Label(insertframe3, text="Age: ", font=georgia_font_normal, width=10, background="black",
                              foreground="white")
        namelabel2.pack(side="left")
        inputbox3 = tk.Entry(insertframe3, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox3.pack(side="left")

        # 4
        insertframe4 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe4.pack(pady=25)
        namelabel3 = tk.Label(insertframe4, text="Criminal Offence: ", font=georgia_font_normal, width=15,
                              background="black",
                              foreground="white")
        namelabel3.pack(side="left")
        inputbox4 = tk.Entry(insertframe4, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox4.pack(side="left")

        # 5
        insertframe5 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe5.pack(pady=25)
        namelabel4 = tk.Label(insertframe5, text="Status ", font=georgia_font_normal, width=10,
                              background="black",
                              foreground="white")
        namelabel4.pack(side="left")
        inputbox5 = tk.Entry(insertframe5, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox5.pack(side="left")

        # 6
        insertframe6 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe6.pack(pady=25)
        namelabel5 = tk.Label(insertframe6, text="Imprisoned: ", font=georgia_font_normal, width=10,
                              background="black",
                              foreground="white")
        namelabel5.pack(side="left")
        inputbox6 = tk.Entry(insertframe6, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox6.pack(side="left")

        # 7
        insertframe7 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe7.pack(pady=25)
        namelabel6 = tk.Label(insertframe7, text="Picture File Path: ", font=georgia_font_normal, width=15,
                              background="black",
                              foreground="white")
        namelabel6.pack(side="left")
        inputbox7 = tk.Entry(insertframe7, width=30, background="black", foreground="white", highlightcolor="grey",
                             highlightthickness=1)
        inputbox7.pack(side="left")

        # getting #frames; name,alias,age,criminal_offence,status,imprisoned,pic
        def submit():
            # To modify the 'status' variable from outer scope
            name = inputbox1.get()
            alias = inputbox2.get()
            age = inputbox3.get()
            criminalo = inputbox4.get()
            status = inputbox5.get()
            imprisoned = inputbox6.get()
            pic = inputbox7.get()

            addtodatabase(name, alias, age, criminalo, status, imprisoned, pic)
            time.sleep(1.9)
            swipesound()
            root2.destroy()
            refresh()

        # submit
        insertframe8 = tk.Frame(root2, highlightthickness=0, borderwidth=0, height=10, width=55, background="black")
        insertframe8.pack(pady=10)

        submit_button = tk.Button(insertframe8, text="Submit!",
                                  command=submit)
        submit_button.pack(side="left")

        root2.mainloop()

    def on_enter1(event):
        addlabel.config(image=addglowtk)

    def on_leave1(event):
        addlabel.config(image=addtk)

    def on_enter2(event):
        removelabel.config(image=remglowtk)

    def on_leave2(event):
        removelabel.config(image=removetk)

    add = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\add.png")
    addtk = ImageTk.PhotoImage(add)
    addlabel = tk.Label(char_canvas, image=addtk, highlightthickness=0, borderwidth=0, background="grey")
    addlabel.image = addtk
    addlabel.grid(row=0, column=0, sticky="sw", pady=50, padx=50)
    addlabel.bind("<Enter>", on_enter1)
    addlabel.bind("<Leave>", on_leave1)
    addlabel.bind("<Button-1>", lambda event: insertinto())

    remove = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\remove.png")
    removetk = ImageTk.PhotoImage(remove)
    removelabel = tk.Label(char_canvas, image=removetk, highlightthickness=0, borderwidth=0, background="black")
    removelabel.image = removetk
    removelabel.bind("<Enter>", on_enter2)
    removelabel.bind("<Leave>", on_leave2)
    removelabel.bind("<Button-1>", lambda event: removefrom())
    removelabel.grid(row=0, column=0, sticky="se", pady=65, padx=13)

    # creating frames inside the canvas for pics, labels for names etc
    # then just adjust/update it inside the showcriminalinfo function
    pic_frame = tk.Frame(char_canvas, width=350, height=190, borderwidth=0, highlightbackground="grey",
                         highlightcolor="black", highlightthickness=1)

    # ---------------------------------
    style = ttk.Style()
    style.configure("customlabel", font=courier_font_bold, background="black", foreground="white", padding=10)
    char_frame = tk.Frame(char_canvas, highlightthickness=0, borderwidth=0, background="", width=630, height=300)

    #
    # #add remove buttons
    # add_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\add.png")
    # add_tk = ImageTk.PhotoImage(add_path)
    # # Create the add button with the image
    # add_button = tk.Button(char_frame, image=add_tk, highlightthickness=0, borderwidth=0, height=100, width=100)
    # add_button.image = add_tk  # Keep a reference to prevent the image from being garbage collected
    # add_button.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")  # Adjust row and column as needed

    # ------------------------------------------------------------------------------------------------------
    # add remove buttons

    # Create the 'buttonscanvas' canvas on top of 'char_canvas'
    # add_image = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\add.png")
    # add_image_tk = ImageTk.PhotoImage(add_image)

    # Update the canvas to display the image

    # addlabel = char_canvas.create_image(660, 480, add_tk)
    # addlabel.image = add_tk

    # char_canvas.grid_rowconfigurelea(char_canvas.grid_size()[1] - 1, weight=1)
    # addremove_canvas = tk.Canvas(char_canvas, height=80, borderwidth=0, highlightthickness=0)
    # addremove_canvas.grid(row=char_canvas.grid_size()[-1], column=0, columnspan=char_canvas.grid_size()[0],
    #                       sticky="nsew",
    #                       pady=10, padx=10)
    #
    # # Adjust the row and column span to fill the entire width of char_canvas
    # addremove_canvas.grid(row=char_canvas.grid_size()[-1], column=0, columnspan=char_canvas.grid_size()[0],
    #                       sticky="nsew")
    # add_button = tk.Label(char_canvas, borderwidth=0, highlightthickness=0, image=add_tk)
    # add_button.image = add_tk
    # add_button.grid()

    # Configure canvas to scroll
    canvas_for_inner_frame.update_idletasks()  # Update to reflect changes
    canvas_for_inner_frame.config(scrollregion=canvas_for_inner_frame.bbox("all"))
    canvas_for_inner_frame.config(scrollregion=(0, 0, width_third, totalbuttonsheight))
    canvas_for_inner_frame.bind_all("<MouseWheel>", limit_scroll)
    canvas_for_inner_frame.create_window((0, 0), window=buttons_frame, anchor="nw")

    # # Create a scrollbar
    # scrollbar = tk.Scrollbar(inner_frame, command=canvas_for_inner_frame.yview)
    # scrollbar.pack(side="right", fill="y")
    # canvas_for_inner_frame.config(yscrollcommand=scrollbar.set)


# ---------------------------------------------------------------------------------------------------
root = tk.Tk()
downloaded_font = font.Font(family="GothamKnights", size=14)
root.title("BatApp | By WayneTech")
root.geometry("1338x643")
root.resizable(False, False)

# Import an image with transparency
logo_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\logoglow.png").resize((640, 240))
logo_tk = ImageTk.PhotoImage(logo_path)

# Background image
bg_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\newest.jpg").resize((1338, 643))
bg_tk = ImageTk.PhotoImage(bg_path)

# button image
button_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\begin.png")
button_tk = ImageTk.PhotoImage(button_path)

# Canvas
canvas = tk.Canvas(root, highlightthickness=0, borderwidth=0, background="blue")
canvas.grid(column=0, columnspan=3, row=0, sticky="nsew")  # Stretch canvas across columns

# Display the background image on the canvas
bg_image = canvas.create_image(0, 0, image=bg_tk, anchor="nw")

# Display the logo on the canvas
logo_image = canvas.create_image(665, 210, image=logo_tk)  # Adjust the position as needed
#
# # button
# # Create a button and add it to the canvas
# button = tk.Button(canvas, image=button_tk, borderwidth=0, highlightthickness=0, command=begin_program)
# button.place(x=400, y=400)
# Create a custom button using a Canvas
# base image
button_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\initiate2.png")
button_tk = ImageTk.PhotoImage(button_path)
# hover image
glow_path = Image.open(r"C:\Users\hamza\Downloads\extrafilespython\batapp\initiate4.png")
glow_tk = ImageTk.PhotoImage(glow_path)

button = canvas.create_image(660, 480, image=button_tk)  # Create button image on canvas


def on_enter(event):
    canvas.itemconfig(button, image=glow_tk)


def on_leave(event):
    canvas.itemconfig(button, image=button_tk)


# Bind click event to the button

canvas.tag_bind(button, "<Button-1>", lambda event: begin_program())
# hover events to button
canvas.tag_bind(button, "<Enter>", on_enter)
canvas.tag_bind(button, "<Leave>", on_leave)

# Configure row and column weights to make canvas stretch
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

if __name__ == "__main__":
    root.mainloop()
