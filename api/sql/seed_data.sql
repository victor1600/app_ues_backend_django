-- Course
INSERT INTO api_course (id, name, description, created_at, icon, active) VALUES (1, 'Matemáticas', '', '2022-02-05 20:39:00.531232', 'photos/icons/2022/02/05/math.jpg', 1);
INSERT INTO api_course (id, name, description, created_at, icon, active) VALUES (2, 'Lenguaje', '', '2022-02-05 20:39:25.054127', 'photos/icons/2022/02/05/lenguaje.jpg', 1);
INSERT INTO api_course (id, name, description, created_at, icon, active) VALUES (3, 'Biologia', '', '2022-02-05 20:39:39.337348', 'photos/icons/2022/02/05/biologia.png', 1);
INSERT INTO api_course (id, name, description, created_at, icon, active) VALUES (4, 'Sociales', '', '2022-02-05 20:39:54.577533', 'photos/icons/2022/02/05/sociales.jpg', 1);
INSERT INTO api_course (id, name, description, created_at, icon, active) VALUES (5, 'Química', '', '2022-02-05 20:40:23.655649', 'photos/icons/2022/02/05/qumica.png', 1);
INSERT INTO api_course (id, name, description, created_at, icon, active) VALUES (6, 'Física', '', '2022-02-05 20:40:57.274821', 'photos/icons/2022/02/05/fisica.png', 1);

-- Topic
INSERT INTO api_topic (id, name, description, created_at, active, course_id) VALUES (1, 'Trigonometría', '', '2022-02-05 20:47:11.702380', 1, 1);
INSERT INTO api_topic (id, name, description, created_at, active, course_id) VALUES (2, 'Factorización', '', '2022-02-05 20:49:18.257187', 1, 1);
INSERT INTO api_topic (id, name, description, created_at, active, course_id) VALUES (3, 'Historia de El Salvador', '', '2022-02-05 20:49:31.797096', 1, 4);
INSERT INTO api_topic (id, name, description, created_at, active, course_id) VALUES (4, 'Análisis sintáctico', '', '2022-02-05 20:49:54.883961', 1, 2);
INSERT INTO api_topic (id, name, description, created_at, active, course_id) VALUES (5, 'Planteamiento de ecuaciones', '', '2022-02-05 21:20:20.877402', 1, 1);

-- Material
INSERT INTO api_material (id, name, description, created_at, file, topic_id,active) VALUES (1, 'Identidades Trigonométricas Fundamentales', '', '2022-02-05 20:51:25.420215', 'files/2022/02/05/trigonometria.pdf', 1, 1);


-- Question
INSERT INTO api_question (id, question_text, created_at, question_image, active, topic_id) VALUES (1, 'La tangente es igual a:', '2022-02-05 20:53:06.399142', '', 1, 1);
INSERT INTO api_question (id, question_text, created_at, question_image, active, topic_id) VALUES (2, 'Primer presidente de El Salvador:', '2022-02-05 21:35:22.722240', 'photos/question_images/2022/02/05/arce_manuel_jose.jpeg', 1, 3);

-- Answer
INSERT INTO api_answer (id, answer_text, created_at, is_right_answer, active, question_id) VALUES (1, 'sin/cos', '2022-02-05 20:55:02.453068', 1, 1, 1);
INSERT INTO api_answer (id, answer_text, created_at, is_right_answer, active, question_id) VALUES (2, 'cos/sin', '2022-02-05 20:55:09.765403', 0, 1, 1);
INSERT INTO api_answer (id, answer_text, created_at, is_right_answer, active, question_id) VALUES (3, 'sin', '2022-02-05 20:55:25.729697', 0, 1, 1);
INSERT INTO api_answer (id, answer_text, created_at, is_right_answer, active, question_id) VALUES (4, 'Manuel José Arce', '2022-02-05 21:36:02.025145', 1, 1, 2);
INSERT INTO api_answer (id, answer_text, created_at, is_right_answer, active, question_id) VALUES (5, 'Alfredo Cristiani', '2022-02-05 21:36:20.241509', 0, 1, 2);
INSERT INTO api_answer (id, answer_text, created_at, is_right_answer, active, question_id) VALUES (6, 'Gerardo Barrios', '2022-02-05 21:36:43.208453', 0, 1, 2);

-- User
INSERT INTO USERS(id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (1, '!H1HpGky6GD5rhKcjWW3SqwKPhAdsBrPsMHr2d2cx', null, true, '', '', true, true, '2021-10-06 18:41:11.160023', 'diana@gmail.com');


