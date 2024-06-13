from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

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
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/editor', methods=['GET', 'POST'])
def editor():
    if request.method == 'POST':
        prices = request.form.to_dict()
        if prices:
            for key, value in prices.items():
                parts = key.split('][')
                hotel_id = int(parts[0].split('[')[-1])
                date_str = parts[1]
                room_type = parts[2].split(']')[0]

                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                price = value if value.isdigit() or value.upper() == "SOLD" else None

                existing_price = RoomPrice.query.filter_by(hotel_id=hotel_id, date=date, room_type=room_type).first()

                if existing_price:
                    existing_price.price = price
                else:
                    new_price = RoomPrice(hotel_id=hotel_id, date=date, room_type=room_type, price=price)
                    db.session.add(new_price)

            db.session.commit()
            return redirect(url_for('editor'))

    groups = HotelGroup.query.all()
    
    group_id = request.args.get('group_id')
    dates_str = request.args.get('dates')
    
    if group_id and dates_str:
        group = HotelGroup.query.get(group_id)
        if not group:
            return "Group not found", 404
        
        hotels = db.session.query(Hotel).join(HotelGroupAssociation).filter(HotelGroupAssociation.hotel_group_id == group_id).all()
        dates = [datetime.strptime(date.strip(), '%Y-%m-%d').date() for date in dates_str.split(',')]

        prices = {}
        for hotel in hotels:
            prices[hotel.name] = {}
            for date in dates:
                prices[hotel.name][date.strftime('%Y-%m-%d')] = {'King': None, 'Queen': None}

                existing_king_price = RoomPrice.query.filter_by(hotel_id=hotel.hotel_id, date=date, room_type='King').first()
                if existing_king_price:
                    prices[hotel.name][date.strftime('%Y-%m-%d')]['King'] = existing_king_price.price

                existing_queen_price = RoomPrice.query.filter_by(hotel_id=hotel.hotel_id, date=date, room_type='Queen').first()
                if existing_queen_price:
                    prices[hotel.name][date.strftime('%Y-%m-%d')]['Queen'] = existing_queen_price.price
        
        form = {}
        for hotel in hotels:
            form[hotel.hotel_id] = {}
            for date in dates:
                form[hotel.hotel_id][date.strftime('%Y-%m-%d')] = {'King': None, 'Queen': None}

                existing_price = RoomPrice.query.filter_by(hotel_id=hotel.hotel_id, date=date, room_type='King').first()
                if existing_price:
                    form[hotel.hotel_id][date.strftime('%Y-%m-%d')]['King'] = existing_price.price

                existing_price = RoomPrice.query.filter_by(hotel_id=hotel.hotel_id, date=date, room_type='Queen').first()
                if existing_price:
                    form[hotel.hotel_id][date.strftime('%Y-%m-%d')]['Queen'] = existing_price.price
        
        return render_template('editor.html', group_name=group.name, hotels=hotels, dates=dates, groups=groups, form=form, prices=prices)

    return render_template('editor.html', groups=groups)

@app.route('/insert_prices', methods=['POST'])
def insert_prices():
    prices = request.form.to_dict()
    
    if prices:
        for key, value in prices.items():
            parts = key.split('][')
            hotel_id = int(parts[0].split('[')[-1])
            date_str = parts[1]
            room_type = parts[2].split(']')[0]

            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            price = value if value.isdigit() or value.upper() == "SOLD" else None

            existing_price = RoomPrice.query.filter_by(hotel_id=hotel_id, date=date, room_type=room_type).first()

            if existing_price:
                existing_price.price = price
                db.session.commit()
            else:
                if price is not None:
                    db.session.add(RoomPrice(hotel_id=hotel_id, date=date, room_type=room_type, price=price))
                    db.session.commit()

        return redirect(url_for('editor'))
    
    return "No prices submitted"

@app.route('/viewer', methods=['GET'])
def viewer():
    groups = HotelGroup.query.all()
    return render_template('viewer.html', groups=groups)

@app.route('/get_hotels/<group_id>', methods=['GET'])
def get_hotels(group_id):
    hotels = db.session.query(Hotel).join(HotelGroupAssociation).filter(HotelGroupAssociation.hotel_group_id == group_id).all()
    hotels_list = [{'hotel_id': hotel.hotel_id, 'name': hotel.name} for hotel in hotels]
    return jsonify({'hotels': hotels_list})

