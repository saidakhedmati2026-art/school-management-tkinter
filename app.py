import customtkinter as ctk
from login_page import LoginFrame

class SchoolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("School Management System")
        
        window_width = 1100
        window_height = 650

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(900, 550)

        # متغیر سراسری نگهداری نام کاربری ادمین فعال
        self.logged_in_user = "admin"

        self.current_frame = None
        self.show_frame(LoginFrame)
        
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy() 
        self.current_frame = frame_class(self, self)
        self.current_frame.pack(fill="both", expand=True)
    