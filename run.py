"""
Point d’entrée de l’application Flask.
Crée et lance l’application avec le CORS d'activé pour éviter des problèmes
de compatibilité avec le front.

⚠️ Configuration pensée pour le développement :
- CORS est permissif
- DEBUG=True est activé

En production, il faudra :
- Restreindre la configuration de CORS
- Désactiver le mode debug
"""
from backend.app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
