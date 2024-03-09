import customtkinter
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image

from repo import download_release
from interface import Progress
from threading import Thread
import os 
from files import dir_path

class ProgressFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=35)
        self.grid_rowconfigure(2, weight=1)
        self.downloading_label = customtkinter.CTkLabel(self, text='Downloading build...') 
        self.downloading_label.grid(row=0, column = 0, sticky='nw', padx=10, pady=4)
        self.progress_bar = customtkinter.CTkProgressBar(master=self)
        self.progress_bar.grid(row=1, column=0, sticky='wen', padx=10)
        self.progress_bar.set(0)
        
    def step_download(self, current):
        self.progress_bar.set(current)

    def download_complete(self):
        self.downloading_label.configure(text='Download Complete!')
        self.close_button = customtkinter.CTkButton(self, text='Close', command=self.winfo_toplevel().close_window, width=90)
        self.close_button.grid(row=1, column=0, sticky='se', padx=7, pady=7)

class DirectoryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master ,fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=30)
        #self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=5)
        
        self.directory_prompt_label = customtkinter.CTkLabel(self, text='Save to:')
        self.directory_prompt_label.grid(row=0, column = 0, sticky='w', padx=4, pady=4)
        
        self.directory_text = tkinter.StringVar(self, dir_path,  'directory_text')
        self.directory_box = customtkinter.CTkEntry(self, placeholder_text=dir_path,  textvariable=self.directory_text, width=230)
        self.directory_box.grid(row=0, column = 1, sticky='wn', padx=4, pady=4) 
        
        self.select_directory_button = customtkinter.CTkButton(self, text='Browse', command=self.select_directory, width=80)
        self.select_directory_button.grid(row=0, column=1, sticky='e', padx=7 )


    def select_directory(self):
        self.directory_text.set(filedialog.askdirectory())

    def get_directory(self):
        return self.directory_text.get()
        

class SelectDirectoryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=25)
        self.grid_rowconfigure(1, weight=2)
        
        #self.title_label = customtkinter.CTkLabel(self, text='Ikemen-GO Build Downloader')
        #self.title_label.grid(row=0, column = 0, sticky='enw', padx=1)

        self.directory_frame = DirectoryFrame(self)
        self.directory_frame.grid(row=0, column = 0, sticky='nwe') 
                
        self.next_button = customtkinter.CTkButton(self, text='Download', command = master.init_download, width=50)
        self.next_button.grid(row=1,column=0,  sticky='se', pady=7, padx=7)

    def get_directory_from_frame(self):
        return self.directory_frame.get_directory()

class UtilFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.select_directory_frame = SelectDirectoryFrame(self)
        self.select_directory_frame.grid(row=0, column=0, sticky='news', padx=5, pady=5)
        self.progress_bar_frame = None  

    def init_download(self):
        directory = self.select_directory_frame.get_directory_from_frame()
        if not os.path.isdir(directory):
            messagebox.showerror("Invalid Directory", "Please enter a valid directory.") 
            return 

        self.select_directory_frame.grid_remove()
        self.progress_bar_frame = ProgressFrame(self)
        self.progress_bar_frame.grid(row=0, column=0, sticky='news')
        thread = Thread(target=download_release, kwargs={'progress': Progress(self.progress_bar_frame), 'directory': directory})
        thread.start()

class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master, img_path):
        super().__init__(master, fg_color="transparent"  )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar_image = customtkinter.CTkImage(light_image = Image.open(img_path), 
                                                    dark_image = Image.open(img_path), 
                                                    size=(120,120))
        self.image_label = customtkinter.CTkLabel(self, text="", image=self.sidebar_image)
        self.image_label.grid(row=0, column=0 )

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('IKEMEN-GO Downloader')
        self.geometry("550x130")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = SidebarFrame(self, "IkemenCylia.png")
        self.sidebar_frame.grid(row=0, column=0, sticky='nesw', padx=4, pady=4)

        self.util_frame = UtilFrame(self)
        self.util_frame.grid(row=0, column=1, sticky='nswe', padx=7, pady=7)

    def button_callback(self):
        self.util_frame.grid_remove()

    def close_window(self):
        self.destroy() 

