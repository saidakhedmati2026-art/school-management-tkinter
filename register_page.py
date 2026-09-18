import customtkinter as ctk
from tkinter import messagebox
import database

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="transparent")
        
        self.user_email = ""
        self.show_pwd = False

        self.form_container = ctk.CTkFrame(self, corner_radius=10, border_width=1, border_color=["#dbdbdb", "#2e2e2e"])
        self.form_container.pack(pady=40, padx=20, expand=True)

        self.header_frame = ctk.CTkFrame(self.form_container, fg_color=["#2d2d2d", "#151515"], corner_radius=0, height=50, width=360)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
                    
        self.header_label = ctk.CTkLabel(self.header_frame, text="Principal Register", text_color="white", font=ctk.CTkFont(size=15, weight="bold"))
        self.header_label.pack(side="left", padx=15, pady=10)
            
        theme_btn = ctk.CTkButton(self.header_frame, text="🌓", fg_color="transparent", 
        text_color="white", hover_color=["#404040", "#2b2b2b"],
        command=self.toggle_theme, width=40, height=30, corner_radius=5)
        theme_btn.pack(side="right", padx=10, pady=10)

        self.dynamic_body = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.dynamic_body.pack(pady=10, padx=20, fill="both", expand=True)

        self.load_step1_interface()
        
    def toggle_password_visibility(self):
        if self.show_pwd:
            self.password_input.configure(show="*")
            self.eye_btn.configure(text="👁️")
            self.show_pwd = False
        else:
            self.password_input.configure(show="")
            self.eye_btn.configure(text="🔒")
            self.show_pwd = True

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")

    def load_step1_interface(self):
        for widget in self.dynamic_body.winfo_children():
            widget.destroy()
        
        self.school_input = ctk.CTkEntry(self.dynamic_body, width=280, placeholder_text="School name", justify="center", height=35)
        self.school_input.pack(pady=8)
        
        self.email_input = ctk.CTkEntry(self.dynamic_body, width=280, placeholder_text="Email Address", justify="center", height=35)
        self.email_input.pack(pady=8)
        
        self.username_input = ctk.CTkEntry(self.dynamic_body, width=280, placeholder_text="Username", justify="center", height=35)
        self.username_input.pack(pady=8)
        
        reg_pwd_border = ctk.CTkFrame(self.dynamic_body, height=35, width=280, corner_radius=8, border_width=1, border_color=["#979797", "#565b5e"], fg_color=["#f9f9f9", "#343638"])
        reg_pwd_border.pack(pady=8)
        reg_pwd_border.pack_propagate(False)
        
        self.password_input = ctk.CTkEntry(reg_pwd_border, placeholder_text="Password", show="*", border_width=0, fg_color="transparent", bg_color="transparent", justify="center")
        self.password_input.pack(side="left", fill="both", expand=True, padx=(30, 0)) # جهت تعادل متن وسط‌چین
        
        self.eye_btn = ctk.CTkButton(reg_pwd_border, text="👁️", width=30, fg_color="transparent", hover_color=["#e0e0e0", "#444444"], text_color=["black", "white"], font=("Arial", 14), command=self.toggle_password_visibility)
        self.eye_btn.pack(side="right", padx=(0, 2))
      
        btn_register = ctk.CTkButton(self.dynamic_body, text="Send Verification Code", width=280, height=35, fg_color="#1c7a45", hover_color="#145a32", cursor="hand2", command=self.send_code_action)
        btn_register.pack(pady=(15, 5))
        
        from login_page import LoginFrame
        btn_back = ctk.CTkButton(self.dynamic_body, text="Back to Login", fg_color="transparent", text_color=["#256fc4", "#256fc4"], cursor="hand2", command=lambda: self.controller.show_frame(LoginFrame))
        btn_back.pack(pady=(0, 10))

    def send_code_action(self):
        school = self.school_input.get()
        email = self.email_input.get()
        user = self.username_input.get()
        password = self.password_input.get()
        
        if not all([school, email, user, password]):
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return
            
        self.user_email = email
        if database.register_step1_send_code(school, user, email, password):
            messagebox.showinfo("Email Sent", f"A 6-digit OTP code has been successfully sent to {email}.\nPlease check your inbox.")
            self.load_step2_interface()
        else:
            messagebox.showerror("Registration Failed", "Username or Email already exists in the system!")

    def load_step2_interface(self):
        for widget in self.dynamic_body.winfo_children():
            widget.destroy()
        
        info_lbl = ctk.CTkLabel(self.dynamic_body, text=f"Enter the 6-digit code sent to:\n{self.user_email}", font=("Arial", 12), text_color="gray")
        info_lbl.pack(pady=10)
        
        self.otp_input = ctk.CTkEntry(self.dynamic_body, width=200, placeholder_text="X X X X X X", justify="center", font=("Arial", 18, "bold"), height=40)
        self.otp_input.pack(pady=10)
        
        btn_verify = ctk.CTkButton(self.dynamic_body, text="Verify & Activate Account", width=280, height=35, fg_color="#1c7a45", hover_color="#056d32", cursor="hand2", command=self.verify_code_action)
        btn_verify.pack(pady=(15, 5))
        
        btn_cancel = ctk.CTkButton(self.dynamic_body, text="Cancel & Restart", fg_color="transparent", text_color="gray", cursor="hand2", command=self.load_step1_interface)
        btn_cancel.pack(pady=(0, 10))

    def verify_code_action(self):
        entered_code = self.otp_input.get()
        if not entered_code:
            messagebox.showwarning("Error", "Please enter the verification code!")
            return
            
        import sqlite3
        from datetime import datetime
        
        conn = database.get_db_connection()
        cur = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cur.execute("""
            SELECT Code FROM EmailVerification 
            WHERE Email = ? AND ExpireTime > ? 
            ORDER BY VerificationID DESC LIMIT 1;
        """, (self.user_email, current_time))
        
        result = cur.fetchone()
        
        if result and result[0] == entered_code:
            cur.execute("UPDATE SchoolAdmins SET IsVerified = 1 WHERE Email = ?;", (self.user_email,))
            cur.execute("DELETE FROM EmailVerification WHERE Email = ?;", (self.user_email,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success 🎉", "Your account has been verified successfully!\nYou can now log in.")
            from login_page import LoginFrame
            self.controller.show_frame(LoginFrame)
        else:
            conn.close()
            messagebox.showerror("Verification Failed", "Invalid code or the 2-minute expiration time has passed!")


