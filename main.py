import os
from PIL import ImageTk
from gui import App


app = App()
app.iconpath = ImageTk.PhotoImage(file="IkemenCylia.png")
app.wm_iconbitmap()
app.iconphoto(False, app.iconpath)
app.mainloop()


