from tkinter import *
import pandas
from random import choice

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')
current_card = {}


# ------------Functions------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    card.itemconfig(card_title, text='French', fill='black')
    card.itemconfig(card_word, text=current_card['French'], fill='black')
    card.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card.itemconfig(card_image, image=card_back_img)
    card.itemconfig(card_title, text='English', fill='white')
    card.itemconfig(card_word, text=current_card['English'], fill='white')


def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)


# -------------- [UI] ----------------- #
# ------------- window ---------------- #
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg='#B1DDC6')
flip_timer = window.after(3000, func=flip_card)
# -------------- card ----------------- #
card = Canvas(height=526, width=800)
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
card_image = card.create_image(400, 263, image=card_front_img)

card_title = card.create_text(400, 150, text='Title', font=('Ariel', 40, 'italic'))
card_word = card.create_text(400, 263, text='word', font=('Ariel', 60, 'bold'))

card.config(bg='#B1DDC6', highlightthickness=0)
card.grid(row=0, column=0, columnspan=2)
# -------------- buttons -------------- #
wrong_image = PhotoImage(file='images/wrong.png')
right_image = PhotoImage(file='images/right.png')
button_wrong = Button(image=wrong_image, highlightthickness=0, command=next_card)
button_wrong.grid(column=0, row=1)
button_right = Button(image=right_image, highlightthickness=0, command=is_known)
button_right.grid(column=1, row=1)

next_card()

window.mainloop()
