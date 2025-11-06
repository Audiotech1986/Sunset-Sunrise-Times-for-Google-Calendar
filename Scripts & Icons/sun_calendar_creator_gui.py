import csv
import requests
from datetime import datetime, timedelta
import pytz
import tkinter as tk
from tkinter import messagebox, filedialog

def generate_calendar_csv(lat, lng, location_name, start_date, end_date, filename):
    tz_uk = pytz.timezone("Europe/London")
    
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description"])
            
            date = start_date
            while date <= end_date:
                date_str = date.strftime("%Y-%m-%d")
                url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date_str}&formatted=0"
                r = requests.get(url)
                data = r.json()["results"]
                
                sunrise_utc = datetime.fromisoformat(data["sunrise"].replace("Z", "+00:00"))
                sunset_utc  = datetime.fromisoformat(data["sunset"].replace("Z", "+00:00"))
                sunrise_local = sunrise_utc.astimezone(tz_uk)
                sunset_local  = sunset_utc.astimezone(tz_uk)
                
                sunrise_end = sunrise_local + timedelta(minutes=15)
                sunset_end  = sunset_local + timedelta(minutes=15)
                
                writer.writerow(["Sunrise", sunrise_local.strftime("%Y-%m-%d"), sunrise_local.strftime("%H:%M"),
                                 sunrise_end.strftime("%Y-%m-%d"), sunrise_end.strftime("%H:%M"),
                                 f"Sunrise in {location_name}"])
                writer.writerow(["Sunset", sunset_local.strftime("%Y-%m-%d"), sunset_local.strftime("%H:%M"),
                                 sunset_end.strftime("%Y-%m-%d"), sunset_end.strftime("%H:%M"),
                                 f"Sunset in {location_name}"])
                
                date += timedelta(days=1)
        messagebox.showinfo("Success", f"CSV file created:\n{filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def run():
    try:
        lat = float(lat_entry.get())
        lng = float(lng_entry.get())
        location_name = location_entry.get()
        start_date = datetime.strptime(start_entry.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end_entry.get(), "%Y-%m-%d")
        filename = file_entry.get()
        if not filename:
            messagebox.showerror("Error", "Please select a CSV file path")
            return
        generate_calendar_csv(lat, lng, location_name, start_date, end_date, filename)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Sunrise/Sunset Calendar CSV Generator")

tk.Label(root, text="Latitude:").grid(row=0, column=0, sticky="e")
lat_entry = tk.Entry(root)
lat_entry.grid(row=0, column=1)
lat_entry.insert(0, "51.2726")

tk.Label(root, text="Longitude:").grid(row=1, column=0, sticky="e")
lng_entry = tk.Entry(root)
lng_entry.grid(row=1, column=1)
lng_entry.insert(0, "0.5260")

tk.Label(root, text="Location Name:").grid(row=2, column=0, sticky="e")
location_entry = tk.Entry(root)
location_entry.grid(row=2, column=1)
location_entry.insert(0, "Maidstone, Kent, UK")

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")
start_entry = tk.Entry(root)
start_entry.grid(row=3, column=1)
start_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="e")
end_entry = tk.Entry(root)
end_entry.grid(row=4, column=1)
end_entry.insert(0, "2025-12-31")

tk.Label(root, text="CSV Filename:").grid(row=5, column=0, sticky="e")
file_entry = tk.Entry(root, width=30)
file_entry.grid(row=5, column=1)
tk.Button(root, text="Browse", command=browse_file).grid(row=5, column=2)

tk.Button(root, text="Generate CSV", command=run).grid(row=6, column=1, pady=10)

root.mainloop()
