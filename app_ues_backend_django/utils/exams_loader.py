import re
import json


def load_exam(json_exam, txt_exam):
    # read txt file
    right_answers = []
    with open(txt_exam) as f:
        lines = f.readlines()
        for l in lines:
            if 'ANSWER' in l.upper():
                correct = l.split(' ')[1].strip()
                right_answers.append(correct)

    # read json
    with open(json_exam) as json_file:
        questions = []
        data = json.load(json_file)
        multiple_choice_questions = list(filter(lambda x: x.get("@type") == 'multichoice', data))
        for q, right_answer in zip(multiple_choice_questions, right_answers):
            question = {}
            raw_qt = q.get('questiontext').get('text')
            result = ''.join(list(
                filter(lambda y: len(y) > 3 and 'img' not in y and 'span' not in y and 'strong' not in y,
                       re.split(r'[<>]', raw_qt))))
            question_text = re.sub(' +', ' ', result)

            if 'file' in q.get('questiontext'):
                if isinstance(q.get('questiontext').get('file'), list):
                    img_dict = q.get('questiontext').get('file')[-1]

                else:
                    img_dict = q.get('questiontext').get('file')

                img = img_dict.get('#text')
                question['imagen'] = img
            if question_text:
                question['texto'] = question_text
            answers = []
            for a, l in zip(q.get('answer'), ['A', 'B', 'C', 'D', 'E']):
                answer = {}
                text = ''.join(list(
                    filter(
                        lambda y: 'img' not in y and 'span' not in y and 'strong' not in y and y != 'p' and y != '/p',
                        re.split(r'[<>]', a['text']))))
                if text:
                    answer['texto'] = text

                if 'file' in a:
                    file = a.get('file')
                    if isinstance(file, list):
                        file = file[-1]

                    img = file.get('#text')
                    answer['imagen'] = img

                answer['literal'] = l
                if answer['literal'] == right_answer:
                    answer['es_respuesta_correcta'] = True
                else:
                    answer['es_respuesta_correcta'] = False
                # answer.pop('literal')
                answers.append(answer)

            question['answers'] = answers
            questions.append(question)

    return questions