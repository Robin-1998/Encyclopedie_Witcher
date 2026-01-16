"""
Classe modèle character qui hérite de basemodel
Non affilié à un utilisateur
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class Character(BaseModel):
    """
    Classe Character en lecture seule

    Cette classe contient les attributs principaux :
        - name, birth_date, death_date, birth_place, death_place,
        - gender, profession, description, citation, relation avec race
        - relation avec culture
    """

    __tablename__ = "characters"

    name = db.Column(db.String(150), nullable=False, unique=True)
    birth_date = db.Column(db.SmallInteger)
    death_date = db.Column(db.SmallInteger)
    gender = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    citation = db.Column(db.String(400))

    # ------------------------
    # Clés étrangères
    # ------------------------

    # ON DELETE SET NULL
    # exemple pour birth_place, Si le lieu est supprimé, on garde le personnage
    # mais on perd l'information du lieu
    birth_place_id = db.Column(db.BigInteger, db.ForeignKey('places.id', ondelete='SET NULL'))
    death_place_id = db.Column(db.BigInteger, db.ForeignKey('places.id', ondelete='SET NULL'))
    culture_id = db.Column(db.BigInteger, db.ForeignKey('cultures.id', ondelete='SET NULL'))
    # ON DELETE RESTRICT :
    # exemple -> Interdit la suppression d'une profession si elle est utilisée
    profession_id = db.Column(db.BigInteger, db.ForeignKey('professions.id', ondelete='RESTRICT'))
    race_id = db.Column(db.BigInteger, db.ForeignKey('races.id', ondelete='RESTRICT'), nullable=False)


    # ------------------------
    # Relations ORM
    # ------------------------

    # passive_deletes=True :
    # On indique à SQLAlchemy de NE PAS gérer la suppression lui-même.
    # C'est la base de données qui applique le ON DELETE SET NULL.
    # Cela évite : - des requêtes inutiles - des incohérences ORM / DB
    birth_place = db.relationship('Place', foreign_keys=[birth_place_id], back_populates='born_characters', passive_deletes=True)
    death_place = db.relationship('Place', foreign_keys=[death_place_id], back_populates='dead_characters', passive_deletes=True)
    profession = db.relationship('Profession', back_populates='characters')
    race = db.relationship('Race', back_populates='characters')
    culture = db.relationship('Culture', back_populates='characters')

    # ------------------------
    # Sérialisation
    # ------------------------

    def to_dict(self):
        """
        Convertit l'objet Character en dictionnaire sérialisable

        Cette méthode va réutiliser BaseModel afin d'inclure les champs id,
        created_at, updated_at
        """
        data = super().to_dict() # récupère le dictionnaire du parent
        data.update ({
            "name": self.name,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "birth_place": self.birth_place.title if self.birth_place else None,
            "death_place": self.death_place.title if self.death_place else None,
            "profession": self.profession.name if self.profession else None,
            "gender": self.gender,
            "description": self.description,
            "citation": self.citation,
        })
        return data
