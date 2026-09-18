""" CRUD  >>>  I am able to creat diferent tabls here """
import smtplib    
import sqlite3
import bcrypt
import random
import os 
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

"""اتصال پایدار به دیتابیس"""
def get_db_connection():
    return sqlite3.connect('School_Management_System.db')

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
   
    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS Schools (
        SchoolID INTEGER PRIMARY KEY AUTOINCREMENT,
        SchoolName TEXT NOT NULL,
        Location TEXT,
        Phone TEXT
    );""")


    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS SchoolAdmins (
        AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
        SchoolID INTEGER,
        Username TEXT NOT NULL UNIQUE,
        Email TEXT NOT NULL UNIQUE,
        PasswordHash TEXT NOT NULL,
        IsVerified INTEGER DEFAULT 0,
        ProfileImage TEXT,  -- ستون جدید برای ذخیره آدرس عکس پروفایل
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (SchoolID) REFERENCES Schools(SchoolID) ON DELETE CASCADE
    );""")


    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS EmailVerification (
        VerificationID INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT NOT NULL,
        Code TEXT NOT NULL,     
        ExpireTime TIMESTAMP NOT NULL              
    );""")

   
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        FatherName TEXT NOT NULL,
        GrandfatherName TEXT,
        StudentCode TEXT UNIQUE,         
        Gender TEXT,
        BirthDate DATE,
        TazkiraNumber TEXT,             
        Address TEXT,
        ParentPhone TEXT NOT NULL,
        EnrollmentDate DATE DEFAULT CURRENT_DATE, 
        Status TEXT DEFAULT 'Active'     
    );""")

   
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        TeacherID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT UNIQUE,                              
        PhoneNumber TEXT NOT NULL,
        HighestDegree TEXT,              
        Specialty TEXT,                  
        HireDate DATE DEFAULT CURRENT_DATE, 
        BaseSalary REAL,                 
        Status TEXT DEFAULT 'Active'     
    );""")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS ExamScores (
        ScoreID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentCode TEXT NOT NULL,
        SubjectName TEXT NOT NULL,
        ExamType TEXT NOT NULL,
        Score REAL NOT NULL,
        ExamDate DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (StudentCode) REFERENCES Students(StudentCode) ON DELETE CASCADE
    );""")

    
   
    cur.execute("""
    CREATE TABLE IF NOT EXISTS StudentFees (
        FeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentCode TEXT NOT NULL,
        Amount REAL NOT NULL,
        FeeMonth TEXT NOT NULL,
        PaymentDate DATE NOT NULL,
        FOREIGN KEY (StudentCode) REFERENCES Students(StudentCode) ON DELETE CASCADE
    );""")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS TeacherSalaries (
        SalaryID INTEGER PRIMARY KEY AUTOINCREMENT,
        TeacherID INTEGER NOT NULL,
        Amount REAL NOT NULL,
        SalaryMonth TEXT NOT NULL,
        PaymentDate DATE NOT NULL,
        FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID) ON DELETE CASCADE
    );""")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS ClassesAndSubjects (
        ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
        ClassName TEXT NOT NULL,
        Section TEXT NOT NULL,
        SubjectName TEXT NOT NULL,
        RoomNumber TEXT,
        TeacherRef TEXT NOT NULL
    );""")

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def send_otp_automatically(receiver_email: str, otp_code: str) -> bool:
    sender_email = "sofiasoufizada2003@gmail.com"  
    sender_password = os.getenv('EMAIL_PASS', "sofiasoufizada2003@gmail.com") 

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your Registration Verification Code"
    
    body = f"Your Registration Verification Code: {otp_code}\nThis Code is valid for 2 minutes."
    message.attach(MIMEText(body, "plain", "utf-8"))
    
    try:
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error in automatic email delivery: {e}")
        return False

def register_step1_send_code(school_name: str, username: str, email: str, password: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Schools (SchoolName) VALUES (?);", (school_name,))
        school_id = cur.lastrowid
        
        hashed_pw = hash_password(password)
        
        cur.execute("""
            INSERT INTO SchoolAdmins (SchoolID, Username, Email, PasswordHash, IsVerified)
            VALUES (?, ?, ?, ?, 0);
        """, (school_id, username, email, hashed_pw))
        
        otp_code = str(random.randint(100000, 999999))
        expire_time = (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
        
        cur.execute("""
            INSERT INTO EmailVerification (Email, Code, ExpireTime)
            VALUES (?, ?, ?);
        """, (email, otp_code, expire_time))
        
        conn.commit()
        send_otp_automatically(email, otp_code)
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_school_admin(username, raw_password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT PasswordHash FROM SchoolAdmins WHERE Username = ? AND IsVerified = 1;", (username,))
    result = cur.fetchone()
    conn.close()

    
    if result:
        hashed_password_in_db = result[0] 
        if check_password(raw_password, hashed_password_in_db):
            return True   
    return False