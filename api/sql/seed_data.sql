-- COURSES
INSERT INTO backend.COURSES (id, name, description, created_at, icon, active) VALUES (1, 'Matemática', '', '2021-09-27 04:16:30.177869', 'photos/icons/2021/09/27/math.jpg', 1);
INSERT INTO backend.COURSES (id, name, description, created_at, icon, active) VALUES (2, 'Lenguaje', '', '2021-09-27 04:17:13.255535', 'photos/icons/2021/09/27/lenguaje.jpg', 1);
INSERT INTO backend.COURSES (id, name, description, created_at, icon, active) VALUES (3, 'Sociales', '', '2021-09-27 04:17:24.192437', 'photos/icons/2021/09/27/sociales.jpg', 1);
INSERT INTO backend.COURSES (id, name, description, created_at, icon, active) VALUES (4, 'Química', '', '2021-09-27 04:17:52.932744', 'photos/icons/2021/09/27/qumica.png', 1);
INSERT INTO backend.COURSES (id, name, description, created_at, icon, active) VALUES (5, 'Física', '', '2021-09-27 04:18:14.291556', 'photos/icons/2021/09/27/fisica.png', 1);
INSERT INTO backend.COURSES (id, name, description, created_at, icon, active) VALUES (6, 'Biología', '', '2021-09-27 04:18:45.611153', 'photos/icons/2021/09/27/biologia.png', 1);

-- TOPICS
INSERT INTO backend.TOPICS (id, name, description, created_at, active, course_id) VALUES (1, 'Factorizacion', '', '2021-09-27 04:20:05.024624', 1, 1);
INSERT INTO backend.TOPICS (id, name, description, created_at, active, course_id) VALUES (2, 'Trigonometria', '', '2021-09-27 04:20:29.296791', 1, 1);

-- SUPPLEMENTARY_MATERIALS
INSERT INTO backend.SUPPLEMENTARY_MATERIALS (id, name, description, created_at, file, topic_id) VALUES (1, 'Guia trigonometria', '', '2021-09-27 04:23:05.609643', 'files/2021/09/27/trigonometria.pdf', 2);

-- user
INSERT INTO backend.USERS (id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, email) VALUES (1, '!H1HpGky6GD5rhKcjWW3SqwKPhAdsBrPsMHr2d2cx', null, 1, '', '', 1, 1, '2021-10-06 18:41:11.160023', 'diana@gmail.com');

