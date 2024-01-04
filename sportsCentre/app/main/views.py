"""
      A file to compose page for main pages
"""


import hashlib
from flask import redirect, render_template, session, url_for, jsonify, request, current_app
from flask_cors import cross_origin
from flask import request, jsonify
import qrcode
from io import BytesIO
from flask import send_file


import json
from . import main
import sqlite3
from .forms import parse, searchProd,getLoginDetails, mgetLoginDetails, egetLoginDetails
from flask import request
from werkzeug.wrappers import Response, Request
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from app.models import eusers, users
import re
from app import db
from datetime import date
from flask import flash
from os import urandom
import base64

#by ayesha
#qr code takes to user home page
@main.route('/qrcode')
def qrcode_generator():
    # Generate the QR code image using the `qrcode` library
    img = qrcode.make(request.host_url)

    # Convert the image to a PNG format
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Send the image to the user
    return send_file(img_io, mimetype='image/png')

#by geeyoon
@main.route('/inbox')
def inbox():
  if 'email' not in session:
        return render_template('inbox.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("inbox.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/emtimetable', methods=['GET', 'POST'])
def emtimetable():
    if request.method == 'POST':
        position = request.form.get('position')
        facility = request.form.get('facility')

    if position == 'instructor':
        # render instructor timetable page
        return render_template('inworkingtime.html')
    elif position == 'receptionist':
        # render receptionist timetable page
        return render_template('reworkingtime.html')
    elif position == 'cleaner':
        # render cleaner timetable page
        return render_template('reworkingtime.html')
    elif position == 'life_guard':
        # render life guard timetable page
        return render_template('liworkingtime.html')
    else:
        # handle invalid input
        return render_template('error.html', message='Invalid input.')

# Route to display the timetable
#by ayesha
@main.route('/timetable')
def timetable():
    if 'email' not in session:
        return render_template('calendar.html')
    loggedIn, firstName = getLoginDetails()
    times = ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']
    return render_template('timetable.html', times=times, loggedIn=loggedIn, firstName=firstName)

# First released by ayesha
@main.route('/calendar', methods=['GET', 'POST'])
def calendar():
  if 'email' not in session:
        return render_template('calendar.html')
  loggedIn, firstName = getLoginDetails()
  
#   if request.method == "POST":
#     day= request.form['date']
#     print("date" + day)
#     with sqlite3.connect('app.db') as con:
#         cur = con.cursor()
#         # retrieve userId from users 
#         cur.execute("SELECT userId, memberhshipId FROM users WHERE email = ?",
#             (session['email'],))
#         userId, membershipId = cur.fetchone()

#         # Insert a new row into the bookings table for each booking
#         cur.execute("INSERT INTO bookings (userId, membershipId,day) VALUES ( ?, ?, ?)",
#                         (userId, membershipId, day, ))

#         # to commit for updated data 
#         con.commit()
  return render_template("calendar.html", loggedIn=loggedIn, firstName=firstName)


@main.route('/_currentDay')
def current_day():
    # Replace this with your actual logic for generating the _currentDay page
    return render_template('_currentDay')


