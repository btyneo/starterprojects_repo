# gui
import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk

from calculator_logic import Calculator
from tkinter import font
import re
from ttkthemes import ThemedTk

#

calc = Calculator()
currentangle = calc.angle_mode


def create_image(path):
    img = Image.open(path)
    imgtk = ImageTk.PhotoImage(img)
    return imgtk


def create_image_resize(path, dim):
    img1 = Image.open(path).resize(dim)
    img1tk = ImageTk.PhotoImage(img1)
    return img1tk


def extract_numbers_and_fractions(text):
    # Regular expression to match numbers and fractions
    pattern = r'[-+]?\b\d+(\.\d+)?(?:\s*[/\\]\s*\d+(\.\d+)?)?\b'

    # Find all matches in the input text

    matches = re.search(pattern, text)
    if matches:
        return matches.group()
    # elif matches != "":
    #     return "no matches"
    else:
        return ""


def initialize_basic_window():
    root = ThemedTk(theme='scidgrey')
    root.title("MathBox")
    root.geometry("429x520")
    root.resizable(False, False)
    root.configure(background='#242323')

   # base foreground where everything will be needs to be on another canvas
    fg_canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0, background="#363636")
    fg_canvas.grid(column=0, columnspan=6, row=0, rowspan=6, sticky='nsew', padx=17, pady=27)
    fg = create_image(r"C:\Users\hamza\Downloads\extrafilespython\cakc\fg1.png")
    canvas_fg = tk.Label(fg_canvas, image=fg, highlightthickness=0, borderwidth=0)
    canvas_fg.image = fg
    canvas_fg.grid(sticky='nsew')
    # create buttons
    buttons_implementation(fg_canvas, fg)

    root.mainloop()


def buttons_implementation(fg_canvas, fg):
    # Create a frame to hold the display
    display_frame = tk.Frame(fg_canvas, bd=0, highlightbackground="#303b46", highlightthickness=0,
                             height=fg_canvas.winfo_reqheight() // 4,
                             width=fg_canvas.winfo_width() + 395, background="#363636")
    display_frame.grid(column=0, columnspan=5, row=0, sticky='n', pady=18)
    # frame for functions (sin cos tan log)
    function_frame = tk.Frame(fg_canvas, bd=0, highlightthickness=0, borderwidth=0,
                              height=display_frame.winfo_height() + 40, width=display_frame.winfo_width() + 380,
                              background="#545252")
    function_frame.grid(column=0, columnspan=5, row=0, sticky='n', pady=80)

    # frame for buttons (1 2 3 4 etc)
    buttons_frame = tk.Frame(fg_canvas, bd=0, highlightthickness=0, borderwidth=0, height=300, width=398,
                             background="#363636")
    buttons_frame.grid(column=0, columnspan=5, pady=15, row=0, sticky='s')

    # add function buttons
    func = ['sin', 'cos', 'tan', 'log', 'sin-1', 'cos-1', 'tan-1', 'ln', f'Angle Mode: {calc.angle_mode}', 'S>D']

    buttons_font = font.Font(family='Arial', size=13, weight='normal', slant='roman')
    buttons_font1 = font.Font(family='Helvica', size=13, weight='normal', slant='roman')
    # Create a label to display the selected function and user input

    display_label = tk.Label(display_frame, text="", font=buttons_font, anchor='e', padx=10, width=35)
    display_label.pack(fill='both', expand=True, pady=10)
    current_text = ""

    def onbuttonclick(value):

        global current_text
        current_text = display_label.cget('text')
        if value == 'C':
            display_label.config(text="")
        elif value == 'DEL':
            display_label.config(text=str(current_text)[:-1])
        elif value == 'x²':
            result = calc.squared(float(extract_numbers_and_fractions(str(current_text))))
            display_label.config(text=result)
        elif value == '=':
            try:
                result = eval(current_text)
                display_label.config(text=result)
            except Exception as e:
                display_label.config(text='Error!')

        else:
            display_label.config(text=(str(current_text) + str(value)))

    def onfuncclick(func, button):

        current_wholetext = display_label.cget('text')
        current_number = extract_numbers_and_fractions(str(current_wholetext))
        if current_number:
            if '/' in str(current_wholetext):
                numerator, denominator = map(float, current_number.split('/'))
                current_number = numerator / denominator
            elif current_number != "":
                current_number = float(current_number)


        # display_label.config(text=f"{func}({current_text})")

        if func == 'sin':
            result = calc.sin(current_number)
        elif func == 'sin-1':
            result = calc.sininverse(current_number)
        elif func == 'cos':
            result = calc.cos(current_number)
        elif func == 'cos-1':
            result = calc.cosinverse(current_number)
        elif func == 'tan':
            result = calc.tan(current_number)
        elif func == 'tan-1':
            result = calc.taninverse(current_number)
        elif str(func).startswith('Angle Mode'):
            if calc.angle_mode == 'radians':
                calc.set_angle_mode('degrees')
            elif calc.angle_mode == 'degrees':
                calc.set_angle_mode('radians')
            result = f'Mode Changed To {calc.angle_mode}'
            button.config(text=f"Angle Mode: {calc.angle_mode}")
        elif func == 'S>D':
            if '°' not in str(current_wholetext) and 'radians' not in str(current_wholetext):
                if '.' in str(current_number):
                    result = calc.decimal_fraction_conversion(current_number)
                else:
                    result = calc.fraction_decimal_conversion(current_number)
            else:
                result = current_wholetext
        elif func == 'log':
            result = calc.log(current_number)

        elif func == 'ln':
            result = calc.ln(current_number)
        else:
            return 'error'
        display_label.config(text=result)

    for i, funcname in enumerate(func):
        row = i // 4
        column = i % 4
        button = tk.Button(function_frame, text=funcname, pady=5, padx=5, font=buttons_font, background="#7D7D7D",
                           foreground="black")  # add display function
        button.config(command=lambda func=funcname, button1=button: onfuncclick(func, button1))
        if funcname.startswith('Angle Mode'):
            row += 1
            column += 1
        if funcname == 'S>D':
            row += 1
            column += 1

        button.grid(row=row, column=column, padx=6, pady=5, sticky='nsew')

    # other buttons
    buttons = [1, 2, 3, '+', 'C',
               4, 5, 6, '-', 'DEL',
               7, 8, 9, '*', 'x²',
               'π', 0, '.', '/', '=']
    bgbutton = '#7D7D7D'
    fgbutton = 'white'
    for i, button in enumerate(buttons):
        if button == 'C':
            fgbutton = 'white'
            bgbutton = 'orange'
        elif button in ['+', '-', '*', '=', '/', 'π']:
            bgbutton = '#7D7D7D'
            fgbutton = 'white'

        else:
            bgbutton = '#7D7D7D'
            fgbutton = 'white'
        button1 = tk.Button(buttons_frame, text=button, pady=5, padx=5, font=buttons_font1, background=bgbutton,
                            foreground=fgbutton)
        if button == 'π':
            button = 3.1415
        button1.config(command=lambda val=button: onbuttonclick(val))
        button1.grid(row=i // 5, column=i % 5, padx=10, pady=5, sticky='nsew')


if __name__ == "__main__":
    initialize_basic_window()
