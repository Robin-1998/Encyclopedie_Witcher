"""
Exemples de to_dict() à ajouter sur tes modèles MapMarker et MapRegion.
Utilise geoalchemy2.shape.to_shape() pour convertir la géométrie PostGIS
en objet Shapely, puis on extrait les coordonnées x/y lisibles par Leaflet.

Dépendance à installer si pas déjà fait :
    pip install geoalchemy2 shapely
"""

# ===========================================================================
# Dans backend/app/models/map_marker.py
# Ajoute cet import en haut du fichier :
# from geoalchemy2.shape import to_shape
# ===========================================================================

def map_marker_to_dict(self):
    """
    Sérialise un MapMarker en dict compatible Leaflet.
    La géométrie POINT PostGIS est convertie en {x, y}.

    Exemple de retour :
    {
        "id": 1,
        "name": "Vizima",
        "type": "ville",
        "place_id": 12,
        "x": 452.0,
        "y": 318.0,
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    }
    """
    data = super().to_dict()  # id, image_url, created_at, updated_at

    # Coordonnées géographiques
    x, y = None, None
    if self.location is not None:
        try:
            point = to_shape(self.location)  # → objet Shapely Point
            x = point.x
            y = point.y
        except Exception:
            pass  # location malformée, on renvoie None plutôt que crasher

    data.update({
        'name': self.name,
        'type': self.type,
        'place_id': self.place_id,
        'x': x,
        'y': y,
    })
    return data


# ===========================================================================
# Dans backend/app/models/map_region.py
# Ajoute cet import en haut du fichier :
# from geoalchemy2.shape import to_shape
# ===========================================================================

def map_region_to_dict(self):
    """
    Sérialise un MapRegion en dict compatible Leaflet.
    La géométrie POLYGON PostGIS est convertie en liste de coordonnées
    [[x1,y1],[x2,y2],...] directement utilisable avec L.polygon() dans Leaflet.

    Exemple de retour :
    {
        "id": 3,
        "name": "Royaume de Temeria",
        "place_id": 5,
        "coordinates": [[100.0, 200.0], [150.0, 250.0], [100.0, 200.0]],
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    }
    """
    data = super().to_dict()  # id, image_url, created_at, updated_at

    coordinates = []
    if self.shape_data is not None:
        try:
            polygon = to_shape(self.shape_data)  # → objet Shapely Polygon
            # polygon.exterior.coords = liste de tuples (x, y)
            coordinates = [[x, y] for x, y in polygon.exterior.coords]
        except Exception:
            pass

    data.update({
        'name': self.name,
        'place_id': self.place_id,
        'coordinates': coordinates,
    })
    return data


# ===========================================================================
# Utilisation côté Leaflet (front) — pour référence
# ===========================================================================
#
# // Marqueur
# fetch('/api/map/markers')
#   .then(r => r.json())
#   .then(markers => {
#     markers.forEach(m => {
#       L.marker([m.y, m.x])           // Leaflet attend [lat, lng] = [y, x]
#         .bindPopup(m.name)
#         .addTo(map)
#     })
#   })
#
# // Région polygonale
# fetch('/api/map/regions')
#   .then(r => r.json())
#   .then(regions => {
#     regions.forEach(r => {
#       const latlngs = r.coordinates.map(c => [c[1], c[0]])  // [y, x]
#       L.polygon(latlngs)
#         .bindPopup(r.name)
#         .addTo(map)
#     })
#   })
