import customtkinter

class lcarsButton(customtkinter.CTkButton):
    def __init__(self, master, text, color, **args):
        super().__init__(master, text=text, corner_radius=100, fg_color=color, text_color="black", **args)
        self.grid(padx=10, pady=10)
