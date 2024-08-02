import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

class Inventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario")
        self.root.geometry("400x300")

        style = ttk.Style()
        style.configure("TLabel", font=("arial", 12), padding=5, foreground="red")
        style.configure("TEntry", font=("arial", 12), padding=5, fieldbackground="yellow")
        style.configure("TButton", font=("arial", 12), padding=5, background="red")
        style.configure("TFrame", padding=10, background="grey")

        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.product_label = ttk.Label(main_frame, text="Producto(🛒):")
        self.product_label.grid(row=0, column=0, sticky=tk.E)
        self.product_entry = ttk.Entry(main_frame)  
        self.product_entry.grid(row=0, column=1, padx=10, pady=5)

        self.purchase_label = ttk.Label(main_frame, text="Comprar (📦):")
        self.purchase_label.grid(row=1, column=0, sticky=tk.E)
        self.purchase_entry = ttk.Entry(main_frame)
        self.purchase_entry.grid(row=1, column=1, padx=10, pady=5) 

        self.sales_label = ttk.Label(main_frame, text="Vender (💸):")
        self.sales_label.grid(row=2, column=0, sticky=tk.E)
        self.sales_entry = ttk.Entry(main_frame)
        self.sales_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(main_frame, text="Agregar", command=self.add_record)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.show_button = ttk.Button(main_frame, text="Mostrar Inventario", command=self.show_inventory)
        self.show_button.grid(row=4, column=0, columnspan=2, pady=10)


        self.filename = "bodega"
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Producto", "Compras", "Ventas"])

    def add_record(self):
        product = self.product_entry.get()
        try:
            purchase = int(self.purchase_entry.get())
            sales = int(self.sales_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos para compras y ventas")
            return

        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product, purchase, sales])

        messagebox.showinfo("Éxito", "Registro agregado con éxito")
        self.clear_entries()

    def clear_entries(self):
        self.product_entry.delete(0, tk.END)
        self.purchase_entry.delete(0, tk.END)
        self.sales_entry.delete(0, tk.END)

    def show_inventory(self):
        inventory = {}
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                product, purchase, sales = row
                purchase = int(purchase)
                sales = int(sales)
                if product in inventory:
                    inventory[product]["Compras"] += purchase
                    inventory[product]["Ventas"] += sales
                else:
                    inventory[product] = {"Compras": purchase, "Ventas": sales}

        inventory_list = []
        for product, data in inventory.items():
            inventory_list.append(f"Producto: {product}, Compras: {data['Compras']}, Ventas: {data['Ventas']}, Inventario: {data['Compras'] - data['Ventas']}")

        messagebox.showinfo("Inventario", "\n".join(inventory_list))

if __name__ == "__main__":
    root = tk.Tk()
    app = Inventario(root)
    root.mainloop()
