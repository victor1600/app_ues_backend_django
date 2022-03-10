-- Course
INSERT INTO api_curso (id, texto, descripcion, created_at, icono, activo) VALUES (1, 'Matematicas', '', '2022-02-05 20:39:00.531232', 'photos/icons/2022/02/05/math.jpg', 1);
INSERT INTO api_curso (id, texto, descripcion, created_at, icono, activo) VALUES (2, 'Lenguaje', '', '2022-02-05 20:39:25.054127', 'photos/icons/2022/02/05/lenguaje.jpg', 1);
INSERT INTO api_curso (id, texto, descripcion, created_at, icono, activo) VALUES (3, 'Biologia', '', '2022-02-05 20:39:39.337348', 'photos/icons/2022/02/05/biologia.png', 1);
INSERT INTO api_curso (id, texto, descripcion, created_at, icono, activo) VALUES (4, 'Sociales', '', '2022-02-05 20:39:54.577533', 'photos/icons/2022/02/05/sociales.jpg', 1);
INSERT INTO api_curso (id, texto, descripcion, created_at, icono, activo) VALUES (5, 'Química', '', '2022-02-05 20:40:23.655649', 'photos/icons/2022/02/05/qumica.png', 1);
INSERT INTO api_curso (id, texto, descripcion, created_at, icono, activo) VALUES (6, 'Fisica', '', '2022-02-05 20:40:57.274821', 'photos/icons/2022/02/05/fisica.png', 1);

-- -- Topic
INSERT INTO api_tema (id, texto, descripcion, created_at, activo, curso_id) VALUES (1, 'Trigonometria', '', '2022-02-05 20:47:11.702380', 1, 1);
INSERT INTO api_tema  (id, texto, descripcion, created_at, activo, curso_id) VALUES (2, 'Factorización', '', '2022-02-05 20:49:18.257187', 1, 1);
INSERT INTO api_tema  (id, texto, descripcion, created_at, activo, curso_id) VALUES (3, 'Historia de El Salvador', '', '2022-02-05 20:49:31.797096', 1, 4);
INSERT INTO api_tema  (id, texto, descripcion, created_at, activo, curso_id) VALUES (4, 'Analisis sintáctico', '', '2022-02-05 20:49:54.883961', 1, 2);
INSERT INTO api_tema  (id, texto, descripcion, created_at, activo, curso_id) VALUES (5, 'Planteamiento de ecuaciones', '', '2022-02-05 21:20:20.877402', 1, 1);

-- -- -- Material
-- INSERT INTO api_material (id, texto, descripcion, created_at, archivo, tema_id,activo) VALUES (1, 'Identidades Trigonométricas Fundamentales', '', '2022-02-05 20:51:25.420215', 'files/2022/02/05/trigonometria.pdf', 1, 1);

--
-- -- -- Question
-- INSERT INTO api_pregunta (id, texto, created_at, imagen, activo, tema_id) VALUES (1, 'La tangente es igual a:', '2022-02-05 20:53:06.399142', '', 1, 1);
-- INSERT INTO api_pregunta (id, texto, created_at, imagen, activo, tema_id) VALUES (2, 'Primer presidente de El Salvador:', '2022-02-05 21:35:22.722240', 'photos/question_images/2022/02/05/arce_manuel_jose.jpeg', 1, 3);
--
-- -- -- Answer
-- INSERT INTO api_respuesta (id, texto, created_at, es_respuesta_correcta, activo, pregunta_id) VALUES (1, 'sin/cos', '2022-02-05 20:55:02.453068', 1, 1, 1);
-- INSERT INTO api_respuesta (id, texto, created_at, es_respuesta_correcta, activo, pregunta_id) VALUES (2, 'cos/sin', '2022-02-05 20:55:09.765403', 0, 1, 1);
-- INSERT INTO api_respuesta (id, texto, created_at, es_respuesta_correcta, activo, pregunta_id) VALUES (3, 'sin', '2022-02-05 20:55:25.729697', 0, 1, 1);
-- INSERT INTO api_respuesta (id, texto, created_at, es_respuesta_correcta, activo, pregunta_id) VALUES (4, 'Manuel José Arce', '2022-02-05 21:36:02.025145', 1, 1, 2);
-- INSERT INTO api_respuesta (id, texto, created_at, es_respuesta_correcta, activo, pregunta_id) VALUES (5, 'Alfredo Cristiani', '2022-02-05 21:36:20.241509', 0, 1, 2);
-- INSERT INTO api_respuesta (id, texto, created_at, es_respuesta_correcta, activo, pregunta_id) VALUES (6, 'Gerardo Barrios', '2022-02-05 21:36:43.208453', 0, 1, 2);


-- User
INSERT INTO user_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (1, 'pbkdf2_sha256$260000$QO6W0kSBNV54iF4lmOjPqr$17ElHqt1eg/MG4+rpJ7kipZlcBhl18aPwZLWdCWCExs=', '2022-03-10 21:20:35.669307', 1, 'admin', '', '', 1, 1, '2022-02-12 18:08:33.112459', 'admin@gmail.com');
INSERT INTO user_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (2, 'pbkdf2_sha256$260000$ypJAj3jLA4G4phqV0O71Ib$c1fR2IlHQZQmbbTrm4JIfvevICUvZqoVusAtsD/K7V0=', null, 0, 'estudiante', 'victor', 'gonzalez', 0, 1, '2022-03-04 03:50:12.215049', 'victor@gmail.com');
INSERT INTO user_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (3, 'pbkdf2_sha256$260000$hNb2pn09Pue4rBSzCj3Ytc$P0rV3JjbhxXYrtxAqv1C744/KTRTj31GlorrCyPfeNU=', null, 0, 'estudiante2', 'Nicole', 'Guerra', 0, 1, '2022-03-04 20:44:25.021444', 'nicole@gmail.com');
INSERT INTO user_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (4, 'pbkdf2_sha256$260000$xaAEK2iqmAToEtmOMid1Wn$ZvvDfZKhDhAUo84qiJ6QqGAqyFhKVTmLPbC7dgvUUII=', null, 0, 'neko', 'samuel', 'paiz', 0, 1, '2022-03-04 20:44:53.918011', 'neko@gmail.com');
INSERT INTO user_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (5, 'pbkdf2_sha256$260000$IsyAoECZPmX8VH2BXx1jXR$9x1qkznSv1XzljdlBIvO6akUTT9uuZaI4t83XN3DdAU=', null, 0, 'estudiante3', 'Kelly', 'Aguilar', 0, 1, '2022-03-10 21:20:59.935352', 'kelly@gmail.com');
INSERT INTO user_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (6, 'pbkdf2_sha256$260000$atmimvCT5NlN6jtBUzjvcY$xY/yz/H5PtKiIqZ76DpIw1i/5KFthiSpEc04Ku1H7lw=', null, 1, 'estudiante4', 'Katya', 'Herrera', 1, 1, '2022-03-10 21:21:42.799308', 'katy@gmail.com');
-- Aspirante
INSERT INTO api_aspirante (id, fecha_de_nacimiento, imagen, user_id) VALUES (1, null, null, 2);
INSERT INTO api_aspirante (id, fecha_de_nacimiento, imagen, user_id) VALUES (2, null, null, 3);
INSERT INTO api_aspirante (id, fecha_de_nacimiento, imagen, user_id) VALUES (3, null, null, 4);
INSERT INTO api_aspirante (id, fecha_de_nacimiento, imagen, user_id) VALUES (4, null, null, 5);
INSERT INTO api_aspirante (id, fecha_de_nacimiento, imagen, user_id) VALUES (5, null, null, 6);