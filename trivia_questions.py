# all questions will be saved with mc options, but if you want to do fr, just load the answer
# categories: eng_lit: english and literature, pc: pop culture, hist: history, 
# gen: general, stem: science/math, tv: movies/tv, world

import json
import random
from color_print import color_print

category_names = {
    'eng_lit':'english/literature',
    'gen':'general',
    'pc':'pop culture',
    'tv':'tv/media',
    'hist':'history',
    'stem':'science',
    'world':'world',
    'temp':'other',
}

def stats(fname = 'all_trivia_qs.txt'):
    with open(fname,'r') as fh:
        qs = json.load(fh)
    cats={}
    diff={}
    for q in qs:
        if q['category'] in cats:
            cats[q['category']]+=1
        else:
            cats[q['category']]=1
        if ('level ' + str(q['difficulty'])) in diff:
            diff['level '+str(q['difficulty'])]+=1
        else:
            diff['level '+str(q['difficulty'])]=1
    print(cats)
    print(diff)

def option_order():
    order = [0,1,2,3]
    random.shuffle(order)
    return order

def quiz(fname):
    if not fname:
        fname = 'all_trivia_qs.txt'
    with open(fname,'r') as fh:
        qs = json.load(fh)

    score=0
    for q in qs:
        print()
        options = option_order()
        if 'type' not in q.keys() or q['type']=='mc':
            if 'difficulty' in q.keys():
                print(f'difficulty: {q["difficulty"]}')
            print(q['question'])
            for i in range(len(options)):
                print(f'{i+1}.',end=' ')
                if options[i]==0:
                    print(q['a'])
                elif options[i]==1:
                    print(q['d1'])
                elif options[i]==2:
                    print(q['d2'])
                elif options[i]==3:
                    print(q['d3'])
            
            print()
            choice = int(input('Enter choice: '))
            if options[choice-1]==0:
                print('Correct!')
                score+=1
            else:
                print('Wrong!')
                print(q['a'])
    print()
    print(f'score is {score}/{len(qs)}')

def get_questions(qs, qtype=None, category=None, difficulty=None, number=None):
    # check arg validity
    if number:
        number = int(number)
    categories = {'eng_lit', 'gen', 'pc', 'tv', 'hist', 'stem', 'world', 'temp'}
    types = {'mc','fr'}
    difficulties = {1,2,3}
    if category and category not in categories:
        color_print('Category Not Found!','red')
        print(f'Valid categories:\n{categories}')
    if qtype and qtype not in types:
        qtype = None
    if difficulty and difficulty not in difficulties:
        difficulty = None

    # loop through and get matching questions
    questions = []
    for q in qs:
        if qtype and 'type' in q.keys():
            if not q['type']==qtype:
                continue
        if difficulty:
            if not q['difficulty']==difficulty:
                continue
        if category:
            if not q['category']==category:
                continue
        questions.append(q)
        if number and len(questions)>=number:
            break
    return questions

def extract_question(qs):
    questions = []
    for q in qs:
        questions.append(f"{q['question']}")
    return questions

def format_question(q):
    question = q['question']
    options = [q['a'],q['d1'],q['d2'],q['d3']]
    random.shuffle(options)
    for i in range(len(options)):
        question +=f'\n  {i+1}) {options[i]}'
    return question

if __name__ == '__main__':
    fname = 'all_trivia_qs.txt'
    # stats()
    print(get_questions(difficulty=2, category='gen'))