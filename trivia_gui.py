import PySimpleGUI as sg
import json
from trivia_questions import get_questions, extract_question, format_question
import random
import threading
import time

# Set the theme
sg.theme('DarkGrey2')

category_names = {
    'English/Literature':'eng_lit',
    'General':'gen',
    'Pop Culture':'pc',
    'TV/Media':'tv',
    'History':'hist',
    'STEM':'stem',
    'World':'world',
    'Other':'temp',
}

# Define layout for the main window
types = ['English/Literature', 'General', 'Pop Culture', 'TV/Media', 'History', 'STEM', 'World', 'Other']
layout = [
    [sg.Text("Select Options:")],
    [sg.Text("Question Type"), sg.Combo(['mc,fr'],key='qtype')],
    [sg.Text("Category"), sg.Combo(types,key='category')],
    [sg.Text("Difficulty"), sg.Combo([1,2,3],key='difficulty')],
    [sg.Text("Number of Questions"), sg.Input(key='number')],
    [sg.Text("Timer (seconds)"), sg.Input(key='timer')],
    [sg.Text("Preview Questions:")],
    [sg.Multiline(default_text="", size=(70, 20), key='preview')],
    [sg.Button("Preview"),sg.Button("Start"), sg.Button("Exit")]
]
    

def start():
    # Create the main window
    window = sg.Window("Quiz App", layout)
    # load questions
    fname = 'all_trivia_qs.json'
    with open(fname,'r') as fh:
        qs = json.load(fh)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        elif event == 'Preview':
            cat = values['category']
            if cat in category_names:
                cat = category_names[cat]
            else:
                cat = None
            questions = get_questions(qs,qtype=values['qtype'],category=cat,difficulty=values['difficulty'],number=values['number'])
            preview = ""
            for q in extract_question(questions):
                preview+=f"- {q}\n"
            window['preview'].update(preview)
        
        elif event == 'Start':
            cat = values['category']
            if cat in category_names:
                cat = category_names[cat]
            else:
                cat = None
            questions = get_questions(qs,qtype=values['qtype'],category=cat,difficulty=values['difficulty'],number=values['number'])
            window.close()
            play(questions, values['timer'])
            break
        
    window.close()



def play(qs,timer):
        random.shuffle(qs)
        num_qs = len(qs)
        if timer:
            timer = int(timer)+1

        current_slide = -1
        ms = 0
        time = 0
        responsivity = 100

        slide_layout = [
            [sg.Text(f"Slide {1} of {num_qs}",key='slide_num'), sg.Text("Time:"),sg.Text(f"{timer}",key="timer")],
            [sg.Multiline("Click 'Next' to Start", size=(40, 10), key='slide_text')],
            [sg.Button("Previous"), sg.Button("Next")]
        ]
        slide_window = sg.Window("Slide", slide_layout, finalize=True)


        while True and current_slide<len(qs):
            slide_event, slide_values = slide_window.read(timeout=responsivity)
            ms+=responsivity

            if slide_event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif slide_event == 'Previous':
                time = timer
                if current_slide > 0:
                    current_slide -= 1
                    slide_window['slide_text'].update(format_question(qs[current_slide]))
                    slide_window['slide_num'].update(f"Slide {current_slide + 1} of {num_qs}")
            elif slide_event == 'Next':
                time = timer
                if current_slide < len(qs) - 1:
                    current_slide += 1
                    slide_window['slide_text'].update(format_question(qs[current_slide]))
                    slide_window['slide_num'].update(f"Slide {current_slide + 1} of {num_qs}")
            if ms>=1000 and time>0:
                time-=1
                ms=0
                slide_window['timer'].update(str(time))

        slide_window.close()


if __name__=='__main__':
    start()