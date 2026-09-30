"""Jeu de données initial : thèmes, lieux, badges."""

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.location import Location
from app.seed_badges import seed_badges_if_empty

CATEGORIES = (
    ("Monuments", "monuments"),
    ("Capitales", "capitales"),
    ("Sites naturels", "sites-naturels"),
)

LOCATIONS = (
    (
        "Tour Eiffel",
        48.8584,
        2.2945,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Tour%20Eiffel%20Wikimedia%20Commons%20(cropped).jpg",
        "monuments",
    ),
    (
        "Big Ben",
        51.5007,
        -0.1246,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Big%20Ben%201.jpg",
        "monuments",
    ),
    (
        "Colisée",
        41.8902,
        12.4922,
        "https://commons.wikimedia.org/wiki/Special:FilePath/The%20Colosseum.jpg",
        "monuments",
    ),
    (
        "Statue de la Liberté",
        40.6892,
        -74.0445,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Statue%20of%20Liberty.jpg",
        "monuments",
    ),
    (
        "Opéra de Sydney",
        -33.8568,
        151.2153,
        "https://commons.wikimedia.org/wiki/Special:FilePath/SydneyOperaHouse.jpg",
        "monuments",
    ),
    (
        "Taj Mahal",
        27.1751,
        78.0421,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Taj%20Mahal%20in%20March%202004.jpg",
        "monuments",
    ),
    (
        "Christ Rédempteur",
        -22.9519,
        -43.2105,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Cristo%20Redentor%20-%20Rio%20de%20Janeiro%2C%20Brasil.jpg",
        "monuments",
    ),
    (
        "Tokyo Tower",
        35.6586,
        139.7454,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Tokyo%20Tower%20and%20around%20Skyscrapers.jpg",
        "capitales",
    ),
    (
        "Cathédrale de Brasília",
        -15.7982,
        -47.8755,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Catedral_Metropolitana_de_Bras%C3%ADlia.jpg",
        "capitales",
    ),
    (
        "Parliament House",
        -35.3082,
        149.1244,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Parliament%20House%2C%20Canberra.jpg",
        "capitales",
    ),
    (
        "Capitole",
        38.8899,
        -77.0091,
        "https://commons.wikimedia.org/wiki/Special:FilePath/US%20Capitol%20west%20side.JPG",
        "capitales",
    ),
    (
        "Fernsehturm de Berlin",
        52.5208,
        13.4094,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Berliner%20Fernsehturm.jpg",
        "capitales",
    ),
    (
        "Grand Canyon",
        36.0544,
        -112.1401,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Grand%20Canyon%20view%20from%20Pima%20Point%202010.jpg",
        "sites-naturels",
    ),
    (
        "Uluru",
        -25.3444,
        131.0369,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Uluru%20Panorama.jpg",
        "sites-naturels",
    ),
    (
        "Chutes du Niagara",
        43.0799,
        -79.0747,
        "https://commons.wikimedia.org/wiki/Special:FilePath/3Falls%20Niagara.jpg",
        "sites-naturels",
    ),
    (
        "Mont Fuji",
        35.3606,
        138.7274,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Mount%20Fuji%2C%20Japan.jpg",
        "sites-naturels",
    ),
    (
        "Chutes d'Iguazú",
        -25.6953,
        -54.4367,
        "https://commons.wikimedia.org/wiki/Special:FilePath/Iguazu%20Falls.jpg",
        "sites-naturels",
    ),
)


def seed_catalog_if_empty(db: Session) -> None:
    if db.query(Category).first() is not None:
        return

    by_slug: dict[str, Category] = {}
    for name, slug in CATEGORIES:
        category = Category(name=name, slug=slug)
        db.add(category)
        by_slug[slug] = category
    db.flush()

    for name, latitude, longitude, image_url, slug in LOCATIONS:
        db.add(
            Location(
                name=name,
                latitude=latitude,
                longitude=longitude,
                image_url=image_url,
                category=by_slug[slug],
            )
        )
    db.commit()


def seed_all(db: Session) -> None:
    seed_catalog_if_empty(db)
    seed_badges_if_empty(db)
