"""Real NASA facts used in the game.

Every entry says where the fact comes from and when it happened or was
published. The numbers INSIDE the game (power 0-100, etc.) are made up for
play, but the facts below are NOT. Only well-documented findings are listed,
and each one points to an official NASA / NOAA landing page so it can be
checked.
"""

DISCLAIMER = (
    "Junior Astronaut Mission Trainer is a learning game. The game scores, "
    "resource numbers and the outpost itself are made up. The 'NASA Fact' "
    "boxes are real, with the date and source shown. Please check them at the "
    "linked NASA pages. A real lunar base would be much more complicated!"
)

SOURCE_GROUPS = {
    "DONKI": "NASA DONKI: space weather database",
    "OSDR": "NASA OSDR: space biology and health data",
    "ARTEMIS": "NASA Artemis: returning to the Moon",
    "MARS": "NASA Mars, Moon and Apollo research",
}

DATA_SOURCES = [
    {
        "name": "DONKI (Space Weather Database Of Notifications, Knowledge, Information)",
        "group": "DONKI",
        "description": "NASA's public record of solar flares, coronal mass ejections, "
                       "geomagnetic storms and solar energetic particle events.",
        "url": "https://ccmc.gsfc.nasa.gov/tools/DONKI/",
    },
    {
        "name": "OSDR (Open Science Data Repository)",
        "group": "OSDR",
        "description": "A free online library of data from space biology and "
                       "biomedical experiments.",
        "url": "https://osdr.nasa.gov/",
    },
    {
        "name": "NASA Artemis",
        "group": "ARTEMIS",
        "description": "NASA's program to return people to the Moon and prepare for Mars.",
        "url": "https://www.nasa.gov/humans-in-space/artemis/",
    },
    {
        "name": "NASA Mars and Moon science",
        "group": "MARS",
        "description": "Mission results from Mars rovers, lunar orbiters and Apollo.",
        "url": "https://science.nasa.gov/mars/",
    },
]

GLOSSARY = [
    {"word": "Sol", "meaning": "One day on a mission. On Mars, a sol is 24 hours 39 minutes 35 seconds. "
                               "In this game each sol is one training day."},
    {"word": "Solar flare", "meaning": "A sudden flash of light and energy from the Sun."},
    {"word": "Radiation", "meaning": "Invisible energy and fast particles from space that can harm living things."},
    {"word": "Shielding", "meaning": "Walls, shelters or soil that block radiation."},
    {"word": "Regolith", "meaning": "The loose dusty soil that covers the Moon."},
    {"word": "Life support", "meaning": "The machines that give a crew clean air and water."},
]

