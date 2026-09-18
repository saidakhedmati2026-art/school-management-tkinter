import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="transparent")

        # برای مدریت دکمه چشم ساخته شده به طور پیش فرض پسورد که کدیر اضافه میکند دیده نمی شود تا زمانی که آیکن چشم را بذند و پسورد دیده میشود.
        self.show_pwd = False

        card_frame = ctk.CTkFrame(self, corner_radius=10, border_width=1, border_color=["#dbdbdb", "#2e2e2e"])
        card_frame.pack(pady=40, padx=20, expand=True)
                    
        header_frame = ctk.CTkFrame(card_frame, fg_color=["#2d2d2d", "#151515"], corner_radius=0, height=50, width=360)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
                    
        header_label = ctk.CTkLabel(header_frame, text="Admin Login", text_color="white", font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(side="left", padx=20, pady=10) 
            
        theme_btn = ctk.CTkButton(header_frame, text="🌓", fg_color="transparent", 
        text_color="white", hover_color=["#404040", "#2b2b2b"],
        command=self.toggle_theme, width=40, height=30, corner_radius=5)
        theme_btn.pack(side="right", padx=10, pady=10)

        form_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        form_frame.pack(pady=15, padx=30, fill="both", expand=True)
                    
        username_label = ctk.CTkLabel(form_frame, text="Username", font=ctk.CTkFont(size=14))
        username_label.pack(anchor="w", pady=(10, 5))
                    
        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter username", height=35, width=280)
        self.username_entry.pack(pady=(0, 15))
                    
        password_label = ctk.CTkLabel(form_frame, text="Password", font=ctk.CTkFont(size=14))
        password_label.pack(anchor="w", pady=(0, 5))
       
        pwd_border_frame = ctk.CTkFrame(form_frame, height=35, width=280, corner_radius=8, border_width=1, border_color=["#979797", "#565b5e"], fg_color=["#f9f9f9", "#343638"])
        pwd_border_frame.pack(pady=(0, 15))
        pwd_border_frame.pack_propagate(False)
        
        self.password_entry = ctk.CTkEntry(pwd_border_frame, placeholder_text="Enter password", show="*", border_width=0, fg_color="transparent", bg_color="transparent")
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        self.eye_btn = ctk.CTkButton(pwd_border_frame, text="👁️", width=30, fg_color="transparent", hover_color=["#e0e0e0", "#444444"], text_color=["black", "white"], font=("Arial", 14), command=self.toggle_password_visibility)
        self.eye_btn.pack(side="right", padx=(0, 2))
                    
        login_btn = ctk.CTkButton(form_frame, text="Login", fg_color="#1c7a45", hover_color="#145a32", 
        font=ctk.CTkFont(size=14, weight="bold"), height=35, width=280, command=self.check_login)
        login_btn.pack(pady=10)

        forgot_btn = ctk.CTkButton(form_frame, text="Forgot Password?", fg_color="transparent",
        text_color=["#b83232", "#fc4444"], font=ctk.CTkFont(size=12, slant="roman"),
        command=self.forgot_password_action)
        forgot_btn.pack(pady=2)
       
        from register_page import RegisterFrame
        signup_btn = ctk.CTkButton(form_frame, text="Don't have an account? Register Here", fg_color="transparent",
        text_color=["#256fc4", "#256fc4"], command=lambda: self.controller.show_frame(RegisterFrame))
        signup_btn.pack(pady=5)
        
    def toggle_password_visibility(self):
        if self.show_pwd:
            self.password_entry.configure(show="*")
            self.eye_btn.configure(text="👁️")
            self.show_pwd = False
        else:
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="🔒")
            self.show_pwd = True

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        import database
        if database.login_school_admin(username, password):
            messagebox.showinfo("Success", "Welcome to School Management System!")
            self.controller.logged_in_user = username
            from home_page import HomeFrame
            self.controller.show_frame(HomeFrame)
        else:
            messagebox.showerror("Error", "Invalid credentials or account not verified!")


    def forgot_password_action(self):
        import sqlite3
        import random
        from datetime import datetime, timedelta
        import database 

        email_dialog = ctk.CTkInputDialog(text="Enter your registered Admin Email Address:", title="🔑 Forgot Password")
        email_input = email_dialog.get_input()
        
        if not email_input or not email_input.strip():
            return
        email_input = email_input.strip()

        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
        
            cur.execute("SELECT Username FROM SchoolAdmins WHERE Email = ?;", (email_input,))
            admin_exists = cur.fetchone()
            
            if not admin_exists:
                messagebox.showerror("Error", "No Admin found with this Email Address!")
                conn.close()
                return
            
            username = admin_exists[0]
            otp_code = str(random.randint(100000, 999999))
            expire_time = (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
            
            cur.execute("""
                INSERT INTO EmailVerification (Email, Code, ExpireTime)
                VALUES (?, ?, ?);
            """, (email_input, otp_code, expire_time))
            conn.commit()
            conn.close()
           
            messagebox.showinfo("Sending...", "Sending verification code to your email. Please wait...")
            email_sent = database.send_otp_automatically(email_input, otp_code)
            
            if not email_sent:
                messagebox.showerror("Error", "Failed to send email. Please check your network or EMAIL_PASS environment variable!")
                return
                
            code_dialog = ctk.CTkInputDialog(text="Enter the 6-digit code sent to your email:", title="🛡️ Verification Required")
            code_input = code_dialog.get_input()
            
            if not code_input or not code_input.strip():
                return
            code_input = code_input.strip()
            
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            current_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cur.execute("""
                SELECT VerificationID FROM EmailVerification 
                WHERE Email = ? AND Code = ? AND ExpireTime > ?;
            """, (email_input, code_input, current_str))
            
            otp_valid = cur.fetchone()
            
            if not otp_valid:
                messagebox.showerror("Error", "Invalid or expired verification code!")
                conn.close()
                return
           
            pass_dialog = ctk.CTkInputDialog(text="Verification Successful! Enter your new Password:", title="🔒 Reset Password")
            new_pass = pass_dialog.get_input()
            
            if not new_pass or not new_pass.strip():
                messagebox.showwarning("Warning", "Password cannot be empty!")
                conn.close()
                return
         
            hashed_pw = database.hash_password(new_pass.strip())
            cur.execute("UPDATE SchoolAdmins SET PasswordHash = ? WHERE Username = ?;", (hashed_pw, username))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success 🎉", "Your password has been successfully reset! You can now log in.")
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))