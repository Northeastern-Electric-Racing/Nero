import tkinter
import customtkinter

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("./themes/ner.json")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("NERO")
        self.geometry(f"{1100}x{580}")

        # create 2x2 grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.logo_label = customtkinter.CTkLabel(
            master=self, text="NERO", font=customtkinter.CTkFont(size=36, weight="bold"), anchor="w")
        self.logo_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.button = customtkinter.CTkButton(
            master=self, command=self.button_callback)
        self.button.grid(row=1, column=0)

        self.speed = customtkinter.CTkLabel(
            master=self, text="Speed:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.speed.grid(row=1, column=1)
        self.mph = customtkinter.CTkLabel(
            master=self, text="45 mph", font=customtkinter.CTkFont(size=36, weight="bold"))
        self.mph.grid(row=2, column=1)

    def button_callback(self):
        print("button pressed")


if __name__ == "__main__":
    app = App()
    app.mainloop()
