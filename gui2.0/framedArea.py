import customtkinter

class framedArea(customtkinter.CTkFrame):
    def __init__(self, master, color, bar=None):
        super().__init__(master)
        self.master = master

        self.color = color

        self.configure(fg_color="black", border_color=self.color, border_width=4, corner_radius=20)
        if bar==True:
            upperBorder = customtkinter.CTkFrame(self)
            upperBorder.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=1)
            upperBorder.configure(fg_color=color, border_color=color, border_width=3, height=20, corner_radius=0)
            self.configure(border_width=0)

