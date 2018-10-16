import sqlite3

conn = sqlite3.connect('demo3.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS DEMO3
         (STUDENT_ID INT NOT NULL,
         STUDENT_NETID TEXT NOT NULL,
         STUDENT_NAME TEXT NOT NULL,
         
         COURSE_ID TEXT NOT NULL,
         COURSE_NAME TEXT NOT NULL,

         EXAM_TYPE TEXT NOT NULL,
         EXAM_FORMAT TEXT NOT NULL,
         EXAM_TIME TEXT NOT NULL,
         EXAM_CSD_TIME TEXT NOT NULL,

         CSD_CAMPUS TEXT NOT NULL,
         CSD_BUILDING TEXT NOT NULL,
         CSD_ROOM TEXT NOT NULL,
         CSD_SEAT TEXT NOT NULL,

         INSTRUCTOR_NETID TEXT NOT NULL,
         INSTRUCTOR_NAME TEXT NOT NULL,
         INSTRUCTOR_PHONE TEXT,
         INSTRUCTOR_EMAIL TEXT,

         MATERIAL TEXT,
         ACCOMMODATIONS TEXT NOT NULL,
         INSTRUCTOR_NOTES TEXT);''')
print ("Table created successfully")

conn.commit()

conn.close()