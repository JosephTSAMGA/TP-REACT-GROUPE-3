# =============================================================
# Géolocalisation inversée via Nominatim (OpenStreetMap) : transforme des
# coordonnées GPS en un nom de lieu lisible. Portage côté backend de
# frontend/src/shared/geocoding.ts (même API, même logique d'extraction
# de l'adresse), utilisé ici par services/badges.py pour le badge
# "Explorateur international".
# =============================================================
import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"


def reverse_geocode(latitude: float, longitude: float) -> str:
    """Appelle Nominatim et renvoie un nom lisible, ex: "Paris, France".

    Lève httpx.HTTPStatusError si l'API répond une erreur HTTP, et
    ValueError si la réponse ne contient aucune adresse exploitable.
    """
    response = httpx.get(
        NOMINATIM_URL,
        params={
            "format": "jsonv2",
            "lat": latitude,
            "lon": longitude,
            "zoom": 10,
            "addressdetails": 1,
        },
        # Nominatim exige un User-Agent identifiable, sous peine de
        # blocage — un simple "Accept" ne suffit pas côté serveur.
        headers={"Accept": "application/json", "User-Agent": "GetClose-TP/1.0"},
        timeout=5.0,
    )
    response.raise_for_status()

    address = response.json().get("address")
    if not address:
        raise ValueError("Aucune adresse trouvée pour ce point")

    place = address.get("city") or address.get("town") or address.get("village")
    country = address.get("country")

    if place and country:
        return f"{place}, {country}"
    return country or "Lieu inconnu"
