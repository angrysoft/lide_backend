from random import randint
from lide_api.models import EmploymentType, Offers, Positions, Locations
import requests

positions = (
    "Asystentka Prezesa Zarządu",
    "Agent Kredytowy",
    "Analityk Kredytowy",
    "Analityk Systemowy",
    "Brukarz",
    "Brygadzista",
    "Biochemik",
    "Hostessa",
    "HR Manager",
    "Hydraulik"
)

for position in positions:
    pos = Positions(name=position)
    pos.save()

locations = ["Zdalna", "Warszawa", "Kraków", "Wrocław"]

for location in locations:
    loc = Locations(name=location)
    loc.save()

emplT = [
    "umowa o prace",
    "umowa o dzieło",
    "umowa zlecenie",
    "umowa agencyjna",
    "kontrakt",
    "kontrakt menadżerski",
    "B2B",
    "Staż / Praktyka",
    "Wolontariat",
]

for empl in emplT:
    e = EmploymentType(name=empl)
    e.save()

for i in range(35):
    r = requests.get(
        "https://baconipsum.com/api/?type=meat-and-filler&paras=1&format=text"
    )
    offer = Offers()
    offer.position = Positions.objects.get(name__exact=positions[randint(0, len(positions)-1)])
    offer.details = r.text
    offer.posted = True
    offer.save()
    offer.location.add(
        Locations.objects.get(
            name__exact=locations[randint(0, len(locations)-1)]
        )
    )
    offer.employment_type.add(
        EmploymentType.objects.get(
            name__exact=emplT[randint(0, len(emplT)-1)]
        )
    )
    print(f"Added Offer {i}")
