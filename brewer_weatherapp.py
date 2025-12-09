import requests
import tkinter
from tkinter import messagebox

#API class
class api:    
    url = "https://api.openweathermap.org/data/2.5/weather"
    # __init__
    def __init__(self, api_key):
        #Sets own API key so it can call it and use it elsewhere, needed a lot
        self.api_key = api_key
    
    #Fetch weather makes an API call to openweathermap and then returns the json response
    # to give us our info.
    def fetch_weather(self, city):
        params = {"q": city, "appid": self.api_key, "units": "metric" }
        response = requests.get(self.url, params=params)

        # If not 200, it's not good
        if response.status_code != 200:
            raise ValueError("City does not exist or API Error.")
        #Used to test if response was valid
        #print(response.url)
        return response.json()
    #Static Method to convert C to F
    @staticmethod
    def celsiusToFahrenheit(celsius):
        return float(((celsius * 9/5) + 32))

#GUI Class
class weatherApp(api):
    #calls __init__ of parent, saves time and effort
    def __init__(self, api_key):
        super().__init__(api_key)

        #Creates window and size of window
        self.window = tkinter.Tk()
        self.window.title("Rocky's Awesome Weather App")
        self.window.geometry("400x400")

        #Prompts user what to input into entry box below
        tkinter.Label(self.window, text="Enter a City Please!", font=("Times New Roman", 12)).pack(pady=5)

        #Lets us input the city we want to check for
        self.city_entry = tkinter.Entry(self.window, width=30)
        self.city_entry.pack(pady=5)
        
        #Button that actually lets this work
        tkinter.Button(self.window, text="Get Weather", command=self.show_weather).pack(pady=10)

        #Output is where the info gathered will be put to.
        self.output = tkinter.Label(self.window, text="", font=("Times New Roman", 12))
        self.output.pack(pady=10)

        self.window.mainloop()

    def show_weather(self):
        city = self.city_entry.get()

        try:
            data = self.fetch_weather(city)

            c = data["main"]["temp"]
            f = self.celsiusToFahrenheit(c)
            
            #List with strings that contain the info to be put to output
            output = (
                f"Weather in {city.title()}:\n"
                f"Temperature: {c:.1f} Celsius or {f:.1f} Fahrenheit:\n"
            )

            #Sending to output
            self.output.config(text=output)
        except Exception as e:
            messagebox.showerror("Error",str(e))

if __name__ == "__main__":
    #Getting this API Key was both harder and easier than I thought it'd be
    api_key = "API_KEY HERE"
    #Calling class and sending API Key

    weatherApp(api_key)