@app.route('/get_group_info/<group_id>', methods=['GET'])
def get_group_info(group_id):
    group = HotelGroup.query.get(group_id)
    if group:
        hotels = Hotel.query.join(HotelGroupAssociation).filter(HotelGroupAssociation.hotel_group_id == group_id).all()
        hotels_info = [{'name': hotel.name, 'hotel_id': hotel.hotel_id} for hotel in hotels]
        return render_template('group_info.html', group=group, hotels=hotels_info)
    else:
        return jsonify({'error': 'Group not found'}), 404

@app.route('/view_prices', methods=['POST'])
def view_prices():
    print(request.form)
    group_id = request.form['group_id']
    dates_str = request.form['dates']
    
    # Parse the date range
    try:
        start_date_str, end_date_str = dates_str.split(' to ')
        start_date = datetime.strptime(start_date_str.strip(), '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str.strip(), '%Y-%m-%d').date()
    except ValueError:
        return "Incorrect date format. Please use YYYY-MM-DD to YYYY-MM-DD format.", 400

    # Generate a list of dates within the range
    dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    
    prices = {}  # Initialize prices dictionary

    # Fetch hotels associated with the given group_id
    hotels = db.session.query(Hotel).join(HotelGroupAssociation).filter(HotelGroupAssociation.hotel_group_id == group_id).all()

    # Initialize prices dictionary with hotel names and dates
    for hotel in hotels:
        prices[hotel.name] = {date.strftime('%Y-%m-%d'): {'King': None, 'Queen': None} for date in dates}

    # Fetch all RoomPrice entries for the selected hotels and dates
    room_prices = RoomPrice.query.filter(RoomPrice.hotel_id.in_([hotel.hotel_id for hotel in hotels]), RoomPrice.date.in_(dates)).all()

    # Update prices dictionary with fetched prices
    for price in room_prices:
        hotel = db.session.query(Hotel).get(price.hotel_id)
        if hotel and hotel.name in prices:
            date_str = price.date.strftime('%Y-%m-%d')
            prices[hotel.name][date_str][price.room_type] = price.price
    
    group_name = HotelGroup.query.get(group_id).name

    return render_template('view_prices.html', prices=prices, dates=dates, group_name=group_name)


@app.route('/manage_groups', methods=['GET', 'POST'])
def manage_groups():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add':
            name = request.form['name']
            new_group = HotelGroup(name=name)
            db.session.add(new_group)
            db.session.commit()
        elif action == 'delete':
            group_id = request.form['group_id']
            group = HotelGroup.query.get(group_id)
            db.session.delete(group)
            db.session.commit()
        elif action == 'update':
            group_id = request.form['group_id']
            name = request.form['name']
            group = HotelGroup.query.get(group_id)
            group.name = name
            db.session.commit()
        return redirect(url_for('manage_groups'))
    
    groups = HotelGroup.query.all()
    return render_template('manage_groups.html', groups=groups)

@app.route('/manage_hotels', methods=['GET', 'POST'])
def manage_hotels():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add':
            name = request.form['name']
            group_id = request.form['group_id']
            
            # Check if the hotel with the given name already exists
            existing_hotel = Hotel.query.filter_by(name=name).first()
            if existing_hotel:
                # If the hotel already exists, use its ID
                hotel_id = existing_hotel.hotel_id
            else:
                # If the hotel doesn't exist, create a new one
                new_hotel = Hotel(name=name)
                db.session.add(new_hotel)
                db.session.commit()
                hotel_id = new_hotel.hotel_id
            
            # Create association between the hotel and the group
            association = HotelGroupAssociation(hotel_id=hotel_id, hotel_group_id=group_id)
            db.session.add(association)
            db.session.commit()
        elif action == 'delete':
            hotel_id = request.form['hotel_id']
            hotel = Hotel.query.get(hotel_id)
            db.session.delete(hotel)
            db.session.commit()
        elif action == 'update':
            hotel_id = request.form['hotel_id']
            name = request.form['name']
            hotel = Hotel.query.get(hotel_id)
            hotel.name = name
            db.session.commit()
        return redirect(url_for('manage_hotels'))
    
    groups = HotelGroup.query.all()
    hotels = Hotel.query.all()
    return render_template('manage_hotels.html', groups=groups, hotels=hotels)

if __name__ == '__main__':
    app.run()
