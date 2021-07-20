import pandas
from tkinter import *
from random import *
import csv


BACKGROUND_COLOR = "#B1DDC6"
random_card = {}

try:
    df_data = pandas.read_csv("left_words.csv", encoding="windows-1250")
    to_learn = df_data.to_dict(orient="records")
except FileNotFoundError:
    df_data = pandas.read_csv("en-pl.csv")
    to_learn = df_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    df_data = pandas.read_csv("en-pl.csv")
    to_learn = df_data.to_dict(orient="records")

if to_learn:
    header = to_learn[0]
else:
    df_data = pandas.read_csv("en-pl.csv")
    to_learn = df_data.to_dict(orient="records")
    header = to_learn[0]


def check_button_pressed():
    if len(to_learn) > 0:
        to_learn.remove(random_card)
        saving_progress()
        next_card()


def saving_progress():
    with open("left_words.csv", "w", encoding="windows-1250") as export_data:
        try:
            writer = csv.DictWriter(export_data, fieldnames=header)
            writer.writeheader()
            for data in to_learn:
                writer.writerow(data)
        except IndexError:
            pass


def inverse_card():
    canvas.itemconfig(lower_text, text=random_card["Polski"])
    canvas.itemconfig(upper_text, text="Polish")
    canvas.itemconfig(image_card, image=card_front_image)


def next_card():
    global flip_timer, random_card
    screen.after_cancel(flip_timer)
    try:
        random_card = choice(to_learn)
    except IndexError:
        canvas.itemconfig(upper_text, text="End of the list.\nTake another database!")
        canvas.itemconfig(lower_text, text="")
    else:
        canvas.itemconfig(upper_text, text="English")
        canvas.itemconfig(image_card, image=card_back_image)
        canvas.itemconfig(lower_text, text=random_card["English"])
        flip_timer = screen.after(3000, func=inverse_card)

# -------------------------- UI SETUP -------------------------#


screen = Tk()
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
screen.title("Flashy")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
image_card = canvas.create_image(10, 10, image=card_back_image, anchor='nw')
canvas.grid(row=0, column=0, columnspan=2)

upper_text = canvas.create_text(400, 150, text="English", font=("Arial", 40, "italic"))
lower_text = canvas.create_text(400, 300, text="Word", font=("Arial", 60, "bold"))


# Buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, bd=1, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, bd=1, highlightthickness=0, command=check_button_pressed)
known_button.grid(row=1, column=1)


flip_timer = screen.after(3000, func=inverse_card)
next_card()
screen.mainloop()
