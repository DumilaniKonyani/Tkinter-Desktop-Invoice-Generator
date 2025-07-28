import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF

class InvoiceApp:
    def __init__(self, master):
        self.master = master
        master.title("Invoice Generator")

        self.items = []

        # Client Name
        tk.Label(master, text="Client Name:").grid(row=0, column=0)
        self.client_entry = tk.Entry(master)
        self.client_entry.grid(row=0, column=1)

        # Table Headers
        tk.Label(master, text="Description").grid(row=1, column=0)
        tk.Label(master, text="Qty").grid(row=1, column=1)
        tk.Label(master, text="Rate").grid(row=1, column=2)

        # First line item
        self.item_entries = []
        self.add_item_row()

        # Buttons
        self.add_button = tk.Button(master, text="Add Item", command=self.add_item_row)
        self.add_button.grid(row=100, column=0, pady=10)

        self.generate_button = tk.Button(master, text="Generate Invoice", command=self.generate_invoice)
        self.generate_button.grid(row=100, column=1, pady=10)

    def add_item_row(self):
        row = len(self.item_entries) + 2
        desc = tk.Entry(self.master)
        qty = tk.Entry(self.master, width=5)
        rate = tk.Entry(self.master, width=10)
        desc.grid(row=row, column=0, padx=5)
        qty.grid(row=row, column=1, padx=5)
        rate.grid(row=row, column=2, padx=5)
        self.item_entries.append((desc, qty, rate))

    def generate_invoice(self):
        client = self.client_entry.get().strip()
        if not client:
            messagebox.showerror("Missing Info", "Please enter a client name.")
            return

        items = []
        total = 0

        for desc_entry, qty_entry, rate_entry in self.item_entries:
            desc = desc_entry.get().strip()
            try:
                qty = int(qty_entry.get())
                rate = float(rate_entry.get())
                line_total = qty * rate
                total += line_total
                items.append((desc, qty, rate, line_total))
            except ValueError:
                continue  # skip incomplete/invalid rows

        if not items:
            messagebox.showerror("No Items", "Please add at least one valid item.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, f"Invoice for {client}", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "", ln=True)

        for desc, qty, rate, line_total in items:
            pdf.cell(200, 10, f"{desc} - {qty} x {rate:.2f} = {line_total:.2f}", ln=True)

        pdf.cell(200, 10, "", ln=True)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, f"Total: {total:.2f}", ln=True)

        filename = f"Invoice_{client.replace(' ', '_')}.pdf"
        pdf.output(filename)
        messagebox.showinfo("Success", f"Invoice saved as {filename}")

# Run the app
root = tk.Tk()
app = InvoiceApp(root)
root.mainloop()
