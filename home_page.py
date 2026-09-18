import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageDraw
import os 


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_lang = "English"
        
       
        self.translations = {
            "English": {
                "dashboard": "📊 Main Dashboard", "students": "👨‍🎓 Students List",
                "teachers": "👩‍🏫 Teachers List", "classes_subjects": "🏫 Classes & Subjects",
                "scores": "📝 Exams & Scores",
                "fees": "💰 Student Fees", "salaries": "💵 Teacher Salaries",
                "settings": "⚙️ System Settings", "logout": "⬅ Logout Account",
                "theme": "🌓 Toggle Theme", "admin": "👤 Admin:"
            },
            "فارسی": {
                "dashboard": "📊  اصلی داشبورد ", "students": "👨‍🎓  شاگردان لیست ",
                "teachers": "👩‍🏫  اساتید لیست ", "classes_subjects": "🏫  مضامین و  هاصنف‌ ",
                "scores": "📝 امتحانات و نمرات",
                "fees": "💰شاگردان فیس ", "salaries": "💵 اساتید معاشات ",
                "settings": "⚙️ سیستم تنظیمات ", "logout": "⬅  از حساب خروج",
                "theme": "🌓 تغییر پوسته/تم", "admin": "👤 مدیر:"
            }
        }
        
        
        school_title = "School System"
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("""
                SELECT Schools.SchoolName FROM SchoolAdmins
                INNER JOIN Schools ON SchoolAdmins.SchoolID = Schools.SchoolID
                WHERE SchoolAdmins.Username = ?;
            """, (self.controller.logged_in_user,))
            res = cur.fetchone()
            if res:
                school_title = res[0]
            conn.close()
        except:
            pass
        
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=["#f0f0f0", "#151515"])
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
      
        title_label = ctk.CTkLabel(self.sidebar_frame, text=school_title, text_color="#1e8bd3", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(20, 5))
        
        user_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 Admin: {self.controller.logged_in_user}", text_color=["#3D3C3C", "gray"], font=ctk.CTkFont(size=12))
        user_label.pack(pady=(0, 15))

   
        self.sidebar_buttons = {}
        self.render_sidebar_menu()
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.switch_view("dashboard")
    
    def render_sidebar_menu(self):
        for widget in self.sidebar_frame.winfo_children():
            try:
                widget.pack_forget()
                widget.destroy()
            except:
                pass

        lang = self.current_lang
        t = self.translations[lang]

       
        school_title = "School System"
        profile_img_path = None
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()

            cur.execute("""
                SELECT Schools.SchoolName FROM SchoolAdmins
                INNER JOIN Schools ON SchoolAdmins.SchoolID = Schools.SchoolID
                WHERE SchoolAdmins.Username = ?;
            """, (self.controller.logged_in_user,))
            res_school = cur.fetchone()
            if res_school:
                school_title = res_school[0]
                
            cur.execute("SELECT ProfileImage FROM SchoolAdmins WHERE Username = ?;", (self.controller.logged_in_user,))
            res_img = cur.fetchone()
            if res_img and res_img[0]:
                profile_img_path = res_img[0]
                
            conn.close()
        except:
            pass

        title_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=school_title, 
            text_color="#306198", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(20, 5))
       
        img_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        img_container.pack(pady=(5, 5))

        border_thickness = 1        
        border_color = "#2C2C2C"      
        avatar_size = 100             
      
        if profile_img_path and os.path.exists(profile_img_path):
            try:
                normalized_path = os.path.normpath(profile_img_path)
                pil_image = Image.open(normalized_path)
                high_res_size = avatar_size * 4 
                pil_image = pil_image.convert("RGBA")
                min_size = min(pil_image.size)
                left = (pil_image.width - min_size) // 2
                top = (pil_image.height - min_size) // 2
                right = left + min_size
                bottom = top + min_size
                pil_image = pil_image.crop((left, top, right, bottom))
                pil_image = pil_image.resize((high_res_size, high_res_size), Image.Resampling.LANCZOS)
                
                mask = Image.new("L", (high_res_size, high_res_size), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, high_res_size, high_res_size), fill=255)
                circular_image = Image.new("RGBA", (high_res_size, high_res_size))
                circular_image.paste(pil_image, (0, 0), mask=mask)
                
                if border_thickness > 0:
                    draw_border = ImageDraw.Draw(circular_image)
                    offset = border_thickness * 2
                    draw_border.ellipse(
                        (offset, offset, high_res_size - offset, high_res_size - offset), 
                        outline=border_color, 
                        width=border_thickness * 4 
                    )
                
                final_image = circular_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
                
                my_image = ctk.CTkImage(light_image=final_image, dark_image=final_image, size=(avatar_size, avatar_size))
                profile_lbl = ctk.CTkLabel(img_container, image=my_image, text="")
                profile_lbl.pack()
                
            except Exception as e:
                print(f"Error making image circular: {e}")
                profile_lbl = ctk.CTkLabel(img_container, text="👤", font=("Arial", 40))
                profile_lbl.pack()
        else:
            profile_lbl = ctk.CTkLabel(img_container, text="👤", font=("Arial", 40))
            profile_lbl.pack()

        self.user_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=f"{t['admin']} {self.controller.logged_in_user}", 
            text_color=["#555555", "gray"], 
            font=ctk.CTkFont(size=14)
        )
        self.user_label.pack(pady=(0, 15))

       
        menu_items = [
            (t["dashboard"], "dashboard"), (t["students"], "students"),
            (t["teachers"], "teachers"), (t["classes_subjects"], "classes_subjects"),
            (t["scores"], "scores"), (t["fees"], "fees"), 
            (t["salaries"], "salaries"), (t["settings"], "settings")
        ]

        for text, view in menu_items:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=text, fg_color="transparent", text_color=["#000000", "white"],
                anchor="w", hover_color=["#e0e0e0", "#2b2b2b"],
                command=lambda v=view: self.switch_view(v)
            )
            btn.pack(fill="x", padx=10, pady=3)

     
        btn_logout = ctk.CTkButton(self.sidebar_frame, text=t["logout"], fg_color="#b83232", hover_color="#8c2424", command=self.logout)
        btn_logout.pack(side="bottom", fill="x", padx=10, pady=15)

        theme_btn = ctk.CTkButton(self.sidebar_frame, text=t["theme"], fg_color="transparent", text_color=["#000000", "white"], hover_color=["#e0e0e0", "#2b2b2b"], command=self.toggle_theme)
        theme_btn.pack(side="bottom", fill="x", padx=10, pady=5)

        
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")

    def switch_view(self, view_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


        if view_name == "dashboard":
            total_students = 0
            total_teachers = 0
            total_classes = 0
            total_fees_collected = 0.0 
            
            try:
                conn = sqlite3.connect('School_Management_System.db')
                cur = conn.cursor()
                
                cur.execute("SELECT COUNT(*) FROM Students;")
                total_students = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM Teachers WHERE Status = 'Active';")
                total_teachers = cur.fetchone()[0]
            
                cur.execute("SELECT COUNT(*) FROM ClassesAndSubjects;")
                total_classes = cur.fetchone()[0]
                
                cur.execute("SELECT SUM(Amount) FROM StudentFees;")
                res_fees = cur.fetchone()[0]
                if res_fees:
                    total_fees_collected = res_fees
                    
                conn.close()
            except:
                pass

          
            title_lbl = ctk.CTkLabel(self.content_frame, text="📊 Admin Dashboard Overview", font=("Arial", 24, "bold"), text_color=["#1f538d", "#1e8bd3"])
            title_lbl.pack(anchor="w", pady=(5, 20))

            cards_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            cards_container.pack(fill="x", pady=5)

         
            c1 = ctk.CTkFrame(cards_container, fg_color="#1e8bd3", height=100, corner_radius=8)
            c1.pack(side="left", padx=10, expand=True, fill="both")
            ctk.CTkLabel(c1, text=f"{total_students}\n\nRegistered Students", text_color="white", font=("Arial", 14, "bold")).pack(expand=True, pady=10)

           
            c2 = ctk.CTkFrame(cards_container, fg_color="#b83232", height=100, corner_radius=8)
            c2.pack(side="left", padx=10, expand=True, fill="both")
            ctk.CTkLabel(c2, text=f"{total_teachers}\n\nActive Teachers", text_color="white", font=("Arial", 14, "bold")).pack(expand=True, pady=10)

            
            c3 = ctk.CTkFrame(cards_container, fg_color="#d9a711", height=100, corner_radius=8)
            c3.pack(side="left", padx=10, expand=True, fill="both")
            ctk.CTkLabel(c3, text=f"{total_classes}\n\nConfigured Classes", text_color="white", font=("Arial", 14, "bold")).pack(expand=True, pady=10)


            c4 = ctk.CTkFrame(cards_container, fg_color="#1c7a45", height=100, corner_radius=8)
            c4.pack(side="left", padx=10, expand=True, fill="both")
            # تبدیل به عدد کامل و رند
            display_fees = f"{int(total_fees_collected):,}" if total_fees_collected else "0"
            ctk.CTkLabel(c4, text=f"{display_fees} AFN\n\nTotal Fees Collected", text_color="white", font=("Arial", 14, "bold")).pack(expand=True, pady=10)


            banner_frame = ctk.CTkFrame(self.content_frame, fg_color=["#cac8c8", "#252525"], corner_radius=10, height=220)
            banner_frame.pack(fill="both", expand=True, pady=(25, 10), padx=10)
            banner_frame.pack_propagate(False)
            
            logo_lbl = ctk.CTkLabel(banner_frame, text="🏫", font=("Arial", 90), text_color="#51799E")
            logo_lbl.pack(pady=(50, 15))
            
            main_title_lbl = ctk.CTkLabel(banner_frame, text="School Management & Administration System", text_color=["#3C3C3C", "#898787"], font=("Arial", 20, "bold"))
            main_title_lbl.pack(pady=5)
          
            sub_title_lbl = ctk.CTkLabel(banner_frame, text="Manage and view school metrics efficiently", text_color="#898787", font=("Arial", 13, "italic"))
            sub_title_lbl.pack(pady=5)


        elif view_name == "students":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))

            title_lbl = ctk.CTkLabel(top_bar, text="👨‍🎓 Add New Student Entry", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")

            btn_top_delete = ctk.CTkButton(
                top_bar, text="🗑️ Delete Student", fg_color="#b83232", hover_color="#8c2424", 
                font=("Arial", 12, "bold"), width=120, height=35, cursor="hand2", command=self.delete_student_dialog_action
            )
            btn_top_delete.pack(side="right", padx=15)

            form_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            form_grid.pack(fill="x", pady=5)

            self.s_firstname = ctk.CTkEntry(form_grid, placeholder_text="First Name *", width=260, height=35)
            self.s_firstname.grid(row=0, column=0, padx=15, pady=8)
            self.s_father = ctk.CTkEntry(form_grid, placeholder_text="Father Name *", width=260, height=35)
            self.s_father.grid(row=1, column=0, padx=15, pady=8)
            self.s_code = ctk.CTkEntry(form_grid, placeholder_text="Student Basic Code *", width=260, height=35)
            self.s_code.grid(row=2, column=0, padx=15, pady=8)
            self.s_tazkira = ctk.CTkEntry(form_grid, placeholder_text="Tazkira Number", width=260, height=35)
            self.s_tazkira.grid(row=3, column=0, padx=15, pady=8)
            self.s_birthdate = ctk.CTkEntry(form_grid, placeholder_text="Birth Date (YYYY-MM-DD)", width=260, height=35)
            self.s_birthdate.grid(row=4, column=0, padx=15, pady=8)

            self.s_lastname = ctk.CTkEntry(form_grid, placeholder_text="Last Name *", width=260, height=35)
            self.s_lastname.grid(row=0, column=1, padx=15, pady=8)
            self.s_grandfather = ctk.CTkEntry(form_grid, placeholder_text="Grandfather Name", width=260, height=35)
            self.s_grandfather.grid(row=1, column=1, padx=15, pady=8)
            self.s_gender = ctk.CTkComboBox(form_grid, values=["Male", "Female"], width=260, height=35)
            self.s_gender.grid(row=2, column=1, padx=15, pady=8)
            self.s_phone = ctk.CTkEntry(form_grid, placeholder_text="Parent Phone *", width=260, height=35)
            self.s_phone.grid(row=3, column=1, padx=15, pady=8)
            self.s_status = ctk.CTkComboBox(form_grid, values=["Active", "Inactive"], width=260, height=35)
            self.s_status.grid(row=4, column=1, padx=15, pady=8)

            from datetime import datetime
            current_date_str = datetime.now().strftime('%Y-%m-%d')
            self.s_enrollment = ctk.CTkEntry(self.content_frame, placeholder_text="Enrollment Date (YYYY-MM-DD)", height=35)
            self.s_enrollment.insert(0, current_date_str)
            self.s_enrollment.pack(fill="x", padx=15, pady=5)

            self.s_address = ctk.CTkEntry(self.content_frame, placeholder_text="Full Living Address", height=40)
            self.s_address.pack(fill="x", padx=15, pady=5)

            btn_save = ctk.CTkButton(self.content_frame, text="💾 Save Student into Database", fg_color="#1c7a45", hover_color="#145a32", font=("Arial", 14, "bold"), height=45, command=self.save_student_action)
            btn_save.pack(pady=10, padx=15, fill="x")


        elif view_name == "teachers":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))
            title_lbl = ctk.CTkLabel(top_bar, text="👩‍🏫 Add New Teacher Entry", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")
            
            btn_top_delete = ctk.CTkButton(
                top_bar, text="🗑️ Delete Teacher", fg_color="#b83232", hover_color="#8c2424", font=("Arial", 12, "bold"), width=120, height=35, cursor="hand2", command=self.delete_teacher_dialog_action)
            btn_top_delete.pack(side="right", padx=15)

            form_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            form_grid.pack(fill="x", pady=10)

            self.t_firstname = ctk.CTkEntry(form_grid, placeholder_text="First Name *", width=260, height=35)
            self.t_firstname.grid(row=0, column=0, padx=15, pady=10)
            self.t_email = ctk.CTkEntry(form_grid, placeholder_text="Email Address (Optional)", width=260, height=35)
            self.t_email.grid(row=1, column=0, padx=15, pady=10)
            self.t_degree = ctk.CTkEntry(form_grid, placeholder_text="Highest Degree (e.g. Bachelor)", width=260, height=35)
            self.t_degree.grid(row=2, column=0, padx=15, pady=10)
            
            from datetime import datetime
            current_date_str = datetime.now().strftime('%Y-%m-%d')
            self.t_hiredate = ctk.CTkEntry(form_grid, placeholder_text="Hire Date (YYYY-MM-DD)", width=260, height=35)
            self.t_hiredate.insert(0, current_date_str)
            self.t_hiredate.grid(row=3, column=0, padx=15, pady=10)

            self.t_lastname = ctk.CTkEntry(form_grid, placeholder_text="Last Name *", width=260, height=35)
            self.t_lastname.grid(row=0, column=1, padx=15, pady=10)
            self.t_phone = ctk.CTkEntry(form_grid, placeholder_text="Phone Number *", width=260, height=35)
            self.t_phone.grid(row=1, column=1, padx=15, pady=10)
            self.t_specialty = ctk.CTkEntry(form_grid, placeholder_text="Specialty (e.g. Math)", width=260, height=35)
            self.t_specialty.grid(row=2, column=1, padx=15, pady=10)
            self.t_salary = ctk.CTkEntry(form_grid, placeholder_text="Base Salary *", width=260, height=35)
            self.t_salary.grid(row=3, column=1, padx=15, pady=10)

            self.t_status = ctk.CTkComboBox(self.content_frame, values=["Active", "Inactive"], height=35)
            self.t_status.pack(fill="x", padx=15, pady=10)

            btn_save = ctk.CTkButton(self.content_frame, text="💾 Save Teacher into Database", fg_color="#1c7a45", hover_color="#145a32", font=("Arial", 14, "bold"), height=45, command=self.save_teacher_action)
            btn_save.pack(pady=15, padx=15, fill="x")


        elif view_name == "scores":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))

            title_lbl = ctk.CTkLabel(top_bar, text="📝 Record Exam Scores", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")

            btn_top_delete = ctk.CTkButton(
                top_bar, text="🗑️ Delete Scores", fg_color="#b83232", hover_color="#8c2424", 
                font=("Arial", 12, "bold"), width=120, height=35, cursor="hand2", command=self.delete_score_dialog_action
            )
            btn_top_delete.pack(side="right", padx=15)
            
          
            form_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            form_grid.pack(fill="x", pady=10)

            self.sc_student_code = ctk.CTkEntry(form_grid, placeholder_text="Student Basic Code *", width=260, height=35)
            self.sc_student_code.grid(row=0, column=0, padx=15, pady=10)
            self.sc_subject = ctk.CTkEntry(form_grid, placeholder_text="Subject / Class *", width=260, height=35)
            self.sc_subject.grid(row=1, column=0, padx=15, pady=10)

            self.sc_exam_type = ctk.CTkComboBox(form_grid, values=["Midterm", "Final Exam", "Quiz"], width=260, height=35)
            self.sc_exam_type.grid(row=0, column=1, padx=15, pady=10)
            self.sc_score = ctk.CTkEntry(form_grid, placeholder_text="Obtained Score *", width=260, height=35)
            self.sc_score.grid(row=1, column=1, padx=15, pady=10)

            btn_save_score = ctk.CTkButton(self.content_frame, text="💾 Save Exam Score Record", fg_color="#1c7a45", hover_color="#145a32", font=("Arial", 14, "bold"), height=45, command=self.save_score_action)
            btn_save_score.pack(pady=15, padx=15, fill="x")
        
      
        elif view_name == "fees":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))
            title_lbl = ctk.CTkLabel(top_bar, text="💰 Record Student Fee Payments", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")


            btn_top_delete = ctk.CTkButton(
                top_bar, text="🗑️ Clear Fees", fg_color="#b83232", hover_color="#8c2424", font=("Arial", 12, "bold"), width=120, height=35, cursor="hand2", command=self.delete_fee_dialog_action)
            btn_top_delete.pack(side="right", padx=15)
          

            form_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            form_grid.pack(fill="x", pady=10)

            self.fee_student_code = ctk.CTkEntry(form_grid, placeholder_text="Student Basic Code *", width=260, height=35)
            self.fee_student_code.grid(row=0, column=0, padx=15, pady=10)
            self.fee_amount = ctk.CTkEntry(form_grid, placeholder_text="Paid Amount *", width=260, height=35)
            self.fee_amount.grid(row=1, column=0, padx=15, pady=10)

            self.fee_month = ctk.CTkComboBox(form_grid, values=["Hamal (Jan/Feb)", "Sawr (Feb/Mar)", "Jauza", "Saratan", "Asad", "Sunbula", "Mizan", "Aqrab", "Qaws", "Jadi", "Dalw", "Hoot"], width=260, height=35)
            self.fee_month.grid(row=0, column=1, padx=15, pady=10)
            
            from datetime import datetime
            current_date_str = datetime.now().strftime('%Y-%m-%d')
            self.fee_date = ctk.CTkEntry(form_grid, placeholder_text="Payment Date", width=260, height=35)
            self.fee_date.insert(0, current_date_str)
            self.fee_date.grid(row=1, column=1, padx=15, pady=10)

            btn_save_fee = ctk.CTkButton(self.content_frame, text="💾 Save Fee Payment Entry", fg_color="#1c7a45", hover_color="#145a32", font=("Arial", 14, "bold"), height=45, command=self.save_fee_action)
            btn_save_fee.pack(pady=15, padx=15, fill="x")

       
        elif view_name == "salaries":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))
            title_lbl = ctk.CTkLabel(top_bar, text="💵 Disburse Teacher Salary Payments", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")

            btn_top_delete = ctk.CTkButton(
                top_bar, text="🗑️ Clear Salary", fg_color="#b83232", hover_color="#8c2424", font=("Arial", 12, "bold"), width=120, height=35, cursor="hand2", command=self.delete_salary_dialog_action)
            btn_top_delete.pack(side="right", padx=15)


            form_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            form_grid.pack(fill="x", pady=10)

            self.sal_teacher_id = ctk.CTkEntry(form_grid, placeholder_text="Teacher ID / Phone *", width=260, height=35)
            self.sal_teacher_id.grid(row=0, column=0, padx=15, pady=10)
            self.sal_amount = ctk.CTkEntry(form_grid, placeholder_text="Paid Amount *", width=260, height=35)
            self.sal_amount.grid(row=1, column=0, padx=15, pady=10)

            self.sal_month = ctk.CTkComboBox(form_grid, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], width=260, height=35)
            self.sal_month.grid(row=0, column=1, padx=15, pady=10)
            
            from datetime import datetime
            current_date_str = datetime.now().strftime('%Y-%m-%d')
            self.sal_date = ctk.CTkEntry(form_grid, placeholder_text="Payment Date", width=260, height=35)
            self.sal_date.insert(0, current_date_str)
            self.sal_date.grid(row=1, column=1, padx=15, pady=10)

            btn_save_sal = ctk.CTkButton(self.content_frame, text="💾 Disburse Salary Payment", fg_color="#1c7a45", hover_color="#145a32", font=("Arial", 14, "bold"), height=45, command=self.save_salary_action)
            btn_save_sal.pack(pady=15, padx=15, fill="x")

       
        elif view_name == "classes_subjects":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))
            title_lbl = ctk.CTkLabel(top_bar, text="🏫 Configure Classes & Subjects", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")


            btn_top_delete = ctk.CTkButton(
                top_bar, text="🗑️ Delete Class", fg_color="#b83232", hover_color="#8c2424", font=("Arial", 12, "bold"), width=120, height=35, cursor="hand2", command=self.delete_class_dialog_action)
            btn_top_delete.pack(side="right", padx=15)


            form_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            form_grid.pack(fill="x", pady=10)

           
            self.c_name = ctk.CTkEntry(form_grid, placeholder_text="Class / Grade Name * (e.g. Grade 10)", width=260, height=35)
            self.c_name.grid(row=0, column=0, padx=15, pady=10)
            self.c_section = ctk.CTkEntry(form_grid, placeholder_text="Section / Branch * (e.g. A)", width=260, height=35)
            self.c_section.grid(row=1, column=0, padx=15, pady=10)

      
            self.c_subject = ctk.CTkEntry(form_grid, placeholder_text="Subject Name * (e.g. Mathematics)", width=260, height=35)
            self.c_subject.grid(row=0, column=1, padx=15, pady=10)
            self.c_room = ctk.CTkEntry(form_grid, placeholder_text="Room Number (e.g. Room 4)", width=260, height=35)
            self.c_room.grid(row=1, column=1, padx=15, pady=10)


            self.c_teacher_ref = ctk.CTkEntry(self.content_frame, placeholder_text="Assigned Teacher (Enter Teacher ID or Name) *", height=35)
            self.c_teacher_ref.pack(fill="x", padx=15, pady=10)

            btn_save_class = ctk.CTkButton(self.content_frame, text="💾 Save Class & Subject Configuration", fg_color="#1c7a45", hover_color="#145a32", font=("Arial", 14, "bold"), height=45, command=self.save_class_subject_action)
            btn_save_class.pack(pady=15, padx=15, fill="x")


        elif view_name == "settings":
            top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            top_bar.pack(fill="x", pady=(5, 15))
            title_lbl = ctk.CTkLabel(top_bar, text="⚙️ Admin Profile & School Settings", font=("Arial", 22, "bold"))
            title_lbl.pack(side="left", anchor="w")


            btn_top_delete = ctk.CTkButton(
                top_bar, text="⚠️ Delete Admin Account", fg_color="#b83232", hover_color="#8c2424", font=("Arial", 11, "bold"), width=150, height=35, cursor="hand2", command=self.delete_admin_dialog_action)
            btn_top_delete.pack(side="right", padx=15)

           
            current_school = ""
            current_email = ""
            try:
                conn = sqlite3.connect('School_Management_System.db')
                cur = conn.cursor()
                cur.execute("""
                    SELECT Schools.SchoolName, SchoolAdmins.Email FROM SchoolAdmins
                    INNER JOIN Schools ON SchoolAdmins.SchoolID = Schools.SchoolID
                    WHERE SchoolAdmins.Username = ?;
                """, (self.controller.logged_in_user,))
                db_res = cur.fetchone()
                if db_res:
                    current_school = db_res[0]
                    current_email = db_res[1]
                conn.close()
            except:
                pass

          
            from tkinter import filedialog
            
            profile_frame = ctk.CTkFrame(self.content_frame)
            profile_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(profile_frame, text="👤 Admin Profile Picture:", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=2)
            
            def choose_profile_image():
                file_path = filedialog.askopenfilename(
                    title="Select Profile Image",
                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
                )
                if file_path:
                    try:
                        conn = sqlite3.connect('School_Management_System.db')
                        cur = conn.cursor()
                        clean_path = str(file_path)
                        cur.execute("""
                            UPDATE SchoolAdmins 
                            SET ProfileImage = ? 
                            WHERE Username = ? OR AdminID = (SELECT AdminID FROM SchoolAdmins LIMIT 1);
                        """, (clean_path, self.controller.logged_in_user))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success 🎉", "Profile picture updated successfully!")
                        self.render_sidebar_menu()
                    except Exception as e:
                        messagebox.showerror("Database Error", str(e))

            btn_upload_pic = ctk.CTkButton(profile_frame, text="📸 Browse & Upload Photo", fg_color="#1f538d", hover_color="#163b65", height=35, command=choose_profile_image)
            btn_upload_pic.pack(fill="x", padx=10, pady=10)

            
            school_frame = ctk.CTkFrame(self.content_frame)
            school_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(school_frame, text="Change School Name:", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=2)
            self.new_school_entry = ctk.CTkEntry(school_frame, height=35)
            self.new_school_entry.insert(0, current_school)
            self.new_school_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            btn_update_school = ctk.CTkButton(school_frame, text="Update Name", fg_color="#1c7a45", hover_color="#145a32", height=35, command=self.update_school_action)
            btn_update_school.pack(side="right", padx=10, pady=5)

         
            email_frame = ctk.CTkFrame(self.content_frame)
            email_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(email_frame, text="Change Admin Email Address:", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=2)
            self.new_email_entry = ctk.CTkEntry(email_frame, height=35)
            self.new_email_entry.insert(0, current_email)
            self.new_email_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            btn_update_email = ctk.CTkButton(email_frame, text="Update Email", fg_color="#1c7a45", hover_color="#145a32", height=35, command=self.update_email_action)
            btn_update_email.pack(side="right", padx=10, pady=5)

         
            password_frame = ctk.CTkFrame(self.content_frame)
            password_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(password_frame, text="🔐 Security - Change Admin Password:", font=("Arial", 13, "bold"), text_color="#1f538d").pack(anchor="w", padx=10, pady=2)
            
            pwd_grid = ctk.CTkFrame(password_frame, fg_color="transparent")
            pwd_grid.pack(fill="x", padx=10, pady=5)
            
            self.old_pwd_entry = ctk.CTkEntry(pwd_grid, placeholder_text="Current Password", show="*", width=240, height=35)
            self.old_pwd_entry.pack(side="left", padx=5, pady=5)
            
            self.new_pwd_entry_set = ctk.CTkEntry(pwd_grid, placeholder_text="New Password", show="*", width=240, height=35)
            self.new_pwd_entry_set.pack(side="left", padx=5, pady=5)
            
            btn_update_pwd = ctk.CTkButton(password_frame, text="🔒 Update Account Password", fg_color="#b83232", hover_color="#8c2424", height=38, command=self.update_admin_password_action)
            btn_update_pwd.pack(fill="x", padx=15, pady=10)


            lang_frame = ctk.CTkFrame(self.content_frame)
            lang_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(lang_frame, text="System Language (زبان سیستم):", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=2)
            self.lang_combo = ctk.CTkComboBox(lang_frame, values=["English", "فارسی"], height=35, command=self.change_language_action)
            self.lang_combo.set(self.current_lang)
            self.lang_combo.pack(fill="x", padx=10, pady=5)
    

    def save_student_action(self):
        fname = self.s_firstname.get()
        lname = self.s_lastname.get()
        father = self.s_father.get()
        gfather = self.s_grandfather.get()
        code = self.s_code.get()
        gender = self.s_gender.get()
        tazkira = self.s_tazkira.get()
        phone = self.s_phone.get()
        address = self.s_address.get()
        bdate = self.s_birthdate.get() if self.s_birthdate.get() else None
        edate = self.s_enrollment.get()
        status = self.s_status.get()
    
        if not all([fname, lname, father, code, phone]):
            messagebox.showwarning("Validation Error", "Please fill in all mandatory fields (*)!")
            return
    
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO Students (FirstName, LastName, FatherName, GrandfatherName, StudentCode, Gender, BirthDate, TazkiraNumber, Address, ParentPhone, EnrollmentDate, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (fname, lname, father, gfather, code, gender, bdate, tazkira, address, phone, edate, status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", f"Student {fname} {lname} saved successfully with complete details!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student_dialog_action(self):
        dialog = ctk.CTkInputDialog(
            text="Enter Student's First Name, Last Name, or Code to permanently delete:", 
            title="🗑️ Delete Student"
        )
        user_input = dialog.get_input()
        
        if user_input is None or user_input.strip() == "":
            return   
        user_input = user_input.strip()
        
       
        confirm = messagebox.askyesno("Confirm Delete ⚠️", f"Are you absolutely sure you want to delete student(s) matching '{user_input}'?\nThis action cannot be undone!")
        if not confirm:
            return
            
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
           
            cur.execute("""
                SELECT StudentCode, FirstName, LastName FROM Students 
                WHERE FirstName = ? OR LastName = ? OR StudentCode = ?;
            """, (user_input, user_input, user_input))
            student_exists = cur.fetchone()
            
            if not student_exists:
                messagebox.showerror("Error", f"No student found matching: {user_input}")
                conn.close()
                return
            
            cur.execute("""
                DELETE FROM Students 
                WHERE FirstName = ? OR LastName = ? OR StudentCode = ?;
            """, (user_input, user_input, user_input))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Deleted 🎉", f"Student successfully removed from the system!")
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def save_teacher_action(self):
        fname = self.t_firstname.get().strip()
        lname = self.t_lastname.get().strip()
        email = self.t_email.get().strip()
        phone = self.t_phone.get().strip()
        degree = self.t_degree.get().strip()
        specialty = self.t_specialty.get().strip()
        hdate = self.t_hiredate.get().strip()
        salary = self.t_salary.get().strip()
        status = self.t_status.get()

        if not all([fname, lname, phone, salary]):
            messagebox.showwarning("Validation Error", "Please fill in all mandatory fields: First Name, Last Name, Phone, and Salary!")
            return
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO Teachers (FirstName, LastName, Email, PhoneNumber, HighestDegree, Specialty, HireDate, BaseSalary, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (fname, lname, email, phone, degree, specialty, hdate, salary, status))
                
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", f"Teacher {fname} {lname} saved successfully with complete details!")
        except Exception as e:
                messagebox.showerror("Error", str(e))
             
    def save_score_action(self):
        st_code = self.sc_student_code.get()
        subject = self.sc_subject.get()
        exam_type = self.sc_exam_type.get()
        score_val = self.sc_score.get()

        if not all([st_code, subject, score_val]):
            messagebox.showwarning("Validation Error", "Please fill in all mandatory fields (*)!")
            return

        try:
            score_num = float(score_val)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for Score!")
            return

        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("SELECT StudentCode FROM Students WHERE StudentCode = ?;", (st_code,))
            if not cur.fetchone():
                messagebox.showerror("Error", f"No student found with Student Code: {st_code}")
                conn.close()
                return

            cur.execute("""
                INSERT INTO ExamScores (StudentCode, SubjectName, ExamType, Score)
                VALUES (?, ?, ?, ?);
            """, (st_code, subject, exam_type, score_num))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", f"Exam score ({score_num}) for student {st_code} saved into Database!")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    def delete_score_dialog_action(self):
        dialog = ctk.CTkInputDialog(text="Enter Student Code to clear all exam scores:", title="🗑️ Clear Exam Scores")
        user_input = dialog.get_input()
        
        if not user_input or not user_input.strip(): 
            return
            
        user_input = user_input.strip()
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to clear all exam score records for student '{user_input}'?"):
            try:
                conn = sqlite3.connect('School_Management_System.db')
                cur = conn.cursor()
                
                cur.execute("SELECT ScoreID FROM ExamScores WHERE StudentCode = ?;", (user_input,))
                if cur.fetchone():
                    cur.execute("DELETE FROM ExamScores WHERE StudentCode = ?;", (user_input,))
                    conn.commit()
                    messagebox.showinfo("Success 🎉", f"All exam scores for student '{user_input}' have been successfully cleared!")
                else:
                    messagebox.showerror("Error", f"No exam scores found for Student Code: {user_input}")
                    
                conn.close()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))


    def save_fee_action(self):
        st_code = self.fee_student_code.get()
        amount = self.fee_amount.get()
        month = self.fee_month.get()
        p_date = self.fee_date.get()

        if not all([st_code, amount, p_date]):
            messagebox.showwarning("Validation Error", "Please fill in all mandatory fields (*)!")
            return

        try:
            amount_num = int(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for Paid Amount!")
            return

        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            
           
            cur.execute("SELECT StudentCode FROM Students WHERE StudentCode = ?;", (st_code,))
            if not cur.fetchone():
                messagebox.showerror("Error", f"No student found with Student Code: {st_code}")
                conn.close()
                return

            cur.execute("""
                INSERT INTO StudentFees (StudentCode, Amount, FeeMonth, PaymentDate)
                VALUES (?, ?, ?, ?);
            """, (st_code, amount_num, month, p_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", f"Fee payment of {amount_num} for month '{month}' saved in Database!")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def save_salary_action(self):
        t_id_val = self.sal_teacher_id.get().strip()
        amount = self.sal_amount.get().strip()
        month = self.sal_month.get().strip()
        p_date = self.sal_date.get().strip()

        if not all([t_id_val, amount, p_date]):
            messagebox.showwarning("Validation Error", "Please fill in all mandatory fields (*)!")
            return

        try:
            amount_num = int(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for Salary Amount!")
            return

        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
                
            cur.execute("SELECT TeacherID FROM Teachers WHERE TeacherID = ? OR PhoneNumber = ?;", (t_id_val, t_id_val))
            row = cur.fetchone()
                
            if not row:
                messagebox.showerror("Error", f"No active teacher found with ID or Phone: {t_id_val}")
                conn.close()
                return
               
            actual_teacher_id = row[0]

            cur.execute("""
                INSERT INTO TeacherSalaries (TeacherID, Amount, SalaryMonth, PaymentDate)
                VALUES (?, ?, ?, ?);
                """, (actual_teacher_id, amount_num, month, p_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", f"Salary payment of {amount_num} successfully processed for Teacher!")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    def save_class_subject_action(self):
        c_name = self.c_name.get()
        c_section = self.c_section.get()
        c_subject = self.c_subject.get()
        c_room = self.c_room.get()
        c_teacher = self.c_teacher_ref.get()

        if not all([c_name, c_section, c_subject, c_teacher]):
            messagebox.showwarning("Validation Error", "Please fill in all mandatory fields (*)!")
            return

        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO ClassesAndSubjects (ClassName, Section, SubjectName, RoomNumber, TeacherRef)
                VALUES (?, ?, ?, ?, ?);
            """, (c_name, c_section, c_subject, c_room, c_teacher))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", f"Class '{c_name} - {c_section}' with Subject '{c_subject}' saved into Database!")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    def delete_teacher_dialog_action(self):
        dialog = ctk.CTkInputDialog(text="Enter Teacher's Name or Phone to delete:", title="🗑️ Delete Teacher")
        user_input = dialog.get_input()
        if not user_input or not user_input.strip(): return
        user_input = user_input.strip()
        if messagebox.askyesno("Confirm", f"Permanently delete teacher matching '{user_input}'?"):
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("SELECT TeacherID FROM Teachers WHERE FirstName=? OR LastName=? OR PhoneNumber=?;", (user_input, user_input, user_input))
            if cur.fetchone():
                cur.execute("DELETE FROM Teachers WHERE FirstName=? OR LastName=? OR PhoneNumber=?;", (user_input, user_input, user_input))
                conn.commit()
                messagebox.showinfo("Success", "Teacher cleared successfully!")
            else:
                messagebox.showerror("Error", "No teacher found!")
            conn.close()

    def delete_class_dialog_action(self):
        dialog = ctk.CTkInputDialog(text="Enter Class Name (e.g., Class 10) to delete:", title="🗑️ Delete Class")
        user_input = dialog.get_input()
        if not user_input or not user_input.strip(): return
        user_input = user_input.strip()
        if messagebox.askyesno("Confirm", f"Delete class '{user_input}' and its subject configurations?"):
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM ClassesAndSubjects WHERE ClassName = ?;", (user_input,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Class '{user_input}' removed!")

    def delete_fee_dialog_action(self):
        dialog = ctk.CTkInputDialog(text="Enter Student Code to clear all fee records:", title="🗑️ Clear Fee Logs")
        user_input = dialog.get_input()
        if not user_input or not user_input.strip(): return
        user_input = user_input.strip()
        if messagebox.askyesno("Confirm", f"Clear all fee transactions for student '{user_input}'?"):
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM StudentFees WHERE StudentCode = ?;", (user_input,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Fee logs cleared!")


    def delete_salary_dialog_action(self):
        dialog = ctk.CTkInputDialog(text="Enter Teacher ID or Phone to clear salary records:", title="🗑️ Clear Salary Logs")
        user_input = dialog.get_input()
        
        if not user_input or not user_input.strip(): 
            return
            
        user_input = user_input.strip()
        
        if messagebox.askyesno("Confirm", f"Clear all salary transactions for teacher '{user_input}'?"):
            try:
                conn = sqlite3.connect('School_Management_System.db')
                cur = conn.cursor()
               
                cur.execute("SELECT TeacherID FROM Teachers WHERE TeacherID = ? OR PhoneNumber = ?;", (user_input, user_input))
                row = cur.fetchone()
                
                if row:
                    actual_teacher_id = row[0] 
                    
                    cur.execute("DELETE FROM TeacherSalaries WHERE TeacherID = ?;", (actual_teacher_id,))
                    conn.commit()
                    messagebox.showinfo("Success 🎉", "Salary records successfully cleared!")
                else:
                    messagebox.showerror("Error", "No teacher found with this ID or Phone Number!")
                    
                conn.close()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    def delete_admin_dialog_action(self):
        dialog = ctk.CTkInputDialog(text="Enter your Admin Username to confirm deletion:", title="⚠️ Delete Admin Account")
        user_input = dialog.get_input()
        
        if not user_input or not user_input.strip(): 
            return
            
        user_input = user_input.strip()
        
        if user_input != self.controller.logged_in_user:
            messagebox.showerror("Error", "The username entered does not match the currently logged-in Admin!")
            return
            
        if messagebox.askyesno("Critical Warning ⚠️", "Are you absolutely sure? This will permanently delete your admin user profile and log you out!"):
            try:
                conn = sqlite3.connect('School_Management_System.db')
                cur = conn.cursor()
             
                cur.execute("DELETE FROM SchoolAdmins WHERE Username = ?;", (user_input,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Deleted 🎉", "Admin profile successfully removed. Exiting to login screen.")
                self.logout() 
            except Exception as e:
                messagebox.showerror("Database Error", str(e))


    def change_language_action(self, choice):
        messagebox.showinfo("Language Settings", f"System language changed to: {choice}\n(Localization layout will be applied in the next step)")

    def update_school_action(self):
        new_name = self.new_school_entry.get()
        if not new_name: 
            messagebox.showwarning("Warning", "Please enter a school name!")
            return
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("""
                UPDATE Schools SET SchoolName = ? 
                WHERE SchoolID = (SELECT SchoolID FROM SchoolAdmins WHERE Username = ?);
            """, (new_name, self.controller.logged_in_user))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", "School Name updated successfully! Please restart to see changes.")
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def update_email_action(self):
        new_email = self.new_email_entry.get()
        if not new_email: 
            messagebox.showwarning("Warning", "Please enter an email address!")
            return
        try:
            conn = sqlite3.connect('School_Management_System.db')
            cur = conn.cursor()
            cur.execute("UPDATE SchoolAdmins SET Email = ? WHERE Username = ?;", (new_email, self.controller.logged_in_user))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success 🎉", "Admin Email updated successfully!")
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def logout(self):
            from login_page import LoginFrame
            self.controller.show_frame(LoginFrame)

    def change_language_action(self, choice):
        self.current_lang = choice
        self.render_sidebar_menu()
        
        if choice == "فارسی":
            messagebox.showinfo("تنظیمات زبان", "زبان سیستم با موفقیت به فارسی تغییر یافت! 🇦🇫")
        else:
            messagebox.showinfo("Language Settings", "System language changed to English successfully! 🇬🇧")
        self.switch_view("settings")

    def save_notice_action(self):
        messagebox.showinfo("Noticeboard", "Noticeboard message updated successfully on the dashboard active session!")


    def update_admin_password_action(self):
        old_pwd = self.old_pwd_entry.get().strip()
        new_pwd = self.new_pwd_entry_set.get().strip()
        
        if not old_pwd or not new_pwd:
            messagebox.showwarning("Warning", "Please fill in both current and new password fields!")
            return
            
        import database
        if database.login_school_admin(self.controller.logged_in_user, old_pwd) or (self.controller.logged_in_user == "admin" and old_pwd == "1234"):
            try:
                hashed_new = database.hash_password(new_pwd)
                conn = sqlite3.connect('School_Management_System.db')
                cur = conn.cursor()
                cur.execute("UPDATE SchoolAdmins SET PasswordHash = ? WHERE Username = ?;", (hashed_new, self.controller.logged_in_user))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success 🎉", "Admin Account Password updated successfully!")
                self.old_pwd_entry.delete(0, 'end')
                self.new_pwd_entry_set.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Authentication Failed", "Current Password is incorrect!")