#by ayesha
@main.route('/usage')
def usage():
    if 'email' not in session:
        return render_template('managerhome.html')
    loggedIn, firstName = mgetLoginDetails()
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute('SELECT facilityId, COUNT(*) FROM bookings GROUP BY facilityId')
    results = c.fetchall()
    c.execute('SELECT activityId, COUNT(*) FROM bookings GROUP BY activityId')
    results1 = c.fetchall()
    c.execute('SELECT activityEventId, COUNT(*) FROM bookings GROUP BY activityEventId')
    results2 = c.fetchall()
    c.execute('SELECT membershipId, COUNT(*) FROM bookings GROUP BY membershipId')
    results3 = c.fetchall()

    conn.close()

    return render_template('usage.html', results=results, results1=results1, results2=results2, results3=results3, loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/managerhome')
def managerhome():
  if 'email' not in session:
        return render_template('managerhome.html')
  loggedIn, firstName = mgetLoginDetails()
  return render_template("managerhome.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/staffmembers')
def staffmembers():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM eusers")
        eusers = cur.fetchall()

  eusers = parse(eusers)
  loggedIn, firstName = getLoginDetails()
  return render_template('staffmembers.html', eusers=eusers, loggedIn=loggedIn, firstName=firstName)

#by geeyoon
@main.route('/employeehome')
def employeehome():
  if 'email' not in session:
        return render_template('employeehome.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("employeehome.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/privacy')
def privacy():
  if 'email' not in session:
        return render_template('privacy.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("privacy.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/eprivacy')
def eprivacy():
  if 'email' not in session:
        return render_template('eprivacy.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("eprivacy.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/mprivacy')
def mprivacy():
  if 'email' not in session:
        return render_template('mprivacy.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("mprivacy.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/payment')
def payment():
  if 'email' not in session:
        return render_template('pay/payment.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("pay/payment.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha, edited by Natalie
@main.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('auth.loginForm'))
    loggedIn, firstName = getLoginDetails()
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        # Enforce password requirements
        if not (re.search('[A-Z]', newPassword) and re.search('[^A-Za-z0-9]', newPassword) and len(newPassword) >= 8):
            msg = "Password must be at least 8 characters long, contain at least one capital letter, and at least one special character"
            return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        if oldPassword == newPassword:
            msg = "New password cannot be the same as the old password"
            return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
    else:
        return render_template("changePassword.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha, edited by Natalie           
@main.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.editProfile'))
      
# Manager edit profile - by ayesha
@main.route('/personaldetails')
def personaldetails():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = mgetLoginDetails()
    return render_template("personaldetails.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route("/account/personaldetails/edit")
def meditProfile():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = mgetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM musers WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("meditProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha, edited by Natalie
@main.route("/account/personaldetails/changePassword", methods=["GET", "POST"])
def mchangePassword():
    if 'email' not in session:
        return redirect(url_for('auth.mloginForm'))
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        # Enforce password requirements
        if not (re.search('[A-Z]', newPassword) and re.search('[^A-Za-z0-9]', newPassword) and len(newPassword) >= 8):
            msg = "Password must be at least 8 characters long, contain at least one capital letter, and at least one special character"
            return render_template("mchangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        if oldPassword == newPassword:
            msg = "New password cannot be the same as the old password"
            return render_template("mchangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM musers WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE musers SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("mchangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("mchangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
    else:
        return render_template("mchangePassword.html", loggedIn=loggedIn, firstName=firstName)


#by ayesha      
@main.route("/mupdateProfile", methods=["GET", "POST"])
def mupdateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE musers SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.meditProfile'))

# First released by moon - membership status in users table
# modified by ayesha - membershipId in bookings table
@main.route('/membership', methods=["GET", "POST"])
def membership():
    # log-in check 
    if 'email' not in session:
        return render_template('pay/memship.html')
    loggedIn, firstName = getLoginDetails()
    
    if request.method == "POST":
        status = request.form['status']
        memberType = request.form['membership_type']
        with sqlite3.connect('app.db') as con:
            cur = con.cursor()
            # to retrieve the 'userId' value from the 'users' table based on the email address
            # in the 'session' object 
            cur.execute("SELECT userId FROM users WHERE email = ?",
                         (session['email'],))
            # to retrieve the first row of the result set using the 'fetchone()' method  
            row = cur.fetchone()
            userId = row[0]
            # to update these column 
            cur.execute("UPDATE users SET status=?, memberType=? WHERE userId=?",
                         (status, memberType, userId))
            
            # to retrieve the 'membershipId' value from the 'memberships' table based on the 'membership_type'
            cur.execute("SELECT membershipId FROM membership WHERE name = ?",
                         (memberType,))
            # to retrieve the first row of the result set using the 'fetchone()' method  
            row = cur.fetchone()
            membershipId = row[0]
            # to insert booking data into the bookings table, including the membershipId column
            cur.execute("INSERT INTO bookings (userId, membershipId) VALUES (?, ?)",
                         (userId, membershipId))
            # to commit the updated data 
            con.commit()
        return redirect(url_for('main.payment'))
    return render_template("pay/memship.html", loggedIn=loggedIn, firstName=firstName )

#modified by moon 
@main.route('/profile')
def profile():
    #  login check 
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        # to retrieve userId same method above membersip decorater  
        userId = cur.execute("SELECT userId FROM users WHERE email = ?", 
                             (session['email'],))
        row = cur.fetchone()
        userId = row[0]
        # to retrieve status value 
        status = cur.execute("SELECT status FROM users WHERE userId = ? ",
                             (userId,))
        status = cur.fetchone()[0]
        # to retrieve membership value 
        if status is not None:
            status = status
        membership = cur.execute("SELECT memberType FROM users WHERE userId = ? ",
                             (userId,))
        membership = cur.fetchone()[0]
        print("membertype: ", membership)
        cur.close()
    conn.close()
    return render_template("profile.html", loggedIn=loggedIn, firstName=firstName,
                            status=status, membership=membership, userId=userId)

#firstly released by moon 
@main.route('/<int:userId>/cancelMembership', methods=['POST'])
def cancelMembership(userId):
    if 'email' not in session:
        return render_template('auth/login.html')
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
        with sqlite3.connect('app.db') as con:
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            userId=int(userId)
            cur.execute('UPDATE users SET memberType = NULL, status = NULL where userId =?',
                         (userId,))
            con.commit() 
    return render_template("/profile.html",
                            loggedIn=loggedIn, firstName=firstName)

# by geeyoon
@main.route('/activities')
def activities():
  if 'email' not in session:
        return render_template('activities.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("activities.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/equipment')
def equipment():
  if 'email' not in session:
        return render_template('equipment.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("equipment.html", loggedIn=loggedIn, firstName=firstName)

#by sandra
from datetime import datetime, timedelta
from collections import Counter

@main.route('/cart')
def cart():
    if 'email' not in session:
        return render_template('auth/login.html', next='main.cart')

    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        cur.execute('''
        SELECT facility.name, activity.name, activityEvent.name, bookings.day, bookings.startTime, bookings.endTime, activity.price
        FROM bookings 
        INNER JOIN facility ON facility.facilityId=bookings.facilityId 
        INNER JOIN activity ON activity.activityId=bookings.activityId 
        LEFT JOIN activityEvent ON activityEvent.activityEventId=bookings.activityEventId
        WHERE bookings.userId = (SELECT userId FROM users WHERE email = ?) 
            AND bookings.membershipId IS NULL
            AND bookings.activityId IS NOT NULL
            AND bookings.facilityId IS NOT NULL
            AND bookings.activityEventId IS NOT NULL
            AND bookings.buyClass IS NULL
    ''', (session['email'],))

        rows1 = cur.fetchall()
        
        # Create a counter to store the number of bookings made within the past 7 days
        bookings_count = Counter()
        bookings_count_extra = Counter()
        total_price_discount= 0
        total_price_nondiscount = 0
        totalPrice = 0
        discount_price = 0

        # Iterate over the rows of data and count the bookings made within the past 7 days
        for row in rows1:
            if row[3] is None:
                continue
            
            try:
                day = datetime.strptime(row[3], '%Y-%m-%d').date()
            except ValueError:
                # If the day is not formatted correctly, try to parse it as a date
                try:
                    day = datetime.strptime(row[3], '%A').date()
                except ValueError:
                    day = None  # set day to None if it cannot be parsed as a date
            
            if day is not None:
                # Count only the bookings made within the last 7 days
                if day <= datetime.now().date() + timedelta(days=7) and day >= datetime.now().date() or day == datetime(1900, 1, 1).date():
                    bookings_count[day] += 1
                    total_price_discount += float(row[6])
                else:
                    bookings_count_extra[day] += 1
                    total_price_nondiscount += float(row[6])
                        
        total_bookings = sum(bookings_count.values())
        total_bookings_extra = sum(bookings_count_extra.values())

        # print(bookings_count[day])
        # print(bookings_count)


        if total_bookings >= 3:
            discount_price = total_price_discount - (15/100 * total_price_discount)
            totalPrice = total_price_nondiscount + discount_price
        else:
            totalPrice = total_price_nondiscount + total_price_discount

        print(f"totalPrice: {totalPrice}")
        
        rows1 = parse(rows1)

    return render_template("cart.html")

@main.route('/checkout')
def checkout():
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        cur.execute('UPDATE bookings SET buyClass = 1 WHERE userId = (SELECT userId FROM users WHERE email = ?) AND buyClass IS NULL',
                    (session['email'],))

        conn.commit()

    return redirect(url_for('main.payment'))

#by ayesha
@main.route('/ecart')
def ecart():
    if 'email' not in session:
        return render_template('ecart.html')
    
    loggedIn, firstName = egetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        cur.execute('''
        SELECT facility.name, activity.name, activityEvent.name, bookings.day, bookings.startTime, bookings.endTime, activity.price
        FROM bookings 
        INNER JOIN facility ON facility.facilityId=bookings.facilityId 
        INNER JOIN activity ON activity.activityId=bookings.activityId 
        LEFT JOIN activityEvent ON activityEvent.activityEventId=bookings.activityEventId
        WHERE bookings.userId = (SELECT userId FROM users WHERE email = ?) 
            AND bookings.membershipId IS NULL
            AND bookings.activityId IS NOT NULL
            AND bookings.facilityId IS NOT NULL
            AND bookings.activityEventId IS NOT NULL
            AND bookings.buyClass IS NULL
    ''', (session['email'],))

        rows1 = cur.fetchall()
        
        # Create a counter to store the number of bookings made within the past 7 days
        bookings_count = Counter()
        bookings_count_extra = Counter()
        total_price_discount= 0
        total_price_nondiscount = 0
        totalPrice = 0
        discount_price = 0

        # Iterate over the rows of data and count the bookings made within the past 7 days
        for row in rows1:
            if row[3] is None:
                continue
            
            try:
                day = datetime.strptime(row[3], '%Y-%m-%d').date()
            except ValueError:
                # If the day is not formatted correctly, try to parse it as a date
                try:
                    day = datetime.strptime(row[3], '%A').date()
                except ValueError:
                    day = None  # set day to None if it cannot be parsed as a date
            
            if day is not None:
                # Count only the bookings made within the last 7 days
                if day <= datetime.now().date() + timedelta(days=7) and day >= datetime.now().date() or day == datetime(1900, 1, 1).date():
                    bookings_count[day] += 1
                    total_price_discount += float(row[6])
                else:
                    bookings_count_extra[day] += 1
                    total_price_nondiscount += float(row[6])
                        
        total_bookings = sum(bookings_count.values())
        total_bookings_extra = sum(bookings_count_extra.values())

        # print(bookings_count[day])
        # print(bookings_count)


        if total_bookings >= 3:
            discount_price = total_price_discount - (15/100 * total_price_discount)
            totalPrice = total_price_nondiscount + discount_price
        else:
            totalPrice = total_price_nondiscount + total_price_discount

        print(f"totalPrice: {totalPrice}")
        
        rows1 = parse(rows1)

    return render_template("ecart.html", rows1=rows1, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/echeckout')
def echeckout():
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        cur.execute('UPDATE bookings SET buyClass = 1 WHERE userId = (SELECT userId FROM users WHERE email = ?) AND buyClass IS NULL',
                    (session['email'],))

        conn.commit()

    return redirect(url_for('main.epayment'))

#by ayesha
@main.route('/epayment')
def epayment():
  if 'email' not in session:
        return render_template('pay/epayment.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("pay/epayment.html", loggedIn=loggedIn, firstName=firstName)

# by geeyoon
@main.route('/qna')
def qna():
  if 'email' not in session:
        return render_template('qna.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("qna.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
@main.route('/elder')
def elder():
  if 'email' not in session:
        return render_template('elder.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("elder.html", loggedIn=loggedIn, firstName=firstName)

# by geeyoon
@main.route('/hiring')
def hiring():
  if 'email' not in session:
        return render_template('hiring.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("hiring.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route('/ehiring')
def ehiring():
  if 'email' not in session:
        return render_template('ehiring.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("ehiring.html", loggedIn=loggedIn, firstName=firstName)

# by geeyoon
@main.route('/aboutUs')
def aboutUs():
  if 'email' not in session:
        return render_template('aboutUs.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("aboutUs.html", loggedIn=loggedIn, firstName=firstName)

@main.route('/maboutUs')
def maboutUs():
  if 'email' not in session:
        return render_template('maboutUs.html')
  loggedIn, firstName = getLoginDetails()
  return render_template("maboutUs.html", loggedIn=loggedIn, firstName=firstName)

# by geeyoon
@main.route('/eaboutUs')
def eaboutUs():
  if 'email' not in session:
        return render_template('eaboutUs.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("eaboutUs.html", loggedIn=loggedIn, firstName=firstName)

# by geeyoon
@main.route('/eqna')
def eqna():
  if 'email' not in session:
        return render_template('eqna.html')
  loggedIn, firstName = egetLoginDetails()
  return render_template("eqna.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route('/mqna')
def mqna():
  if 'email' not in session:
        return render_template('mqna.html')
  loggedIn, firstName = mgetLoginDetails()
  return render_template("mqna.html", loggedIn=loggedIn, firstName=firstName)

# by sandra
@main.route('/facilities')
def facilities():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        #showing facility table in facility.html
        cur.execute("SELECT facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility")
        facility = cur.fetchall()
        #team events, clases table
        cur.execute('''
        SELECT facility.name, activity.name, activity.price FROM activity
        INNER JOIN facility ON facility.facilityId = activity.facilityId
        ''')
        # Fetching rows from the result table
        result = cur.fetchall()
        #showing activity table in facility.html
        cur.execute('''
        SELECT  facility.name, activityEvent.name, activityEvent.day, activityEvent.startTime, activityEvent.endTime FROM activityEvent
        INNER JOIN facility ON activityEvent.facilityId = facility.facilityId
        ''')

# Fetching rows from the result table
        result1 = cur.fetchall()

  facility = parse(facility)
  result = parse(result)
  result1 = parse(result1)
  loggedIn, firstName = getLoginDetails()
  return render_template('facilities.html', result=result, result1=result1,facility=facility, loggedIn=loggedIn, firstName=firstName)

# See all facilities - for manager 
#by ayesha
@main.route('/mfacilities')
def mfacilities():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        #showing facility table in facility.html
        cur.execute("SELECT facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility")
        facility = cur.fetchall()
        #team events, clases table
        cur.execute('''
        SELECT facility.name, activity.name, activity.price FROM activity
        INNER JOIN facility ON facility.facilityId = activity.facilityId
        ''')
        # Fetching rows from the result table
        result = cur.fetchall()
        #showing activity table in facility.html
        cur.execute('''
        SELECT  facility.name, activityEvent.name, activityEvent.day, activityEvent.startTime, activityEvent.endTime FROM activityEvent
        INNER JOIN facility ON activityEvent.facilityId = facility.facilityId
        ''')

# Fetching rows from the result table
        result1 = cur.fetchall()

  facility = parse(facility)
  result = parse(result)
  result1 = parse(result1)
  loggedIn, firstName = mgetLoginDetails()
  return render_template('mfacilities.html', result=result, result1=result1,facility=facility, loggedIn=loggedIn, firstName=firstName)

# ================== manager - delete facilities ===========================
#by ayesha
@main.route('/<int:facilityId>/Deletef', methods=['POST'])
def Deletef(facilityId):
    if 'email' not in session:
        return render_template('managerhome.html')
    loggedIn, firstName = mgetLoginDetails()
    if request.method == "POST":
        with sqlite3.connect('app.db') as con:
            con.row_factory=sqlite3.Row

            cur = con.cursor()
            facilityId=int(facilityId)
            
            cur.execute('DELETE from facility where facilityId =?', (facilityId,))
            con.commit() 
            # rows = cur.fetchone()
            return redirect("/mfacilities")
    return render_template("managerhome.html", loggedIn=loggedIn, firstName=firstName)

# ================== manager - delete activities ===========================
#by sandra, edited by Natalie
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = base64.b64encode(urandom(48)).decode('utf-8')
    return session['_csrf_token']

@main.route('/Deletea', methods=['POST'])
@cross_origin()
def Deletea():
    if 'email' not in session:
        return render_template('managerhome.html')
    loggedIn, firstName = mgetLoginDetails()

    if request.method == "POST":
        # Check if it's an AJAX request
        if request.is_json:
            activityName = request.json['activityName']
        else:
            activityName = request.form['activityName']

        print(f"Deleting activity with name: {activityName}")  # Print activityName

        with sqlite3.connect('app.db') as con:
            con.row_factory = sqlite3.Row

            cur = con.cursor()

            cur.execute('SELECT activityId from activity where name =?', (activityName,))
            result = cur.fetchone()
            if result is None:
                print("Activity not found")  # Print when activity is not found
                return render_template('error.html', error_message="Activity not found")

            activityId = result['activityId']
            print(f"Deleting activity with ID: {activityId}")  # Print activityId
            cur.execute('DELETE from activity where activityId =?', (activityId,))
            con.commit()

            if request.is_json:
                return jsonify({'status': 'success'})
            else:
                return redirect("/mactivities")

    return render_template("managerhome.html", loggedIn=loggedIn, firstName=firstName)


# Allowing manager to edit facilities
#by ayesha
@main.route("/meditfacilities")
def meditfacilities():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = mgetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT facilityId, name, roomCounter description, capacity, openTime, closeTime FROM facility WHERE name = ?", (['facilityId'] ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("meditfacilities.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)

#by ayesha      
@main.route("/mupdatefacilities", methods=["GET", "POST"])
def mupdatefacilities():
    if request.method == 'POST':
        facilityId = request.form['facilityId']
        name = request.form['name']
        roomCounter = request.form['roomCounter']
        description = request.form['description']
        capacity = request.form['capacity']
        openTime = request.form['openTime']
        closeTime = request.form['closeTime']
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE facility SET roomCounter = ?, description = ?, capacity = ?, openTime = ?, closeTime = ? WHERE name = ?', (roomCounter, description, capacity, openTime, closeTime, name))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.meditfacilities', msg=msg))

# manager - adding facilities 
#by ayesha
@main.route("/maddfacilityForm")
def maddfacilityForm():
    return redirect(url_for('main.meditfacilities', msg=''))


@main.route("/maddfacility", methods = ['GET', 'POST'])
def maddfacility():
    loggedIn, firstName = mgetLoginDetails()
    if request.method == 'POST':
        #Parse form data
        name = request.form['name']
        roomCounter = request.form['roomCounter']
        description = request.form['description']
        capacity = request.form['capacity']
        openTime = request.form['openTime']
        closeTime = request.form['closeTime']

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO facility (name, roomCounter, description, capacity, openTime, closeTime) VALUES (?, ?, ?, ?, ?, ?)', (name, roomCounter, description, capacity, openTime, closeTime))
                con.commit()

                msg = "Added Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return redirect(url_for('main.meditfacilities', msg=msg))  

# See all activities - for manager 
#by ayesha
@main.route('/mactivities')
def mactivities():
  with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        #team events, clases table
        cur.execute('''
        SELECT facility.name, activity.name, activity.price FROM activity
        INNER JOIN facility ON facility.facilityId = activity.facilityId
        ''')
        # Fetching rows from the result table
        result = cur.fetchall()
  result = parse(result)
  loggedIn, firstName = mgetLoginDetails()
  return render_template('mactivities.html', result=result, loggedIn=loggedIn, firstName=firstName)

# Allowing manager to edit facilities
#by ayesha, edited by Natalie
@main.route("/mupdateactivities", methods=["GET", "POST"])
def mupdateactivities():
    if request.method == 'POST':
        activityId = request.form['activityId']
        name = request.form['name']
        price = request.form['price']
        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('UPDATE activity SET price = ? WHERE activityId = ?', (price, activityId))
                con.commit()
                flash("Saved Successfully")
            except:
                con.rollback()
                flash("Error occurred", "danger")
        con.close()
        return redirect(url_for('main.meditactivities', msg=msg))

@main.route("/meditactivities")
def meditactivities():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = mgetLoginDetails()
    msg = request.args.get('msg')
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT activityId, facilityId, name, price FROM activity WHERE activityId = ?", (['activityId'] ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("meditactivities.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, msg=msg)

#by ayesha
# manager - adding activities 
@main.route("/maddactivityForm")
def maddactivityForm():
    return render_template("maddactivity.html")

#by ayesha
@main.route("/maddactivity", methods = ['GET', 'POST'])
def maddactivity():
    loggedIn, firstName = mgetLoginDetails()
    if request.method == 'POST':
        #Parse form data
        facilityId = request.form['facilityId']
        name = request.form['name']
        price = request.form['price']

        with sqlite3.connect('app.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO activity (facilityId, name, price) VALUES (?, ?, ?)', (facilityId, name, price))
                con.commit()

                msg = "Added Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("managerhome.html", error=msg, loggedIn=loggedIn, firstName=firstName)  

#by ayesha - functionality
#edited by sandra and ayesha - debugging
#putting capacity and membership by moon 
@main.route('/booking', methods=['GET', 'POST'])
def booking():
    loggedIn, firstName = getLoginDetails()
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    facilities = cursor.execute("SELECT facilityId, name FROM facility").fetchall()
    activities = []
    events = []
    message = None

    if request.method == 'POST':
        facility_id = request.form['facility']

        if facility_id is not None:
            activities = cursor.execute("SELECT activity.activityId, activity.name FROM activity JOIN facility ON activity.facilityId = facility.facilityId WHERE facility.facilityId = ?", (facility_id,)).fetchall()
            if request.form.get('activity'):
                activity_id = request.form['activity']
                events = cursor.execute("SELECT activityEvent.activityEventId, activityEvent.name, activityEvent.day, activityEvent.startTime FROM activityEvent JOIN activity ON activity.activityId = activityEvent.activityId WHERE activity.activityId=?", (activity_id,)).fetchall()
                activity_type = cursor.execute("SELECT name FROM activity WHERE activityId=?", (activity_id,)).fetchone()
                # Get the selected options from the form
                selected_facility = request.form['facility']
                selected_activity = request.form.get('activity')
                selected_event = request.form.get('event')

                # Get the userId based on the logged in user's email address
                email = session.get('email')
                selected_userId = cursor.execute("SELECT userId FROM users WHERE email=?", (email,)).fetchone()[0]
                
                # Get membership Id for storing once making a book
                if cursor.execute("SELECT memberType FROM users WHERE email=?", (email,)).fetchone()[0] is not None:
                    user_membership_type = cursor.execute("SELECT memberType FROM users WHERE email=?", (email,)).fetchone()[0]
                    membership_id = cursor.execute("SELECT membershipId FROM membership WHERE name=?", (user_membership_type,)).fetchone()[0]
                else:
                    membership_id = None

                # Check the capacity for the selected facility
                capacity = cursor.execute("SELECT capacity FROM facility WHERE facilityId=?", (selected_facility,)).fetchone()[0]
                # Check the current number of bookings for the selected facility and activity
                current_bookings = cursor.execute("SELECT COUNT(*) FROM bookings WHERE facilityId=? AND activityId=?", (selected_facility, selected_activity)).fetchone()[0]
                

                # Check if there is still room to create a new booking
                if current_bookings < capacity:
                    # Fetch the maximum bookingId from the database and increment it by 1 to create the new bookingId
                    max_booking_id = cursor.execute("SELECT MAX(bookingId) FROM bookings").fetchone()[0]
                    new_booking_id = max_booking_id + 1 if max_booking_id else 1

                    # Create a new booking with the provided options
                    cursor.execute("INSERT INTO bookings (bookingId, membershipid, facilityId, activityId, activityEventId, userId) VALUES (?,?, ?, ?, ?, ?)",
                            (new_booking_id, membership_id ,selected_facility, selected_activity, selected_event, selected_userId))
                    
                    # If activity type is general use, lane swimming, lessons, or 1-hour sessions, update the activityEventId to 0
                    if selected_activity and activity_type[0] in ['General use', 'Lane swimming', 'Lessons', '1-hour sessions']:
                        cursor.execute("UPDATE bookings SET activityEventId = 0 WHERE bookingId = ?", (new_booking_id,))
                        conn.commit()
                        return render_template('bookingpopup.html', loggedIn=loggedIn, firstName=firstName)
                    elif selected_event:
                        # Update the day, startTime, and endTime of the booking with the selected activityEvent
                        cursor.execute("UPDATE bookings SET activityEventId = ?, day = (SELECT day FROM activityEvent WHERE activityEventId = ?), startTime = (SELECT startTime FROM activityEvent WHERE activityEventId = ?), endTime = (SELECT endTime FROM activityEvent WHERE activityEventId = ?) WHERE bookingId = ?", (selected_event, selected_event, selected_event, selected_event, new_booking_id,))
                        conn.commit()
                        return redirect(url_for('main.booked'))
                else:
                    # alert messaging: a message to the user indicating that the capacity has been reached
                    message = "Sorry! Booking capacity for this activity has been full.  Please select another activity or time."
    
    conn.close()
    return render_template('booking.html',  message=message, facilities=facilities, activities=activities, events=events, loggedIn=loggedIn, firstName=firstName)


#by ayesha
@main.route('/bookingpopup', methods=['POST'])
def generaluseBooking():
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        # Get the userId based on the logged in user's email address
        email = session.get('email')
        user_id = cur.execute("SELECT userId FROM users WHERE email=?", (email,)).fetchone()[0]

        # Extract the form data
        date = request.form['date']
        time = request.form['time']

        # Retrieve the facility open and close time based on the selected date
        facility_id = 1 # Replace with the actual facility ID based on the booking
        facility_data = cur.execute("SELECT openTime, closeTime FROM facility WHERE facilityId=?", (facility_id,)).fetchone()
        open_time = datetime.strptime(facility_data[0], '%H:%M').time()
        close_time = datetime.strptime(facility_data[1], '%H:%M').time()

        # Check if the selected time is within the facility open and close time
        selected_time = datetime.strptime(time, '%H:%M').time()
        if selected_time < open_time or selected_time >= close_time:
            # Store the booking details in a session variable and redirect to the booking popup page
            session['booking_details'] = {'date': date, 'time': time}
            return redirect(url_for('main.booking_popup'))

        # Calculate end time
        end_time = (datetime.strptime(time, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')

        # Insert the new booking into the bookings table
        cur.execute("UPDATE bookings SET day=?, startTime=?, endTime=? WHERE bookingId=(SELECT MAX(bookingId) FROM bookings)", (date, time, end_time))
        conn.commit()

        # Redirect to booked.html page
        return redirect(url_for('main.booked'))

# by ayesha
@main.route('/bookingpopup')
def booking_popup():
    # Check if a booking is pending
    booking_details = session.get('booking_details')
    if booking_details:
        return render_template('bookingpopup.html', date=booking_details['date'], time=booking_details['time'])
    else:
        # Redirect to home page if no booking is pending
        return redirect(url_for('main.index'))


#done by sandra
#edited by ayesha
@main.route('/booked')
def booked():
    loggedIn, firstName = getLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        # Get the userId based on the logged in user's email address
        email = session.get('email')
        user_id = cur.execute("SELECT userId FROM users WHERE email=?", (email,)).fetchone()[0]

        # Fetch the user's bookings for facilities and activities
        cur.execute('''
        SELECT bookings.bookingId, facility.name, activity.name, bookings.day, bookings.startTime, bookings.endTime
        FROM bookings
        INNER JOIN facility ON facility.facilityId = bookings.facilityId
        INNER JOIN activity ON activity.activityId = bookings.activityId
        WHERE bookings.userId = ? 
        AND bookings.activityId IS NOT NULL 
        AND bookings.facilityId IS NOT NULL 
        AND bookings.activityEventId IS NOT NULL
        ''', (user_id,))
        
        bookings = cur.fetchall()
        bookings = parse(bookings)
        loggedIn, firstName = getLoginDetails()
        return render_template('booked.html', bookings=bookings, loggedIn=loggedIn, firstName=firstName)
    
# # ==================  delete bookings ===========================
#by sandra
@main.route('/<int:bookingId>/Deletebooking', methods=['POST'])
def Deletebooking(bookingId):
    if 'email' not in session:
        return render_template('loginForm.html')
    loggedIn, firstName = getLoginDetails()
    if request.method == "POST":
        with sqlite3.connect('app.db') as con:
            con.row_factory=sqlite3.Row

            cur = con.cursor()
            bookingId=int(bookingId)
            
            cur.execute('DELETE from bookings where bookingId =?', (bookingId,))
            con.commit() 
            # rows = cur.fetchone()
            return redirect("/booked")
    return render_template("booked.html", loggedIn=loggedIn, firstName=firstName)

#by ayesha
#display user list
@main.route('/userlist', methods=['GET', 'POST'])
def userlist():
    loggedIn, firstName = egetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        # Fetch all users
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        return render_template('userlist.html', users=users, loggedIn=loggedIn, firstName=firstName)

#by ayesha
# input email of user 
@main.route('/inputuser', methods=['GET', 'POST'])
def inputuser():
    loggedIn, firstName = egetLoginDetails()
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT userId FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['userId'] = user[0]  # Store userId in the session
            return redirect(url_for('main.userbookings', userId=user[0]))
        elif user:
            return redirect(url_for('main.eallowbooking', userId=user[0]))
        else:
            error = "Email not found."
            return render_template('inputuser.html', loggedIn=loggedIn, firstName=firstName, error=error)
    return render_template('inputuser.html', loggedIn=loggedIn, firstName=firstName)

#by ayesha
# views inputted user bookings - employee
@main.route('/userbookings', methods=['GET', 'POST'])
def userbookings():
    loggedIn, firstName = egetLoginDetails()
    if request.method == 'GET':
        userId = request.args.get('userId')
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        # cursor.execute("SELECT * FROM bookings WHERE userId=?", (userId,))
        cursor.execute('''
        SELECT bookings.bookingId, facility.name, activity.name, bookings.day, bookings.startTime, bookings.endTime
        FROM bookings
        INNER JOIN facility ON facility.facilityId = bookings.facilityId
        INNER JOIN activity ON activity.activityId = bookings.activityId
        WHERE bookings.userId = ? 
        AND bookings.activityId IS NOT NULL 
        AND bookings.facilityId IS NOT NULL 
        AND bookings.activityEventId IS NOT NULL
        ''', (userId,))
        bookings = cursor.fetchall()
        conn.close()
        return render_template('userbookings.html', loggedIn=loggedIn, firstName=firstName, bookings=bookings)
    else:
        return redirect(url_for('main.inputuser'))

# by sandra and ayesha, edited by geeyoon
#employee make booking for user 
@main.route('/eallowbooking', methods=['GET', 'POST'])
def eallowbooking():
    loggedIn, firstName = egetLoginDetails()
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    facilities = cursor.execute("SELECT facilityId, name FROM facility").fetchall()
    activities = []
    events = []
    message = None

    if request.method == 'POST':
        facility_id = request.form['facility']

        if facility_id is not None:
            activities = cursor.execute("SELECT activity.activityId, activity.name FROM activity JOIN facility ON activity.facilityId = facility.facilityId WHERE facility.facilityId = ?", (facility_id,)).fetchall()
            if request.form.get('activity'):
                activity_id = request.form['activity']
                events = cursor.execute("SELECT activityEvent.activityEventId, activityEvent.name, activityEvent.day, activityEvent.startTime FROM activityEvent JOIN activity ON activity.activityId = activityEvent.activityId WHERE activity.activityId=?", (activity_id,)).fetchall()
                activity_type = cursor.execute("SELECT name FROM activity WHERE activityId=?", (activity_id,)).fetchone()
                # Get the selected options from the form
                selected_facility = request.form['facility']
                selected_activity = request.form.get('activity')
                selected_event = request.form.get('event')

                # Get the userId based on the logged in user's email address
                email = session.get('email')
                selected_userId = session.get('userId')
                
                # Get membership Id for storing once making a book
                # if cursor.execute("SELECT memberType FROM users WHERE email=?", (email,)).fetchone()[0] is not None:
                #     user_membership_type = cursor.execute("SELECT memberType FROM users WHERE email=?", (email,)).fetchone()[0]
                #     membership_id = cursor.execute("SELECT membershipId FROM membership WHERE name=?", (user_membership_type,)).fetchone()[0]
                # else:
                membership_id = None

                # Check the capacity for the selected facility
                capacity = cursor.execute("SELECT capacity FROM facility WHERE facilityId=?", (selected_facility,)).fetchone()[0]
                # Check the current number of bookings for the selected facility and activity
                current_bookings = cursor.execute("SELECT COUNT(*) FROM bookings WHERE facilityId=? AND activityId=?", (selected_facility, selected_activity)).fetchone()[0]
                

                # Check if there is still room to create a new booking
                if current_bookings < capacity:
                    # Fetch the maximum bookingId from the database and increment it by 1 to create the new bookingId
                    max_booking_id = cursor.execute("SELECT MAX(bookingId) FROM bookings").fetchone()[0]
                    new_booking_id = max_booking_id + 1 if max_booking_id else 1

                    # Create a new booking with the provided options
                    cursor.execute("INSERT INTO bookings (bookingId, membershipid, facilityId, activityId, activityEventId, userId) VALUES (?,?, ?, ?, ?, ?)",
                            (new_booking_id, membership_id ,selected_facility, selected_activity, selected_event, selected_userId))
                    
                    # If activity type is general use, lane swimming, lessons, or 1-hour sessions, update the activityEventId to 0
                    if selected_activity and activity_type[0] in ['General use', 'Lane swimming', 'Lessons', '1-hour sessions']:
                        cursor.execute("UPDATE bookings SET activityEventId = 0 WHERE bookingId = ?", (new_booking_id,))
                        conn.commit()
                        return render_template('ebookingpopup.html', loggedIn=loggedIn, firstName=firstName)
                    elif selected_event:
                        # Update the day, startTime, and endTime of the booking with the selected activityEvent
                        cursor.execute("UPDATE bookings SET activityEventId = ?, day = (SELECT day FROM activityEvent WHERE activityEventId = ?), startTime = (SELECT startTime FROM activityEvent WHERE activityEventId = ?), endTime = (SELECT endTime FROM activityEvent WHERE activityEventId = ?) WHERE bookingId = ?", (selected_event, selected_event, selected_event, selected_event, new_booking_id,))
                        conn.commit()
                        return redirect(url_for('main.inputuser'))
                else:
                    # alert messaging: a message to the user indicating that the capacity has been reached
                    message = "Sorry! Booking capacity for this activity has been full.  Please select another activity or time."
    
    conn.close()
    return render_template('eallowbooking.html',  message=message, facilities=facilities, activities=activities, events=events, loggedIn=loggedIn, firstName=firstName) 


#by ayesha
@main.route('/ebookingpopup', methods=['POST'])
def ebookingpopup():
    loggedIn, firstName = egetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()

        # Get the userId based on the logged in user's email address
        email = session.get('email')
        user_id = request.args.get('userId')

        # Extract the form data
        date = request.form['date']
        time = request.form['time']

        # Retrieve the facility open and close time based on the selected date
        facility_id = 1 # Replace with the actual facility ID based on the booking
        facility_data = cur.execute("SELECT openTime, closeTime FROM facility WHERE facilityId=?", (facility_id,)).fetchone()
        open_time = datetime.strptime(facility_data[0], '%H:%M').time()
        close_time = datetime.strptime(facility_data[1], '%H:%M').time()

        # Check if the selected time is within the facility open and close time
        selected_time = datetime.strptime(time, '%H:%M').time()
        if selected_time < open_time or selected_time >= close_time:
            # Store the booking details in a session variable and redirect to the booking popup page
            session['booking_details'] = {'date': date, 'time': time}
            return redirect(url_for('main.booking_popup'))

        # Calculate end time
        end_time = (datetime.strptime(time, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')

        # Insert the new booking into the bookings table
        cur.execute("UPDATE bookings SET day=?, startTime=?, endTime=? WHERE bookingId=(SELECT MAX(bookingId) FROM bookings)", (date, time, end_time))
        conn.commit()

        # Redirect to booked.html page
        return redirect(url_for('main.inputuser'))

# by ayesha
@main.route('/ebookingpopup')
def ebooking_popup():
    # Check if a booking is pending
    booking_details = session.get('booking_details')
    if booking_details:
        return render_template('ebookingpopup.html', date=booking_details['date'], time=booking_details['time'])
    else:
        # Redirect to home page if no booking is pending
        return redirect(url_for('main.employeehome'))  

#by ayesha
@main.route("/search_result", methods=["POST"])
def Search():
    loggedIn, firstName = getLoginDetails()
    form = searchProd()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT 'facility' AS table_name, facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility WHERE name='{form.searched.data}' UNION ALL SELECT 'membership' AS table_name, membershipId, name, NULL, NULL, NULL, NULL, price FROM membership WHERE name='{form.searched.data}' UNION ALL SELECT 'activity' AS table_name, activityId, NULL, name, NULL, NULL, NULL, price FROM activity WHERE name='{form.searched.data}'")

        fsearchData = cur.fetchall()
        if len(fsearchData) == 0:
            return render_template('search.html', fsearchData='NO ITEM', itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
        return render_template('search.html', fsearchData=fsearchData, itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
      

#by ayesha, edited by Natalie
@main.route("/msearch_result", methods=["POST"])
def mSearch():
    loggedIn, firstName = mgetLoginDetails()
    form = searchProd()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT 'facility' AS table_name, facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility WHERE name='{form.searched.data}' UNION ALL SELECT 'membership' AS table_name, membershipId, name, NULL, NULL, NULL, NULL, price FROM membership WHERE name='{form.searched.data}' UNION ALL SELECT 'activity' AS table_name, activityId, NULL, name, NULL, NULL, NULL, price FROM activity WHERE name='{form.searched.data}'")

        fsearchData = cur.fetchall()
        if len(fsearchData) == 0:
            return render_template('msearch.html', fsearchData='NO ITEM', itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
        return render_template('msearch.html', fsearchData=fsearchData, itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
      
#employee - search 
#by ayesha, edited by Natalie
@main.route("/esearch_result", methods=["POST"])
def eSearch():
    loggedIn, firstName = egetLoginDetails()
    form = searchProd()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT 'facility' AS table_name, facilityId, name, roomCounter, description, capacity, openTime, closeTime FROM facility WHERE name='{form.searched.data}' UNION ALL SELECT 'membership' AS table_name, membershipId, name, NULL, NULL, NULL, NULL, price FROM membership WHERE name='{form.searched.data}' UNION ALL SELECT 'activity' AS table_name, activityId, NULL, name, NULL, NULL, NULL, price FROM activity WHERE name='{form.searched.data}'")

        fsearchData = cur.fetchall()
        if len(fsearchData) == 0:
            return render_template('esearch.html', fsearchData='NO ITEM', itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)
        return render_template('esearch.html', fsearchData=fsearchData, itemSear=form.searched.data, loggedIn=loggedIn, firstName=firstName)

#by Natalie
from datetime import datetime, timedelta
import calendar
from calendar import monthrange

def get_work_periods(start_date, end_date):
    """
    Returns a list of tuples representing work periods for the given date range,
    where each tuple contains the start and end time of a work period.
    """
    periods = []
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    while start_datetime <= end_datetime:
        first_day_of_month = datetime(start_datetime.year, start_datetime.month, 1)
        last_day_of_month = datetime(start_datetime.year, start_datetime.month, 1) + timedelta(days=32)
        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
        period_start = max(start_datetime, first_day_of_month)
        period_end = min(end_datetime, last_day_of_month)
        periods.append((period_start, period_end))
        start_datetime = datetime(start_datetime.year, start_datetime.month, 1) + timedelta(days=32)
    return periods

#by Natalie
@main.route('/etimetable', methods=['GET', 'POST'])
def etimetable():
    if 'email' not in session:
        return redirect(url_for('auth.root'))

    loggedIn, firstName = getLoginDetails()
    rows = []
    month = None
    if request.method == 'POST':
        month = request.form.get('start')
        if not month:
            error = 'Please select a month'
            return render_template('etimetable.html', loggedIn=loggedIn, firstName=firstName, error=error)
        else:
            month_start = datetime.strptime(month, '%Y-%m').date()
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)

        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM eusers WHERE email = ?", (session['email'],))
            staff_id = cur.fetchone()[0]
            cur.execute("SELECT date, startTime, endTime, position, facility FROM work WHERE staffId = ? AND date BETWEEN ? AND ?", (staff_id, month_start, month_end))
            data = cur.fetchall()

        for row in data:
            rows.append({
                'date': row[0],
                'start_time': datetime.strptime(row[1], '%Y-%m-%dT%H:%M').strftime('%H:%M'),
                'end_time': datetime.strptime(row[2], '%Y-%m-%dT%H:%M').strftime('%H:%M'),
                'position': row[3],
                'facility': row[4]
            })

        rows = sorted(rows, key=lambda row: datetime.strptime(row['date'] + ' ' + row['start_time'], '%Y-%m-%d %H:%M'))

    return render_template('etimetable.html', rows=rows, month=month, loggedIn=loggedIn, firstName=firstName, no_work=len(rows) == 0)



#by Natalie
@main.route('/epayslip', methods=['GET', 'POST'])
def epayslip():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    
    loggedIn, firstName = getLoginDetails()
    
    positionData = None 

    if request.method == 'POST':
        start_date = request.form['start']
        if not start_date:
            return render_template('epayslip.html', error='Please enter a date', loggedIn=loggedIn, firstName=firstName, positionData=positionData)
        
        start_date = request.form['start'] + "-01"
        year, month, _ = start_date.split('-')
        days_in_month = monthrange(int(year), int(month))[1]
        end_date = f"{year}-{month}-{days_in_month}"
    
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM eusers WHERE email = ?", (session['email'],))
            staff_id = cur.fetchone()[0]
            cur.execute("SELECT position, hourlyRate FROM work WHERE staffId = ?", (staff_id,))
            positionData = cur.fetchone()

            if positionData is not None:
                cur.execute("SELECT startTime, endTime FROM work WHERE staffId = ? AND startTime BETWEEN ? AND ?", (staff_id, start_date, end_date))
                work_periods = cur.fetchall()
                hours_worked = 0
                for start, end in work_periods:
                    start_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M")
                    end_datetime = datetime.strptime(end, "%Y-%m-%dT%H:%M")
                    hours_worked += (end_datetime - start_datetime).total_seconds() / 3600

                # Calculate the basic pay, tax, and total pay
                if positionData[1] is not None:
                    basic_pay = round(positionData[1] * hours_worked, 2)
                    tax = round(basic_pay * 0.2, 2)
                    total = round(basic_pay - tax, 2)
                else:
                    hours_worked, basic_pay, tax, total = 0, 0, 0, 0
            else:
                hours_worked, basic_pay, tax, total = 0, 0, 0, 0

        
        conn.close()
        
        return render_template("epayslip.html", loggedIn=loggedIn, firstName=firstName, positionData=positionData, start_date=start_date, end_date=end_date, hours_worked=hours_worked, basic_pay=basic_pay, tax=tax, total=total)
        
    return render_template("epayslip.html", loggedIn=loggedIn, firstName=firstName, positionData=positionData)

#by Natalie
@main.route('/eprofile')
def eprofile():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = egetLoginDetails()
    return render_template("eprofile.html", loggedIn=loggedIn, firstName=firstName)

#by Natalie
@main.route("/account/eprofile/edit")
def eeditProfile():
    if 'email' not in session:
        return redirect(url_for('auth.root'))
    loggedIn, firstName = egetLoginDetails()
    with sqlite3.connect('app.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone, position FROM eusers WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("e_editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)


#by Natalie
@main.route("/eupdateProfile", methods=["GET", "POST"])
def eupdateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        position = request.form['position']
        with sqlite3.connect('app.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE eusers SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ?, position = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, position, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('main.eeditProfile', msg=msg))
      
#by Natalie
@main.route("/account/eprofile/echangePassword", methods=["GET", "POST"])
def echangePassword():
    if 'email' not in session:
        return redirect(url_for('auth.loginForm'))
    loggedIn, firstName = egetLoginDetails()
    msg = None  # Initialize msg variable
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        # Enforce password requirements
        if not (re.search('[A-Z]', newPassword) and re.search('[^A-Za-z0-9]', newPassword) and len(newPassword) >= 8):
            msg = "Password must be at least 8 characters long, contain at least one capital letter, and at least one special character"
            return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        if oldPassword == newPassword:
            msg = "New password cannot be the same as the old password"
            return render_template("echangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM eusers WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE eusers SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("echangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("echangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
    else:
       return render_template("echangePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName)
      
#by Natalie
@main.route('/massignjob', methods=['GET', 'POST'])
def massignjob():
    if 'email' not in session:
        return redirect(url_for('main.login'))

    loggedIn, firstName = mgetLoginDetails()

    if request.method == 'POST':
        userId = request.form.get('user')
        facilityId = request.form.get('facility')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        hourly_rate = request.form.get('hourly_rate')

        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT firstName, lastName, position FROM eusers WHERE userId = ?", (userId,))
            user = cur.fetchone()
            cur.execute("SELECT name FROM facility WHERE facilityId = ?", (facilityId,))
            facility = cur.fetchone()
            cur.execute("INSERT INTO work (staffId, staffName, date, startTime, endTime, hourlyRate, facility, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (userId, user[0] + ' ' + user[1], date.today().strftime("%Y-%m-%d"), start_time, end_time, hourly_rate, facility[0], user[2]))
            conn.commit()

        flash('Job assigned successfully!', 'success')
        return redirect(url_for('main.massignjob'))

    try:
        with sqlite3.connect('app.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, firstName, lastName FROM eusers")
            users = cur.fetchall()
            cur.execute("SELECT facilityId, name FROM facility")
            facilities = cur.fetchall()
    except Exception as e:
        flash('Error fetching data from database: {}'.format(str(e)), 'danger')
        users = []
        facilities = []

    return render_template('massignjob.html', loggedIn=loggedIn, firstName=firstName, users=users, facilities=facilities)

###################Database########################
#this function updates the database contents
# @main.route('/')
# def createDbs():
#   with sqlite3.connect('app.db') as conn:
#         cur = conn.cursor()

#         cur.executemany("insert or replace into facility values (?,?,?,?,?,?,?)", facility_list)
#         cur.executemany("insert or replace into activity values (?,?,?,?)", activity_list)
#         cur.executemany("insert or replace into activityEvent values (?,?,?,?,?,?,?)", activityEvent_list)
#         cur.executemany("insert or replace into membership values (?,?,?)", membership_list)
#         conn.commit()
        
#         cur.execute("SELECT * FROM facility")
#         cur.execute("SELECT * FROM activity")
#         cur.execute("SELECT * FROM activityEvent")
#         cur.execute("SELECT * FROM membership")

#         loggedIn, firstName = getLoginDetails()
#         return render_template('index.html', loggedIn=loggedIn, firstName=firstName)

# facility_list = [
#   ("1", "Swimming pool", "1",  "General use, Lane swimming, Lessons, Team Events", "30", "08:00", "20:00"),
#   ("2", "Fitness room", "1",  "General use", "35", "08:00", "22:00"),
#   ("3", "Squash court", "2",  "1-hour sessions * (1)", "2", "08:00", "22:00"),
#   ("4", "Sports hall", "1",  "1-hour sessions, Team events", "45", "08:00", "22:00"),
#   ("5", "Climbing wall", "1",  "General use", "22", "10:00", "22:00"),
#   ("6", "Studio", "1",  "Classes: Pilates, Aerobics, Yoga", "25", "08:00", "22:00")
# ]

# activity_list = [
#   #swimming pool
#   ("1", "1", "General use", "15"),
#   ("2", "1", "Lane swimming", "15"),
#   ("3", "1", "Lessons", "15"),
#   ("4", "1", "Swimming Pool Team Events", "15"),
#   #fitness room
#   ("5", "2", "General use", "15"),
#   #squash court
#   ("6", "3", "1-hour sessions", "15"),
#   #sports hall
#   ("7", "4", "1-hour sessions", "15"),
#   ("8", "4", "Sports Hall Team Events", "15"),
#   #climbing wall
#   ("9", "5", "General use", "15"),
#   #studio
#   ("10", "6", "Exercise classes: Pilates", "15"),
#   ("11", "6", "Exercise classes: Aerobics", "15"),
#   ("12", "6", "Exercise classes: Yoga ", "15")
# ]

# activityEvent_list = [
#   #swimming pool
#   ("1", "4", "1", "Swimming Pool Team Events", "Friday", "08:00", "10:00"),
#   ("2", "4", "1", "Swimming Pool Team Events", "Sunday", "08:00", "10:00"),
#   #sports hall
#   ("3", "8", "4", "Sports Hall Team Events", "Tuesday", "19:00", "21:00"),
#   ("4", "8", "4", "Sports Hall Team Events", "Saturday", "09:00", "11:00"),

#   #studio pilates
#   ("5", "10", "6", "Pilates", "Monday", "18:00", "19:00"),
#   #studio aerobics
#   ("6", "11", "6", "Aerobics", "Tuesday", "10:00", "11:00"),
#   ("7", "11", "6", "Aerobics", "Thursday", "19:00", "20:00"),
#   ("8", "11", "6", "Aerobics", "Saturday", "10:00", "11:00"),
#   #studio yoga
#   ("9", "12", "6", "Yoga", "Friday", "19:00", "20:00"),
#   ("10", "12", "6", "Yoga", "Sunday", "09:00", "10:00")

# ]

# membership_list = [
#   ("1", "Monthly", "35"),
#   ("2", "Annual", "300")
  
# ]
###################Database########################

