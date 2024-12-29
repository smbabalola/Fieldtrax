
from datetime import date
from fastapi import FastAPI, HTTPException
from schemas import Pump_Types, Genre_Types, Pump, BandBase, BandCreate, BandwithID 

app = FastAPI()

    
Pumps = [
   {'id':1, 'rig_id': 101,'rig_name':'SP-295', 'liner_id': 6.5, 'pump_type':'triplex', 'stroke_length':12, 'rod_diameter':0, 'efficiency': 0.97, 'riser': False, 'kill': False},
   {'id':4, 'rig_id': 101,'rig_name':'SP-295', 'liner_id': 6.5, 'pump_type':'triplex', 'stroke_length':12, 'rod_diameter':0, 'efficiency': 0.97, 'riser': False, 'kill': False},
   {'id':5, 'rig_id': 101,'rig_name':'SP-295', 'liner_id': 6.5, 'pump_type':'triplex', 'stroke_length':12, 'rod_diameter':0, 'efficiency': 0.97, 'riser': False, 'kill': False},
   {'id':2, 'rig_id': 105,'rig_name':'NBR-197', 'liner_id': 6.5,'pump_type':'duplex', 'stroke_length':11, 'rod_diameter':0, 'efficiency': 0.98, 'riser': False, 'kill': False},
   {'id':3, 'rig_id': 106,'rig_name':'SINO-21', 'liner_id': 6, 'pump_type':'duplex', 'stroke_length':12, 'rod_diameter':0, 'efficiency': 0.97, 'riser': False, 'kill': False},
]

Bands = [
    {'id': 1, 'name': "The Beatles", 'genre': "Rock", 'albums': [
        {'title': "Abbey Road", 'release_date': '1969-11-08'},
        # {'title': "Sgt. Pepper's Lonely Hearts Club Band", 'release_date': '1967-06-01'}
    ]},
    {'id': 2, 'name': "Queen", 'genre': "Rock", 'albums': [
        {'title': "Bohemian Rhapsody", 'release_date': '1975-11-10'},
        {'title': "A Night at the Opera", 'release_date': '1975-11-21'}
    ]},
    {'id': 3, 'name': "Led Zeppelin", 'genre': "Rock", 'albums': [
        {'title': "Led Zeppelin IV", 'release_date': '1971-11-08'},
        {'title': "Physical Graffiti", 'release_date': '1975-02-25'}
    ]},
    {'id': 4, 'name': "Nirvana", 'genre': "Grunge", 'albums': [
        {'title': "Bleach", 'release_date': '1989-09-15'},
        {'title': "Nevermind", 'release_date': '1991-09-24'}
    ]},
    {'id': 5, 'name': "Pink Floyd", 'genre': "Progressive Rock", 'albums': [
        {'title': "Dark Side of the Moon", 'release_date': '1973-03-07'},
        {'title': "Wish You Were Here", 'release_date': '1975-08-15'}
    ]},
    {'id': 6, 'name': "Metallica", 'genre': "Thrash Metal", 'albums': [
        {'title': "Master of Puppets", 'release_date': '1986-03-03'},
        {'title': "...And Justice for All", 'release_date': '1988-08-25'}
    ]},
    {'id': 7, 'name': "AC/DC", 'genre': "Hard Rock", 'albums': [
        {'title': "Back in Black", 'release_date': '1980-07-25'},
        {'title': "Highway to Hell", 'release_date': '1979-07-30'}
    ]},
    {'id': 8, 'name': "U2", 'genre': "Rock", 'albums': [
        {'title': "The Joshua Tree", 'release_date': '1987-03-10'},
        {'title': "Achtung Baby", 'release_date': '1991-11-18'}
    ]},
    {'id': 9, 'name': "The Who", 'genre': "Rock", 'albums': [
    ]},
    {'id': 10, 'name': "The Rolling Stones", 'genre': "Rock and Roll", 'albums': [
        {'title': "Sticky Fingers", 'release_date': '1971-04-23'},
        {'title': "Exile on Main St.", 'release_date': '1972-05-12'}
    ]}
]

@app.get("/")
async def index() -> dict[str,str]:
    return {"hello": "world"}

@app.get('/about')
async def about() -> str:
    return "An exceptional Company"

# @app.get("/pumps")
# async def pumps() -> list[dict]:
#     return Pumps

@app.get("/pumps")
async def pumps() -> list[Pump]:
    return [
        Pump(**p) for p in Pumps
        
    ]

@app.get('/pumps/{pump_id}')
async def pumps(pump_id: int) -> Pump:
    pump = next((b for b in Pumps if b['id'] == pump_id), None)
    if pump is None:
        raise HTTPException(status_code=404, detail="Pump not found!")
    return pump

@app.get('/pumps/rigname/{rig_name}')
async def pumps_for_rig(rig_name:str) -> list[Pump]:
   return [
       b for b in Pumps if b['rig_name'].lower() == rig_name.lower()
   ]

@app.get('/pumps/rig/{rig_id}')
async def pumps_for_rig(rig_id:int) -> list[Pump]:
   return [
       b for b in Pumps if b['rig_id'] == rig_id
   ]

@app.get('/pumps/pump_type/{pump_type}')
async def pumps_types_for_rigs(pump_type: Pump_Types) -> list[Pump]:
   return [
       b for b in Pumps if b['pump_type'].lower() == pump_type.value  
       ]
        
# Bands
@app.get("/bands")
async def bands(genre:Genre_Types| None=None, 
                has_albums: bool = True
                ) -> list[BandwithID]:
    band_list = [BandwithID(**b)for b in Bands]
    if genre: 
            band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if not has_albums:
            band_list = [
            b for b in band_list if len(b.albums) ==0
            ]
    return band_list    
        
@app.get('/bands/{band_id}')
async def bands(band_id: int) -> BandwithID:
    # band = next((b for b in Bands if b['id'] == band_id), None)
    band = next((BandwithID(**b)for b in Bands if b['id'] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found!")
    return band

# @app.get('/bands/genre/{genre}')
# async def bands_from_genre(genre: Genre_Types) -> list[Band]:
#    return [
#        b for b in Bands if b['genre'].lower() == genre.value
#        ]


@app.post('/bands')
async def create_band(band_data:BandCreate)->BandwithID:
    id = Bands[-1]['id']+1
    band = BandwithID(id=id, **band_data.model_dump()).model_dump()
    Bands.append(band)
    return band

    
        
