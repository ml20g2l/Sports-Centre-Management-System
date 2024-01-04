# from app import db

# db.create_all()

import sqlite3

#Open database
conn = sqlite3.connect('app.db')
cursor=conn.cursor

#Create table users
#by ayesha
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		zipcode TEXT,
		city TEXT,
		state TEXT,
		country TEXT, 
		phone TEXT,
                memberType TEXT,
                status BOOLEAN NOY NULL CHECK (status IN (0,1))
		)''')

# status BOOLEAN NULL CHECK (status IN (0,1))
# db for facilities 
# we will need a foregin key to connect with activity
# by Sandra
conn.execute('''CREATE TABLE facility
        (facilityId INTEGER PRIMARY KEY,
         name TEXT,
         roomCounter INTEGER,
         description TEXT,
         capacity INTEGER,
         openTime TIME,
         closeTime TIME
        )''')


#by ayesha, edited by Natalie        
conn.execute('''CREATE TABLE activity
        (activityId INTEGER PRIMARY KEY,
        facilityId INTEGER,
        name TEXT,
        price REAL,
	FOREIGN KEY (facilityId) REFERENCES facility(facilityId) ON DELETE CASCADE
        )''')

# conn.execute('''UPDATE activity SET s = (SELECT facility.name FROM facility INNER JOIN 
#  activity ON facility.facilityId = activity.facilityId
#         )''')

  




#by sandra       
conn.execute('''CREATE TABLE activityEvent
        (activityEventId INTEGER PRIMARY KEY,
        activityId INTEGER,
        facilityId INTEGER,
        name TEXT,
        day DATETIME,
        startTime TIME,
        endTime TIME,
        FOREIGN KEY(facilityId) REFERENCES facility(facilityId),
        FOREIGN KEY(activityId) REFERENCES activity(activityId)
        )''')

#by ayesha        
conn.execute('''CREATE TABLE membership
        (membershipId INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
        )''')

#by ayesha
conn.execute('''CREATE TABLE bookings
        (
        bookingId INTEGER PRIMARY KEY,
        userId INTEGER,
        membershipId INTEGER,
        activityId INTEGER,
        facilityId INTEGER,
        activityEventId INTEGER,
        day DATETIME,
        startTime TIME,
        endTime TIME,
         buyClass INTEGER,
	FOREIGN KEY(userId) REFERENCES users(userId),
	FOREIGN KEY(membershipId) REFERENCES membership(membershipId),
        FOREIGN KEY(activityId) REFERENCES activity(activityId),
        FOREIGN KEY(facilityId) REFERENCES facility(facilityId),
        FOREIGN KEY(activityEventId) REFERENCES activityEvent(activityEventId)
	)''')

#manager table
conn.execute('''CREATE TABLE IF NOT EXISTS musers 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		zipcode TEXT,
		city TEXT,
		state TEXT,
		country TEXT, 
		phone TEXT
		)''')

#employee table
#by geeyoon ,edited by Natalie
conn.execute('''CREATE TABLE IF NOT EXISTS eusers
        (userId INTEGER PRIMARY KEY,
        password TEXT,
        email TEXT,
        firstName TEXT,
        lastName TEXT,
        address1 TEXT,
        address2 TEXT,
        zipcode TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        phone TEXT,
        position TEXT
        )''')


# #Add positions to eusers table
# conn.execute('''ALTER TABLE eusers ADD COLUMN position TEXT''')

# # Update positions for existing users
# conn.execute('''UPDATE eusers SET position = "receptionist" WHERE userId = 1''')
# conn.execute('''UPDATE eusers SET position = "instructor" WHERE userId = 2''')
# conn.execute('''UPDATE eusers SET position = "cleaner" WHERE userId = 3''')
# conn.execute('''UPDATE eusers SET position = "lifeguard" WHERE userId = 4''')



# Create a table to store the work details
#by Natalie
conn.execute('''CREATE TABLE IF NOT EXISTS work
                    (userId INTEGER PRIMARY KEY,
                    staffId INTEGER,
                    staffName TEXT,
                    date TEXT,
                    startTime TEXT,
                    endTime TEXT,
                    hourlyRate INTEGER,
                    facility TEXT,
                    position TEXT,
                    FOREIGN KEY(staffId) REFERENCES eusers(userId),
                    FOREIGN KEY(position) REFERENCES eusers(position)
                    )''')


conn.close()

