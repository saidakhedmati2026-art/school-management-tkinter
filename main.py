import database
from app import SchoolApp

if __name__ == "__main__":
    
    database.init_db()

    print("Launching Desktop Application layout successfully...")
    app = SchoolApp()
    app.mainloop()  
