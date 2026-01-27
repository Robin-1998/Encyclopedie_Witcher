"""
Classe modèle pour les différentes cultures
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel
from sqlalchemy.orm import validates

class Culture(BaseModel):
    """
    Classe culture en lecture seule

    Une culture peut représenter :
    - une magie
    - un sort magique
    - une religion
    - etc.

    La relation parent/enfant permet par exemple :
    - Magie (parent)
      └── Sorts magiques (enfants)
    """

    __tablename__ = "cultures"


    name = db.Column(db.String(150), nullable=False)
    short_description = db.Column(db.Text)

    # Relation classique : un personnage appartient à une culture
    # lazy="select" signifie :
    # ➜ les personnages NE sont PAS chargés automatiquement
    # ➜ la requête SQL est exécutée seulement quand on accède à .characters

    characters = db.relationship('Character', back_populates='culture', lazy='select')
    culture_type_id = db.Column(db.BigInteger, db.ForeignKey("culture_types.id", ondelete="RESTRICT"), nullable=False)

    culture_type = db.relationship("CultureType", back_populates="cultures")

    # ------------------------------------------------------------------
    # Relation parent / enfant (auto-référencée)
    # ------------------------------------------------------------------

    # Référence vers une autre culture de la MÊME table.
    # Exemple :
    # - un sort magique → parent = une magie
    parent_culture_id = db.Column(
        db.BigInteger,
        db.ForeignKey("cultures.id", ondelete="RESTRICT"),
        nullable=True
    )
    # Relation vers le parent
        #
        # remote_side est OBLIGATOIRE dans une relation auto-référencée.
        # Il indique à SQLAlchemy :
        #   "Culture.id est du côté PARENT de la relation"
        #
        # Sans remote_side, SQLAlchemy ne sait pas distinguer
        # le parent de l'enfant (même table, mêmes clés).
    parent_culture = db.relationship("Culture", remote_side="Culture.id", back_populates="children")

    # Relation vers les enfants
    children = db.relationship("Culture", back_populates="parent_culture", lazy="select")
    
    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str):
            raise ValueError("Le nom doit être une chaîne.")
        if not name.strip():
            raise ValueError("Le nom est requis.")
        return name

    def to_dict(self):
        """
        Convertit l'objet Culture en dictionnaire sérialisable

        Cette méthode va réutiliser BaseModel afin d'inclure les champs id,
        created_at, updated_at
        """
        data = super().to_dict() # récupère le dictionnaire du parent
        data.update ({
            "name": self.name,
            "short_description": self.short_description,
            "culture_type_id": self.culture_type_id,
            "parent_culture_id": self.parent_culture_id
        })
        return data
