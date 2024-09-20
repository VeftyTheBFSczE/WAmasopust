import tkinter as tk
from tkinter import messagebox
import requests
from requests.auth import HTTPBasicAuth


root = tk.Tk()
root.title("Evidenční formulář kávy")


consumption_data = []



def submit_data():
    person = person_var.get()
    coffee_type = coffee_var.get()
    quantity = quantity_var.get()

    if not quantity:
        messagebox.showwarning("Chyba", "Zadejte množství!")
        return

    data = {
        "person": person,
        "coffeeType": coffee_type,
        "quantity": quantity
    }

    consumption_data.append(data)
    messagebox.showinfo("Úspěch", "Data byla úspěšně uložena!")


# Function to show coffee consumption
def show_consumption():
    if consumption_data:
        consumption_window = tk.Toplevel(root)
        consumption_window.title("Seznam vypité kávy")
        output = tk.Text(consumption_window, wrap="word", height=10, width=50)
        output.pack(padx=10, pady=10)

        for item in consumption_data:
            output.insert(tk.END, f"{item['person']} vypil {item['quantity']} ml {item['coffeeType']}\n")
    else:
        messagebox.showwarning("Chyba", "Nebyly nalezeny žádné záznamy.")


# Function to fetch and display monthly summary
def show_monthly_summary():
    month = month_entry.get()

    if not month.isdigit() or int(month) < 1 or int(month) > 12:
        messagebox.showwarning("Chyba", "Neplatné číslo měsíce!")
        return

    try:
        response = requests.get(f"http://ajax1.lmsoft.cz/procedure.php?cmd=getSummaryOfDrinks&month={month}",
                                auth=HTTPBasicAuth('cafe', 'cafe'))
        data = response.json()

        summary_window = tk.Toplevel(root)
        summary_window.title(f"Měsíční přehled pro měsíc {month}")
        output = tk.Text(summary_window, wrap="word", height=10, width=50)
        output.pack(padx=10, pady=10)

        for item in data:
            output.insert(tk.END, f"{item['person']} vypil celkem {item['totalQuantity']} ml kávy\n")
    except Exception as e:
        messagebox.showerror("Chyba", f"Došlo k chybě při načítání měsíčního přehledu: {e}")



tk.Label(root, text="Osoba:").pack(anchor="w")
person_var = tk.StringVar(value="Masopust Lukáš")
person_menu = tk.OptionMenu(root, person_var, "Masopust Lukáš", "Molič Jan", "Adámek Daniel", "Weber David")
person_menu.pack(fill="x", pady=5)

tk.Label(root, text="Typ kávy:").pack(anchor="w")
coffee_var = tk.StringVar(value="Mléko")
coffee_menu = tk.OptionMenu(root, coffee_var, "Mléko", "Espresso", "Coffe", "Long", "Dopio++")
coffee_menu.pack(fill="x", pady=5)

tk.Label(root, text="Množství (v ml):").pack(anchor="w")
quantity_var = tk.StringVar()
quantity_entry = tk.Entry(root, textvariable=quantity_var)
quantity_entry.pack(fill="x", pady=5)

submit_button = tk.Button(root, text="Odeslat", command=submit_data)
submit_button.pack(pady=5)

show_button = tk.Button(root, text="Zobrazit spotřebu", command=show_consumption)
show_button.pack(pady=5)

tk.Label(root, text="Zadejte číslo měsíce (1-12):").pack(anchor="w")
month_entry = tk.Entry(root)
month_entry.pack(fill="x", pady=5)

summary_button = tk.Button(root, text="Zobrazit měsíční přehled", command=show_monthly_summary)
summary_button.pack(pady=5)

# Start the application
root.mainloop()
