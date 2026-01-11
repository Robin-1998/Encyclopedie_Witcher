-- -----------------------------
-- Inserts Characters
-- -----------------------------
INSERT INTO Characters (id, name, birth_date, death_date, birth_place_id, death_place_id, gender, profession_id, description, citation, race_id, culture_id)
VALUES (
	1, 'Geralt de Riv', 1211, NULL, NULL, NULL, 'Masculin', 1, 'geralt de Riv, surnommé le boucher de Blaviken', 'Je ne tue que les monstres', 10, NULL
);

INSERT INTO character_organisations (id, character_id, organisation_id, role)
VALUES 
(1, 1, 1, 'Sorceleur');
