import customtkinter as ctk
from PIL import Image
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# فرض می‌کنیم آیکون‌ها داخل پوشه‌ای به نام icons در کنار کدهایتان هستند
ICONS_DIR = os.path.join(CURRENT_PATH, "icons") 

class AppIcons:
    # لود کردن آیکون‌ها فقط برای یک‌بار
    USER = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS_DIR, "user.png")), size=(20, 20))
    LOCK = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS_DIR, "lock.png")), size=(20, 20))
    LOGIN = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS_DIR, "login.png")), size=(18, 18))
    HOME = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS_DIR, "home.png")), size=(16, 16))
    