_FACT_LIST = [
    # ---------------------------------------------------------------- DONKI
    {
        "id": "donki_overview", "group": "DONKI",
        "title": "What is DONKI?",
        "text": "DONKI is NASA's Space Weather Database Of Notifications, Knowledge, Information. "
                "It is run by the Community Coordinated Modeling Center at NASA Goddard and keeps "
                "records of space weather such as solar flares, coronal mass ejections (CMEs), "
                "geomagnetic storms and solar energetic particle events.",
        "date": "Ongoing public database",
        "source": "NASA Community Coordinated Modeling Center (CCMC), DONKI",
        "url": "https://ccmc.gsfc.nasa.gov/tools/DONKI/",
    },
    {
        "id": "flare_classes", "group": "DONKI",
        "title": "Flares come in sizes",
        "text": "Solar flares are ranked by strength with the letters A, B, C, M and X. Each letter "
                "is about ten times stronger than the one before it, so X-class flares are the "
                "strongest kind.",
        "date": "NASA reference information",
        "source": "NASA Science: Solar Storms and Flares",
        "url": "https://science.nasa.gov/sun/solar-storms-and-flares/",
    },
    {
        "id": "flare_speed", "group": "DONKI",
        "title": "Light first, cloud later",
        "text": "Light from a solar flare takes about 8 minutes to reach us. A coronal mass ejection "
                "(CME), a huge cloud of solar material, usually takes one to a few days to arrive. "
                "That gap is why space weather forecasters can send warnings.",
        "date": "NASA reference information",
        "source": "NASA Science: Solar Storms and Flares",
        "url": "https://science.nasa.gov/sun/solar-storms-and-flares/",
    },
    {
        "id": "may2024_storm", "group": "DONKI",
        "title": "The May 2024 super storm",
        "text": "On 10-11 May 2024 Earth had its strongest geomagnetic storm in about 20 years, rated "
                "G5 ('extreme') by NOAA's Space Weather Prediction Center. It was caused by several "
                "eruptions from the Sun. Space weather events like this are what DONKI records.",
        "date": "10-11 May 2024",
        "source": "NOAA Space Weather Prediction Center and NASA",
        "url": "https://www.swpc.noaa.gov/",
    },
    {
        "id": "sep_1972", "group": "DONKI",
        "title": "A close call between Apollo missions",
        "text": "In August 1972, between the Apollo 16 and Apollo 17 Moon missions, the Sun released a "
                "huge burst of energetic particles. No Apollo crew was in space at the time, but NASA "
                "scientists point out that astronauts on the Moon during such a storm could have "
                "received a dangerous radiation dose.",
        "date": "August 1972",
        "source": "NASA Science: Solar Storms and Flares",
        "url": "https://science.nasa.gov/sun/solar-storms-and-flares/",
    },
    # --------------------------------------------------------------- ARTEMIS
    {
        "id": "artemis_plan", "group": "ARTEMIS",
        "title": "Why Artemis?",
        "text": "NASA's Artemis program aims to return people to the Moon, explore the Moon's south "
                "polar region, and learn how to live and work there to prepare for later human "
                "missions to Mars.",
        "date": "Artemis Plan, 2020",
        "source": "NASA Artemis",
        "url": "https://www.nasa.gov/humans-in-space/artemis/",
    },
    {
        "id": "moon_no_shield", "group": "ARTEMIS",
        "title": "The Moon has no bubble",
        "text": "Earth is protected from much space radiation by its magnetic field and thick "
                "atmosphere. The Moon has no global magnetic field and almost no atmosphere, so "
                "explorers there need shielding. Engineers study shelters and covering habitats "
                "with lunar soil (regolith) as ways to add protection.",
        "date": "NASA reference information",
        "source": "NASA Science: Moon, and NASA Artemis",
        "url": "https://science.nasa.gov/moon/",
    },
    {
        "id": "artemis1_mare", "group": "ARTEMIS",
        "title": "Mannequins that measured radiation",
        "text": "Artemis I flew an uncrewed Orion capsule around the Moon from 16 November to "
                "11 December 2022. Two mannequin torsos named Helga and Zohar carried radiation "
                "sensors for the MARE experiment (from the German Space Agency DLR and the Israel "
                "Space Agency). Zohar wore a protective AstroRad vest and Helga did not, so "
                "scientists could compare the two.",
        "date": "16 November - 11 December 2022",
        "source": "NASA Artemis I and DLR",
        "url": "https://www.nasa.gov/humans-in-space/artemis/",
    },
    {
        "id": "radiation_limit", "group": "ARTEMIS",
        "title": "A radiation limit for astronauts",
        "text": "In 2022 NASA adopted a career radiation limit of 600 millisieverts (mSv) of effective "
                "dose for all astronauts, the same for everyone regardless of age or sex.",
        "date": "2022",
        "source": "NASA Office of the Chief Health and Medical Officer (NASA-STD-3001)",
        "url": "https://www.nasa.gov/humans-in-space/",
    },
    # ------------------------------------------------------------ MARS / MOON
    {
        "id": "sol_definition", "group": "MARS",
        "title": "What is a sol?",
        "text": "A sol is one Martian day: 24 hours, 39 minutes and 35 seconds. NASA Mars rover teams "
                "count their mission days in sols.",
        "date": "NASA reference information",
        "source": "NASA Mars Exploration",
        "url": "https://science.nasa.gov/mars/",
    },
    {
        "id": "mars_rad_cruise", "group": "MARS",
        "title": "Radiation on the way to Mars",
        "text": "During Curiosity's roughly eight-month trip to Mars (November 2011 - August 2012), its "
                "RAD instrument measured about 1.8 millisieverts of radiation per day. The data "
                "helps NASA plan protection for future astronauts.",
        "date": "Published in Science, May 2013",
        "source": "NASA Mars Science Laboratory (Curiosity) RAD team",
        "url": "https://science.nasa.gov/mars/",
    },
    {
        "id": "moxie", "group": "MARS",
        "title": "Making oxygen on Mars",
        "text": "On 20 April 2021 MOXIE, a toaster-sized experiment on the Perseverance rover, made "
                "oxygen from the carbon dioxide in Mars's air for the first time: about 5.4 grams, "
                "roughly 10 minutes of breathing for an astronaut. By August 2023 it had made 122 "
                "grams in total, about what a small dog breathes in 10 hours.",
        "date": "20 April 2021 and August 2023",
        "source": "NASA / JPL: Mars 2020 Perseverance MOXIE",
        "url": "https://science.nasa.gov/mission/mars-2020-perseverance/",
    },
    {
        "id": "opportunity_dust", "group": "MARS",
        "title": "Dust and solar power on Mars",
        "text": "In June 2018 a planet-wide dust storm blocked so much sunlight that the solar-powered "
                "Opportunity rover stopped communicating (10 June 2018). Earlier in the mission, "
                "wind gusts sometimes cleaned dust off rover solar panels.",
        "date": "June 2018",
        "source": "NASA / JPL: Mars Exploration Rover Opportunity",
        "url": "https://science.nasa.gov/mars/",
    },
    {
        "id": "chapea", "group": "MARS",
        "title": "Practising Mars life on Earth",
        "text": "From 25 June 2023 to 6 July 2024, four volunteers lived for 378 days inside Mars Dune "
                "Alpha, a 3D-printed habitat at NASA's Johnson Space Center. The CHAPEA mission "
                "practised living with limited resources, equipment failures, communication delays "
                "and growing food.",
        "date": "25 June 2023 - 6 July 2024",
        "source": "NASA Johnson Space Center: CHAPEA",
        "url": "https://www.nasa.gov/humans-in-space/",
    },
    {
        "id": "iss_water", "group": "MARS",
        "title": "Recycling nearly all the water",
        "text": "In June 2023 NASA announced that the International Space Station's Environmental "
                "Control and Life Support System had reached a 98% water recovery rate, recycling "
                "nearly all water from urine, sweat and moisture in the air.",
        "date": "June 2023",
        "source": "NASA International Space Station Program",
        "url": "https://www.nasa.gov/international-space-station/",
    },
    {
        "id": "lcross", "group": "MARS",
        "title": "Water found near the Moon's south pole",
        "text": "On 9 October 2009 NASA's LCROSS mission crashed a rocket stage into Cabeus crater near "
                "the Moon's south pole. Instruments studying the dust plume detected water.",
        "date": "9 October 2009 (results announced November 2009)",
        "source": "NASA Ames Research Center: LCROSS",
        "url": "https://science.nasa.gov/moon/",
    },
    {
        "id": "sofia", "group": "MARS",
        "title": "Water on the sunny Moon",
        "text": "On 26 October 2020 NASA announced that its SOFIA flying telescope had found water "
                "molecules on the sunlit surface of the Moon, in the large crater Clavius.",
        "date": "26 October 2020",
        "source": "NASA: SOFIA",
        "url": "https://science.nasa.gov/moon/",
    },
    {
        "id": "apollo17_dust", "group": "MARS",
        "title": "Sticky, sharp Moon dust",
        "text": "Apollo astronauts, including the Apollo 17 crew in December 1972, found that sharp, "
                "sticky Moon dust clung to their suits and tools, wore down gear and irritated "
                "their eyes and noses. Apollo 17 geologist Harrison Schmitt described hay-fever-like "
                "symptoms. Dust is still a design challenge for Artemis.",
        "date": "December 1972",
        "source": "NASA Apollo 17 mission records",
        "url": "https://science.nasa.gov/moon/",
    },
    {
        "id": "apollo13_co2", "group": "MARS",
        "title": "The Apollo 13 air-filter fix",
        "text": "In April 1970 the Apollo 13 crew survived an oxygen tank failure. When carbon dioxide "
                "built up in their lunar module 'lifeboat', engineers on the ground designed a way to "
                "fit a square filter into a round socket using tape, plastic bags and other items "
                "already on board.",
        "date": "13-17 April 1970",
        "source": "NASA Apollo 13 mission history",
        "url": "https://science.nasa.gov/moon/",
    },
    {
        "id": "moon_day", "group": "MARS",
        "title": "A very long Moon day",
        "text": "One full day-night cycle on the Moon lasts about 29.5 Earth days: roughly two weeks "
                "of sunlight followed by two weeks of darkness at most places.",
        "date": "NASA reference information",
        "source": "NASA Science: Moon facts",
        "url": "https://science.nasa.gov/moon/",
    },
    {
        "id": "lro_cold", "group": "MARS",
        "title": "The coldest places",
        "text": "NASA's Lunar Reconnaissance Orbiter measured some permanently shadowed craters near the "
                "Moon's poles at temperatures below minus 200 degrees Celsius, among the coldest "
                "places measured in the Solar System.",
        "date": "LRO Diviner results, published 2010",
        "source": "NASA Lunar Reconnaissance Orbiter (LRO)",
        "url": "https://science.nasa.gov/moon/",
    },
    # ------------------------------------------------------------------ OSDR
    {
        "id": "osdr_overview", "group": "OSDR",
        "title": "A library of space biology",
        "text": "NASA's Open Science Data Repository (OSDR) is a free online library of data from "
                "space biology and biomedical experiments, such as studies of plants, microbes and "
                "animals flown in space, so scientists and students anywhere can explore them.",
        "date": "Ongoing public data repository",
        "source": "NASA Open Science Data Repository (OSDR)",
        "url": "https://osdr.nasa.gov/",
    },
    {
        "id": "twins_study", "group": "OSDR",
        "title": "The Twins Study",
        "text": "NASA's Twins Study compared astronaut Scott Kelly, who spent 340 days on the "
                "International Space Station (March 2015 - March 2016), with his identical twin Mark "
                "Kelly on Earth. Results published in Science showed many changes in the body during "
                "flight, and most returned toward normal after he came home.",
        "date": "Flight 2015-2016, results published April 2019",
        "source": "NASA Human Research Program, Science journal",
        "url": "https://www.nasa.gov/humans-in-space/",
    },
    {
        "id": "bone_loss", "group": "OSDR",
        "title": "Why astronauts exercise",
        "text": "Without gravity's pull, bones can lose about 1% or more of their density each month in "
                "weight-bearing areas such as the hips. Astronauts on the ISS exercise about two hours "
                "a day to help protect their muscles and bones.",
        "date": "NASA reference information",
        "source": "NASA Human Research Program",
        "url": "https://www.nasa.gov/humans-in-space/",
    },
    {
        "id": "veggie_lettuce", "group": "OSDR",
        "title": "Lettuce grown in space",
        "text": "On 10 August 2015 ISS astronauts Scott Kelly, Kjell Lindgren and Kimiya Yui ate red "
                "romaine lettuce grown in the station's Veggie plant chamber, a step toward growing "
                "food on long missions.",
        "date": "10 August 2015",
        "source": "NASA International Space Station Program",
        "url": "https://www.nasa.gov/international-space-station/",
    },
]

FACTS = {fact["id"]: fact for fact in _FACT_LIST}


def get_fact(fact_id):
    """Return one fact dictionary (or None)."""
    return FACTS.get(fact_id)


def facts_for(fact_ids):
    """Return a list of fact dictionaries for the ids given."""
    return [FACTS[i] for i in fact_ids if i in FACTS]


def all_facts_grouped():
    """Facts organised by source group, used by /api/about."""
    grouped = {}
    for fact in _FACT_LIST:
        grouped.setdefault(fact["group"], []).append(fact)
    return grouped
