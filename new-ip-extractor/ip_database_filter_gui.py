import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import pandas as pd

def load_ips_from_pdf(file_path):
    """Load IPs from a given PDF file and return as a set."""
    try:
        ips = set()
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    for line in text.splitlines():
                        cleaned = line.strip()
                        if cleaned:
                            ips.add(cleaned)
        if not ips:
            raise ValueError("The PDF file is empty or contains no valid IPs.")
        return ips
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load PDF file: {e}")
        return set()

class IPFilterTool:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Filter Tool — Export New IPs to Excel")

        # Labels
        tk.Label(root, text="Scanned/New IPs PDF:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Database IPs PDF:").grid(row=1, column=0, padx=10, pady=10)

        # Entry fields
        self.file1_entry = tk.Entry(root, width=50)
        self.file1_entry.grid(row=0, column=1, padx=10, pady=10)

        self.file2_entry = tk.Entry(root, width=50)
        self.file2_entry.grid(row=1, column=1, padx=10, pady=10)

        # Browse buttons
        tk.Button(root, text="Browse", command=self.browse_file1).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_file2).grid(row=1, column=2, padx=10, pady=10)

        # Compare Button
        tk.Button(root, text="Export New IPs to Excel", command=self.export_new_ips,
                  bg="green", fg="white", width=30).grid(row=2, column=1, pady=20)

    def browse_file1(self):
        file_path = filedialog.askopenfilename(title="Select Scanned/New IPs PDF", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file1_entry.delete(0, tk.END)
            self.file1_entry.insert(0, file_path)

    def browse_file2(self):
        file_path = filedialog.askopenfilename(title="Select Database IPs PDF", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file2_entry.delete(0, tk.END)
            self.file2_entry.insert(0, file_path)

    def export_new_ips(self):
        file1_path = self.file1_entry.get()
        file2_path = self.file2_entry.get()

        if not file1_path or not file2_path:
            messagebox.showwarning("Missing Input", "Please select both PDF files.")
            return

        scanned_ips = load_ips_from_pdf(file1_path)
        database_ips = load_ips_from_pdf(file2_path)

        if not scanned_ips or not database_ips:
            return  # Errors already shown

        # Filter IPs that are not in the database
        new_ips = sorted(scanned_ips - database_ips)

        if not new_ips:
            messagebox.showinfo("No New IPs", "All scanned IPs already exist in the database.")
            return

        # Prompt user to choose save location
        output_file = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save New IPs to Excel"
        )

        if not output_file:
            return  # User cancelled

        try:
            df = pd.DataFrame(new_ips, columns=["New IPs"])
            df.to_excel(output_file, index=False)
            messagebox.showinfo("Success", f"New IPs saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to write Excel file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPFilterTool(root)
    root.mainloop()
