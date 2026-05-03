"""
Le parent Repository pour gérer la persistance des données avec SQLAlchemy.
Il contient : 
    - Repository : classe abstraite définissant l'interface générique 
    pour les opérations CRUD
    - SQLAlchemyRepository : implémentation concrète utilisant SQLAlchemy
    comme moteur ORM

"""

from abc import ABC, abstractmethod
from backend.app import db

#------- Classe abstraite Repository ------------
class Repository(ABC):
    """
    Opération CRUD
    """
    @abstractmethod
    def add(self, obj):
        """ajoute un objet à la base de donnée"""
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @abstractmethod
    def get(self, obj_id):
        """Récupère un objet par son ID"""
        pass

    @abstractmethod
    def get_all(self):
        """récupère tous les objets"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Met à jour un objet existant"""
    pass

    @abstractmethod
    def delete(self, obj_id):
        """supprime un objet de la db par son identifiant (id)"""
    pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """récupère un objet par un attribut spécifique"""
    pass

# ==================================
# . Implémentation SQLAlchemy
# ==================================
class SQLAlchemyRepository(Repository):
    """
    Repository basé sur SQLAlchemy
    fournit les opérations CRUD générique pour n'importe quel type de modèle
    """
    def __init__(self, model):
        self.model = model

#--------------- CREATION ----------------

    def add(self, obj):
        """
        Ajoute un objet à la base de donnée et le commit
        Code Erreur:
            Exception: Si une erreur survient lors du commit
        """
        try: 
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

#--------------- READ ----------------

    def get(self, obj_id):
        """Récupère un objet par son identifiant"""
        return db.session.get(self.model, obj_id)

    def get_all(self):
        """Récupère tous les objets"""
        return self.model.query.all()

    def get_by_attribute(self, attr_name, attr_value):
        """Récupère un objet selon la valeur d'un attribut donnée"""
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

#------------UPDATE------------------

    def update(self, obj_id, data):
        """
        Met à jour un objet existant avec les valeurs fournies.
        """
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    # Vérifie que l'attribut existe sur le modèle
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                db.session.commit()
                return obj
            return None
        except Exception as e:
            db.session.rollback()
            raise

    def delete(self, obj_id):
        """
        Supprime un objet de la base de données.
        Code Erreur:
            Exception: Si la suppression échoue
        """
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Erreur lors de la suppression de {self.model.__name__}: {e}")
