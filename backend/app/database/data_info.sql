-- -----------------------------
-- Inserts Profession
-- -----------------------------
INSERT INTO professions (id, name, description)
VALUES
(1, 'Sorceleurs', 'Les sorecleurs ont été créé par les magiciens pour éradiquer les monstres'),
(2, 'Magicien', 'Les magiciens tirent leur pouvoir de différents éléments'),
(3, 'Scoia''tell', 'Groupe armée constituer uniquement de non humain dans le but de se venger des humains qui ont pillé leurs terres et massacrer les leurs')

-- -----------------------------
-- Inserts Culture
-- -----------------------------

INSERT INTO cultures (id, name, description)
VALUES
(1, 'Culte de Melitele', 'Culte qui provient du royaume du Nord on l''on prit pour la déesse Melitele');

-- -----------------------------
-- Inserts Organisation
-- -----------------------------
INSERT INTO organisation (id, name, description, organisation_type_id)
VALUES
(1, 'École du loup', 'La confrérie de sorceleurs de Kaer Morhen, dont Geralt fait partie', 5),
(2, 'École du chat', 'Sorceleurs connues pour leurs méthodes amorales et leur mobilité', 5),
(3, 'Loge des Magiciennes', 'Organisation secrète visant à influencer le pouvoir politique', 3),
(4, 'Ordre de la rose ardente', 'Ordre chevaleresque du royaume de Temeria', 2);

INSERT INTO organisation_types (id, name)
VALUES 
(1, 'Guilde'),
(2, 'Ordre Militaire'),
(3, 'Confrérie'),
(4, 'Organisation criminelle'),
(5, 'Ecole de sorceleurs'),
(6, 'Culte / Ordre religieux');
