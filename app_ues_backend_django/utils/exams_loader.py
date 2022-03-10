import re
import xmltodict


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
        # for i, (name, age) in enumerate(zip(names, ages)):
        for i, (q, right_answer) in enumerate(zip(multiple_choice_questions, right_answers)):
            question = {"numero_pregunta": i+1}
            raw_qt = q.get('questiontext').get('text')
            try:
                result = ''.join(list(
                    filter(lambda y: len(y) > 3 and 'img' not in y and 'span' not in y and 'strong' not in y,
                           re.split(r'[<>]', raw_qt))))
                question_text = re.sub(' +', ' ', result)
                question_text = question_text.replace("br /", "")
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
            answers = []
            for a, l in zip(q.get('answer'), ['A', 'B', 'C', 'D', 'E']):
                answer = {}
                text = ''.join(list(
                    filter(
                        lambda y: 'img' not in y and 'span' not in y and 'strong' not in y and y != 'p' and y != '/p',
                        re.split(r'[<>]', a['text']))))
                text = text.replace("br /", "")
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