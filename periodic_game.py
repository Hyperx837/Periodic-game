import tkinter as tk
from tkinter.messagebox import showwarning
import random
import time

import periodictable


def is_correct():
    destroying_elements = 'show_result answer hint'.split()
    for el in destroying_elements:
        # globals()[el] = el
        print(el in globals())
        if el in globals():
            globals()[el].destroy()

    entered_symbol = enter_symbol.get()
    # enter_symbol.delete(0, 'end')

    if answerable and is_valid(entered_symbol):
        if entered_symbol == element.symbol:
            show_result = tk.Label(frame, text='Correct!', font='arial 14')
            show_result.place(x=200, y=150)

        else:
            show_result = tk.Label(frame, text='Wrong!', font='arial 14')
            show_result.place(x=200, y=150)
            globals()['wrong'] += 1
            hint = give_hint(element, entered_symbol)
            hint.place(x=150, y=300)
            if globals()['wrong'] > 4:
                for slave in frame.place_slaves():
                    slave.destroy()

                tk.Label(frame, text='You Lost (5 Unsuccessful tries)', font='arial 15').place(x=100, y=150)
                time.sleep(5)
                root.quit()

        globals()['show_result'] = show_result

    elif not is_valid(entered_symbol):
        show_result = tk.Label(frame, text=f'Invalid Atomic Symbol "{entered_symbol}"', font='arial 14')
        show_result.place(x=150, y=150)
        globals()['show_result'] = show_result

    else:
        showwarning(title='Unanswerable', message='entered a revealed answer.')
        return

    print(type(globals()['show_result']))


def is_valid(element):
    return element in [el.symbol for el in periodictable.elements]


def new_question():
    for widget in 'show_number', 'answer':
        if widget in globals():
            globals()[widget].destroy()


    answerable = True
    number = random.randint(1, 118)
    question = f'which element has the atomic number {number}?'
    element = periodictable.elements[number]
    # correct_answer = element.symbol, element.name.title()

    show_number = tk.Label(frame, text=question, font='italic 15', bg='yellow')
    show_number.place(x=80, y=10)

    for var, val in locals().items():
        globals()[var] = val


def reveal_answer():
    answer = tk.Label(frame, text=f'{element.symbol}: {element.name.title()}',
                      font='bold 15', bg='purple', fg='yellow')
    answer.place(x=200, y=250)
    globals()['answer'] = answer
    globals()['answerable'] = False
    # new_question()


def give_hint(element, user):
    element_no, user_no = element.number, number2element[user]
    if element_no > user_no:
        text = 'higher than the entered element'

    else:
        text = 'lower then the entered element'

    globals()['hint'] = tk.Label(frame, text=f'Hint: {text}', font='arial 15')
    return globals()['hint']


wrong = 0
number2element = {element.symbol: element.number for element in periodictable.elements}

root = tk.Tk()
root.geometry('600x600')
root.title('Learn Periodic-Table')

frame = tk.Frame(root, height=500, width=520, bg='red')
frame.place(x=40, y=40)

new_question()

tk.Label(frame,
         text='(enter the symbol of the element)',
         font='bold 15',
         bg='yellow').place(x=110, y=40)

enter_symbol = tk.Entry(frame,
                        font='times 15',
                        width=5)
enter_symbol.place(x=210, y=100)

submit_button = tk.Button(frame, text='submit',
                          command=is_correct)
submit_button.place(x=264.4, y=100)

options = tk.Label(frame, text='Options:', font='arial 16', bg='black', fg='white')
options.place(x=20, y=200)

get_answer = tk.Button(frame, text='Get Answer', font='arial 10',
                       command=reveal_answer)
get_answer.place(x=130, y=200)

generate_new = tk.Button(frame, text='Next Question', font='arial 10', command=new_question)
generate_new.place(x=220, y=200)

tk.Button(frame, text='Quit', font='arial 10', command=root.quit).place(x=350, y=200)
# todo: add hints

root.mainloop()
