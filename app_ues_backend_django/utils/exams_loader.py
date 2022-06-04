import json
import re
import xmltodict
from bs4 import BeautifulSoup


def load_exam(xml_exam, txt_exam):
    # read txt file
    right_answers = []
    with open(txt_exam) as f:
        lines = f.readlines()
        for l in lines:
            if 'ANSWER' in l.upper():
                correct = l.split(' ')[1].strip()
                right_answers.append(correct)

    # read json
    with open(xml_exam, "r") as xml_file:
        questions = []
        data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()
        data = data_dict.get('quiz').get('question')
        multiple_choice_questions = list(filter(lambda x: x.get("@type") == 'multichoice', data))
        iterations = 0
        for i, (q, right_answer) in enumerate(zip(multiple_choice_questions, right_answers)):
            iterations += 1
            if iterations > 10:
                break
            question = {"numero_pregunta": i + 1}
            raw_qt = q.get('questiontext').get('text')
            # TODO: decide best approach
            try:

                question_text = None
                htmlParse = BeautifulSoup(raw_qt, 'html.parser')
                for para in htmlParse.find_all("p"):
                    question_text = para.get_text()

                if not question_text:
                    result = ''.join(list(
                        filter(lambda y: len(y) > 3 and 'img' not in y and 'span' not in y and 'strong' not in y,
                               re.split(r'[<>]', raw_qt))))
                    question_text = re.sub(' +', ' ', result)
                    question_text = question_text.replace("br /", "")
                if 'sup' in question_text:
                    continue
                if 'data:image/png;base64' in raw_qt:
                    q['questiontext']['file'] = {}
                    img = str(raw_qt.split("src=")[1].split(" alt")[0]).split("base64,")[1]
                    q['questiontext']['file']['#text'] = img


            except:
                print('Error detected, skipping')
                print(xml_exam)
                continue

            if 'file' in q.get('questiontext'):
                if isinstance(q.get('questiontext').get('file'), list):
                    img_dict = q.get('questiontext').get('file')[-1]

                else:
                    img_dict = q.get('questiontext').get('file')

                img = img_dict.get('#text')
                question['imagen'] = img
            if question_text:
                question['texto'] = question_text

            if 'imagen' not in question:
                if not question.get('texto') or question.get('texto').isspace():
                    continue
            answers = []
            for a, l in zip(q.get('answer'), ['A', 'B', 'C', 'D', 'E']):
                answer = {}
                text = None
                htmlParse = BeautifulSoup(a['text'], 'html.parser')
                for para in htmlParse.find_all("p"):
                    text = para.get_text()

                if 'data:image/png;base64' in a['text']:
                    a['file'] = {}
                    try:
                        img2 = str(a['text'].split("src=")[1].split(" alt")[0]).split("base64,")[1]
                    except IndexError:
                        print(a['text'])
                    a['file']['#text'] = img2
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
                answers.append(answer)

            question['answers'] = answers
            questions.append(question)

    return questions
