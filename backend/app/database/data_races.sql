-- -----------------------------
-- Inserts Races_types
-- -----------------------------
INSERT INTO race_types (name, parent_id)
VALUES
('Humain', NULL),
('Elfe', NULL),
('Nain', NULL),
('Monstre', NULL),
('Nécrophage', 4),
('Goule', 5)
('Putréfacteur', 5),
('Ogroïde', 4),
('Nekker', 8),
('Mutant', NULL);
-- -----------------------------
-- Inserts Races
-- -----------------------------
-- Penser à rajouter image_url
INSERT INTO races (id, name, race_type_id, description, citation)
VALUES (
	1, 'Aen Seidhe', 2, 'Les Aen Seidhe sont les elfes principaux du Continent, gracieux, anciens, proches de la magie et de la nature.',
	'Va fail'
);

INSERT INTO races (id, name, race_type_id, description, citation)
VALUES (
	2, 'Aen Elle', 2, 'Les Aen Elle sont les elfes qui ont quitté la sphera mundi pour rester sur tir Tochair, ce sont une race pur',
	'Tir Tochair est notre foyer'
)

-- -----------------------------
-- Inserts Race_traits
-- -----------------------------
INSERT INTO Race_traits (race_id, trait, category)
VALUES
(1, 'Longévité', 'Physique'),
(1, 'Affinité avec la magie', 'Magique'),
(1, 'Grande agilité', 'Physique'),
(1, 'Architecture et art raffinés', 'Culture');
