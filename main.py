from tkinter import *
import pandas
import random

'''
This program is a simple GUI for flash cards. 
For the very first time user, the program will use the provided french_words.csv file.
If the user clicks check_mark to acknowledge a word is known, 
it is remove from the file and the rest are added to a new CSV file.
After that, the program will use words added to a new file to create flash cards.
'''

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
data_dict = {}

# Get words from word_to_learn.csv file.
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # If word_to_learn.csv doesn't exist yet, use french_words.csv.
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    # When next_card function is called, cancel flip_timer so that the card doesn't flip to show answer.
    window.after_cancel(flip_timer)
    # Get randomly chosen card from data dictionary.
    current_card = random.choice(data_dict)
    # Show card in French.
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"])
    # Show front image.
    canvas.itemconfig(card_background, image=front_photo)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    # Show back image with answer in English.
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"])
    canvas.itemconfig(card_background, image=back_image)


def word_learned():
    # If user knows the current word, remove it from the dictionary.
    data_dict.remove(current_card)
    # Save the remaining data into a new CSV file.
    data_to_save = pandas.DataFrame(data_dict)
    data_to_save.to_csv("data/words_to_learn.csv", index=False)
    # Also trigger next_card function.
    next_card()


# Create a GUI with desired title.
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Flip card after 5s to show the answer.
flip_timer = window.after(5000, func=flip_card)

# Use Canvas class to add front img and back img to the GUI.
canvas = Canvas(width=800, height=526)
front_photo = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_photo)
# Title and word are added later.
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Create buttons for check_mark and cross_img.
cross_image = PhotoImage(file="images/wrong.png")
# When cross_img is clicked, triggers just next_card func.
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)
check_mark_image = PhotoImage(file="images/right.png")
# When check_mark is clicked, triggers both word_learned and next card funcs.
check_mark_button = Button(image=check_mark_image, highlightthickness=0, command=word_learned)
check_mark_button.grid(column=1, row=1)

# Call the func so that the very first page starts displaying words.
next_card()
# To keep displaying.
window.mainloop()

