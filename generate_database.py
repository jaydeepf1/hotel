from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HotelGroup(db.Model):
    __tablename__ = 'hotel_group'
    hotel_group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Hotel(db.Model):
    __tablename__ = 'hotel'
    hotel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    groups = db.relationship('HotelGroup', secondary='hotel_group_association', backref='hotels', lazy=True)

class HotelGroupAssociation(db.Model):
    __tablename__ = 'hotel_group_association'
    hotel_group_association_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.hotel_id'), nullable=False)
    hotel_group_id = db.Column(db.Integer, db.ForeignKey('hotel_group.hotel_group_id'), nullable=False)

class RoomPrice(db.Model):
    __tablename__ = 'room_price'
    room_price_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.hotel_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # King or Queen
    price = db.Column(db.String(50))
    
with app.app_context():
    db.create_all()

    # Sample data
    hotel_names = [
      'AC HotelLouisville Downtown(Marriott)',
      'AggielandBoutiqueHotelIHG',
      'Aloft Hotel CollegeStationMarriott',
      'Avid HotelAuburn, University area, AL(IHG)',
      'Avid HotelRinggold, GA(IHG)',
      'Avid hotel Columbus Northwest Hilliard(IHG)',
      'Baton Rouge Inn & SuitesLSU/Medical Corridor(Choice)',
      'Baymontby WyndhamLouisville East',
      'Best Western Plus Killeen/Fort HoodHotel and Suites',
      'Comfort Inn, University area, Baton Rouge,LA(Choice)',
      'Comfort InnCurry drive Killeen, TX(Choice)',
      'Comfort SuitesBaton Rouge South I-10, LA(Choice)',
      'Courtyard Bettendorfby Marriott Utica',
      'Courtyard Bryan college StattionMarriott',
      'Courtyard ColumbusWest / Hilliard (Marriott)',
      'Courtyard by Marriott Louisville East',
      'Courtyard louisville Downtown(Marriott)',
      'CourtyardBowling Green Convention Center(Marriott)',
      'Drury Inn & Suites Baton Rouge(Drury)',
      'Drury Inn & Suites Bowling Green, KY(Drury)',
      'Drury Inn & Suites Louisville East',
      'Embassy Suites by Hilton Louisville Downtown(Hilton)',
      'Fairfield Inn & Suites Columbus Hilliard(Marriott)',
      'Fairfield Inn & Suites by Marriott Davenport Quad Cities',
      'Fairfield Inn& SuitesLouisville North(Marriott)',
      'Fairfield Innand Suites Killeen(Marriott)',
      'Fairfield Innand SuitesChattanoogaSouth/East Ridge(Marriott)',
      'Hampton  inn college stationHilton',
      'Hampton Inn & Suites Davenport (Hilton)',
      'Hampton Inn Shallowford/  Hamilton placeChattanooga, TN (Hilton)',
      'Hampton Inn and SuitesColumbus Hilliard(Hilton)',
      'Hampton InnBowling Green(Hilton)',
      'Hampton InnChattanoogaEast Ridge(Hilton)',
      'Hampton InnRinggold, GA(Hilton)',
      'Hampton in Columbus WestBy hilton(Hilton)',
      'Hilton Garden Inn Bettendorf Quad Cities(Hilton)',
      'Hilton Garden Inn Bowling Green(Hilton)',
      'Hilton Garden Inn Louisville Airport(Hilton)',
      'Hilton Garden Inn Louisville East',
      'Hilton Garden Inn LouisvilleMall of St. Matthews',
      'Holiday In and suites College Station IHG',
      'Holiday Inn & Suites Davenport, an IHG Hotel',
      'Holiday Inn Express & Suites East RidgeChattanooga(IHG)',
      'Holiday Inn Express & Suites: Chattanooga Downtown',
      'Holiday Inn ExpressDalton, GA(IHG)',
      'Holiday Inn ExpressRinggold, Ga(IHG)',
      'Holiday Inn Louisville Downtown(IHG)',
      'Holiday InnColumbus Hilliard(IHG)',
      'Holiday InnExpress & Suites KilleenFort Hood Area(IHG)',
      'Holiday InnExpress RinggoldChattanooga Area(IHG)',
      'Holiday InnLouisville East Hurstbourne (IHG)',
      'Holiday InnUniversity PlazaBowling Green(IHG)',
      'Holiday inn Express & Suites LouisvilleEast (IHG)',
      'Home2 Suites By Hilton Columbus West(Hilton)',
      'Homewood Suites by Hilton Columbus Hilliard(Hilton)',
      'Hyatt Place Bowling Green KY(HYATT)',
      'Hyatt PlaceBaton Rouge/I-10(Hyatt)',
      'Hyatt PlaceCollege stationAggieland',
      'Hyatt PlaceLouisville East',
      'Hyatt Regency Louisville(Hyatt)',
      'Hyatt houseLouisville-  East',
      'La Quinta Inn  Davenport & Conference Center(Wyndham)',
      'La Quinta Inn & Suites by Wyndham Baton Rouge Siegen Lane',
      'La Quinta Inn & Suites by Wyndham ChattanoogaEast Ridge',
      'La Quinta Inn & Suites by Wyndham Opelika Auburn',
      'La Quinta Innand SuitesChattanoogaEast Ridge(Wyndham)',
      'LouisvilleMarriott East',
      'Quality Inn Ringgold,GA(Choice)',
      'Quality InnAuburn CampusArea I-85(Choice)',
      'Ramada by Wyndham Bettendorf',
      'Sheraton Louisville Riverside Hotel(Marriott)',
      'Sleep Inn &SuitesAuburn Campus Area I-85 (Choice)',
      'Sonesta Select Bettendorf  lowa',
      'SpringHill Suites Baton Rouge South(Marriott)',
      'Springhill suitesChattanooga South/RinggoldGA (Marriott)',
      'Staybridge Suites Bowling Green(IHG)',
      'The Galt House Hotel, Trademark Collection by (Wyndham)',
      'The Seelbach Hilton Louisville(Hilton)',
      'TowneplaceSuites ChattanoogaSouth/East Ridge(Marriott)',
      'TowneplaceSuitesKilleen(Marriott)',
      'Tru HotelRinggold, GA(Hilton)',
      'Tru by Hilton Baton RougeI-10 East(Hilton)',
      'Tru by HiltonAuburn, AL(Hilton)']

    group_names = ['ATLRG', 'CLLCS', 'IA3021', 'BNAZG', 'SDFEA', 'CSBR', 'AUOAV', 'CHAER', 'KILHH', 'SDFSI', 'CMHWT']

    # Create groups
    groups = [HotelGroup(name=name) for name in group_names]

    db.session.add_all(groups)
    db.session.commit()

    data = {'ATLRG': ['Avid Hotel Ringgold, GA (IHG)', 'Holiday Inn Express Ringgold, Ga (IHG)', 'Holiday Inn Express Dalton, GA (IHG)', 'Holiday Inn Express & Suites: Chattanooga Downtown', 'Tru Hotel Ringgold, GA (Hilton)', 'Hampton Inn Ringgold, GA (Hilton)', 'Hampton Inn Shallowford/ Hamilton place Chattanooga, TN (Hilton)', 'Springhill suites Chattanooga South/Ringgold GA (Marriott)', 'La Quinta Inn & Suites by Wyndham Chattanooga East Ridge', 'Quality Inn Ringgold,GA (Choice)'], 'CLLCS': ['Aggieland Boutique Hotel IHG', 'Holiday In and suites College Station IHG', 'Courtyard Bryan college Stattion Marriott', 'Aloft Hotel College Station Marriott', 'Hampton inn college station Hilton', 'Hyatt Place College station Aggieland'], 'IA3021': ['Sonesta Select Bettendorf lowa', 'La Quinta Inn Davenport & Conference Center (Wyndham)', 'Ramada by Wyndham Bettendorf', 'Hilton Garden Inn Bettendorf Quad Cities (Hilton)', 'Hampton Inn & Suites Davenport (Hilton)', 'Holiday Inn & Suites Davenport, an IHG Hotel', 'Fairfield Inn & Suites by Marriott Davenport Quad Cities', 'Courtyard Bettendorf by Marriott Utica'], 'BNAZG': ['Hyatt Place Bowling Green KY (HYATT)', 'Holiday Inn University Plaza Bowling Green (IHG)', 'Staybridge Suites Bowling Green (IHG)', 'Hilton Garden Inn Bowling Green (Hilton)', 'Hampton Inn Bowling Green (Hilton)', 'Courtyard Bowling Green Convention Center (Marriott)', 'Drury Inn & Suites Bowling Green, KY (Drury)'], 'SDFEA': ['Holiday Inn Louisville East Hurstbourne (IHG)', 'Holiday inn Express & Suites Louisville East (IHG)', 'Hilton Garden Inn Louisville East', 'Hilton Garden Inn Louisville Mall of St. Matthews', 'Louisville Marriott East', 'Courtyard by Marriott Louisville East', 'Baymont by Wyndham Louisville East', 'Hyatt Place Louisville East', 'Hyatt house Louisville- East', 'Drury Inn & Suites Louisville East'], 'CSBR': ['Comfort Suites Baton Rouge South I-10, LA (Choice)', 'Baton Rouge Inn & Suites LSU/Medical Corridor (Choice)', 'Comfort Inn, University area, Baton Rouge,LA (Choice)', 'SpringHill Suites Baton Rouge South (Marriott)', 'La Quinta Inn & Suites by Wyndham Baton Rouge Siegen Lane', 'Hyatt Place Baton Rouge/I-10 (Hyatt)', 'Drury Inn & Suites Baton Rouge (Drury)', 'Tru by Hilton Baton Rouge I-10 East (Hilton)'], 'AUOAV': ['Avid Hotel Auburn, University area, AL (IHG)', 'Tru by Hilton Auburn, AL (Hilton)', 'La Quinta Inn & Suites by Wyndham Opelika Auburn', 'Sleep Inn &Suites Auburn Campus Area I-85 (Choice)', 'Quality Inn Auburn Campus Area I-85 (Choice)'], 'CHAER': ['Holiday Inn Express & Suites East Ridge Chattanooga (IHG)', 'Holiday Inn Express Ringgold Chattanooga Area (IHG)', 'La Quinta Inn and Suites Chattanooga East Ridge (Wyndham)', 'Hampton Inn Chattanooga East Ridge (Hilton)', 'Towneplace Suites Chattanooga South/East Ridge (Marriott)', 'Fairfield Inn and Suites Chattanooga South/East Ridge (Marriott)'], 'KILHH': ['Holiday Inn Express & Suites Killeen Fort Hood Area (IHG)', 'Comfort Inn Curry drive Killeen, TX (Choice)', 'Fairfield Inn and Suites Killeen (Marriott)', 'Towneplace Suites Killeen (Marriott)', 'Best Western Plus Killeen/Fort Hood Hotel and Suites'], 'SDFSI': ['Sheraton Louisville Riverside Hotel (Marriott)', 'Fairfield Inn & Suites Louisville North (Marriott)', 'AC Hotel Louisville Downtown (Marriott)', 'Courtyard louisville Downtown (Marriott)', 'Holiday Inn Louisville Downtown (IHG)', 'Hilton Garden Inn Louisville Airport (Hilton)', 'Embassy Suites by Hilton Louisville Downtown (Hilton)', 'The Seelbach Hilton Louisville (Hilton)', 'Hyatt Regency Louisville (Hyatt)', 'The Galt House Hotel, Trademark Collection by (Wyndham)'], 'CMHWT': ['Courtyard Columbus West / Hilliard (Marriott)', 'Fairfield Inn & Suites Columbus Hilliard (Marriott)', 'Holiday Inn Columbus Hilliard (IHG)', 'Avid hotel Columbus Northwest Hilliard (IHG)', 'Home2 Suites By Hilton Columbus West (Hilton)', 'Hampton in Columbus West By hilton (Hilton)', 'Hampton Inn and Suites Columbus Hilliard (Hilton)', 'Homewood Suites by Hilton Columbus Hilliard (Hilton)']}

    # Assign hotels to groups
    hotels = []
    for group_name, hotel_names in data.items():
        group = HotelGroup.query.filter_by(name=group_name).first()  # Fetch HotelGroup instance
        if group:
            for hotel_name in hotel_names:
            #   hotel = Hotel(name=hotel_name, group=group)
              hotel = Hotel(name=hotel_name, groups=[group])
              hotels.append(hotel)
              db.session.add(hotel)

    db.session.commit()

    # Add room prices for each hotel
    room_types = ['King', 'Queen']
    start_date = date(2024, 1, 1)
    for hotel in hotels:
        for i in range(30):  # Add prices for 30 days
            for room_type in room_types:
                room_price = RoomPrice(
                    hotel_id=hotel.hotel_id,
                    date=start_date + timedelta(days=i),
                    room_type=room_type,
                    price=int(random.uniform(100, 300))
                )
                db.session.add(room_price)

    db.session.commit()