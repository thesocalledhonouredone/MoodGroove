import tkinter as tk
from tkinter import messagebox

class DetailsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Preference")
        self.root.geometry("600x400")
        self.root.config(bg="#f0f0f0")

        self.create_widgets()

        # final returns
        self.num = 0
        self.lang = ""
        self.phno = ""

    def create_widgets(self):
        tk.Label(self.root, text="Song Preference", font=("Arial", 16, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Number of Songs:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=20, pady=10, sticky='e')
        self.num_songs_entry = tk.Entry(self.root, font=("Arial", 12), borderwidth=2, relief="solid")
        self.num_songs_entry.grid(row=1, column=1, padx=20, pady=10, sticky='w')

        tk.Label(self.root, text="Language Preference:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=20, pady=10, sticky='e')
        self.language_var = tk.StringVar(self.root)
        self.language_var.set("English")
        self.language_menu = tk.OptionMenu(self.root, self.language_var, 'Telugu', 'Tamil', 'Hindi', 'English')
        self.language_menu.config(font=("Arial", 12), bg="#ffffff", borderwidth=2, relief="solid")
        self.language_menu.grid(row=2, column=1, padx=20, pady=10, sticky='w')

        tk.Label(self.root, text="Phone Number:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=20, pady=10, sticky='e')
        self.phone_entry = tk.Entry(self.root, font=("Arial", 12), borderwidth=2, relief="solid")
        self.phone_entry.grid(row=3, column=1, padx=20, pady=10, sticky='w')

        self.submit_button = tk.Button(self.root, text="Submit", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#ffffff", command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20, padx=10)

    def submit(self):
        num_songs = self.num_songs_entry.get()
        language = self.language_var.get()
        phone = self.phone_entry.get()

        if not num_songs.isdigit() or not phone.isdigit():
            messagebox.showerror("Input Error", "Please enter valid numbers for songs and phone number.")
            return
        
        messagebox.showinfo("Submitted Information", 
                            f"Number of songs: {num_songs}\n"
                            f"Preferred language: {language}\n"
                            f"Phone number: {phone}")

        self.return_values(num_songs, language, phone)

    def return_values(self, num_songs, language, phone):
        print(f"Returned values: {num_songs}, {language}, {phone}")
        self.num = num_songs
        self.lang = language
        self.phno = phone

    def ret_details(self):
        return [self.num, self.lang, self.phno]

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SongPreferenceApp(root)
#     root.mainloop()
