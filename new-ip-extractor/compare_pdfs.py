import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

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
                        ips.add(line.strip())
        if not ips:
            raise ValueError("The PDF file is empty or contains no valid IPs.")
        return ips
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please select a valid file.")
        return set()
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
        return set()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load PDF file: {e}")
        return set()

def compare_ips():
    """Compare IPs from two PDF files and display missing IPs."""
    file1_path = filedialog.askopenfilename(title="Select Configured IPs PDF", filetypes=[("PDF Files", "*.pdf")])
    file2_path = filedialog.askopenfilename(title="Select IP Range PDF", filetypes=[("PDF Files", "*.pdf")])

    if not file1_path or not file2_path:
        messagebox.showwarning("Warning", "Please select both files.")
        return

    configured_ips = load_ips_from_pdf(file1_path)
    ip_range = load_ips_from_pdf(file2_path)

    if not configured_ips or not ip_range:
        return  # Error messages already shown in load_ips_from_pdf

    missing_ips = ip_range - configured_ips
    count_missing = len(missing_ips)

    result_text = f"Count of Missing IPs: {count_missing}\n"
    result_text += "List of Missing IPs:\n" + "\n".join(missing_ips) if missing_ips else "No missing IPs."

    messagebox.showinfo("Missing IPs", result_text)

# Create the main window
root = tk.Tk()
root.title("IP Comparison Tool")

# Create a button to start the comparison
compare_button = tk.Button(root, text="Compare IP Lists", command=compare_ips)
compare_button.pack(pady=20)

# Run the application
root.mainloop()
