import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import gui.lcarsSettings


class plotList(customtkinter.CTkFrame):
    def __init__(self, master, figList):
        super().__init__(master)

        self.canvasList = []

        self.color = gui.lcarsSettings.magenta
        self.configure(fg_color="black", border_width=0)
        i = 0
        for f in figList:
            canvas = FigureCanvasTkAgg(f, master=self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=i, padx=10, pady=(10, 10), sticky="ew")
            self.canvasList.append(canvas)
            i = i+1


