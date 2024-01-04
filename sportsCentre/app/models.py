

"""
  A file that manage and define database 
"""
#source: Web for Development CWk Shopping...
#made by Ayesha
from app import db
from datetime import datetime

class users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    zipcode = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    country = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    memberType = db.Column(db.String(200))
    status = db.Column(db.Boolean, nullable=False, default=False)
    
#management users
class musers(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    zipcode = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    country = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    
    
#added by geeyoon and Natalie
#employee users
class eusers(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    zipcode = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    country = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    position = db.Column(db.String(200))


#added more values
# eddited by Sandra
class facility(db.Model):
    facilityId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    roomCounter = db.Column(db.Integer)
    decription = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    openTime = db.Column(db.Time)
    closeTime = db.Column(db.Time)

class activity(db.Model):
    activityId = db.Column(db.Integer, db.ForeignKey("users.userId"), primary_key=True)
    facilityId = db.Column(db.Integer, db.ForeignKey("facility.facilityId"))
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
   

#by sandra 
class activityEvent(db.Model):
    activityEventId = db.Column(db.Integer, db.ForeignKey("users.userId"), primary_key=True)
    activityId = db.Column(db.Integer, db.ForeignKey("activity.activityId"))
    facilityId = db.Column(db.Integer, db.ForeignKey("facility.facilityId"))
    name = db.Column(db.String(200))
    startTime = db.Column(db.Time)
    endTime = db.Column(db.Time)
    day = db.Column(db.DateTime)

class membership(db.Model):
    membershipId = db.Column(db.Integer, db.ForeignKey("users.userId"), primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)

#For all the bookings made by the user
class bookings(db.Model):
    bookingId = db.Column(db.Integer, db.ForeignKey("users.userId"), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.userId"), primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey("activity.activityId"), db.ForeignKey("membership.membershipId"))
    buyClass = db.Column(db.Integer)
    
# edit booking for users (employee page)
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.facilityId'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)

    facility = db.relationship('facility', backref='bookings')
    user = db.relationship('users', backref='bookings')
    
    
#by Natalie
#Employee work schedule
class Work(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    staffId = db.Column(db.Integer, db.ForeignKey('eusers.userId'))
    date = db.Column(db.String(10))
    startTime = db.Column(db.String(10))
    endTime = db.Column(db.String(10))
    hourlyRate = db.Column(db.Integer)
    position = db.Column(db.String(200), db.ForeignKey('eusers.position'))
    facilityName = db.Column(db.String(50))

