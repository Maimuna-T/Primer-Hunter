import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

def reverse_complement(primer):
    """Generate the reverse complement of the primer sequence."""
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement.get(base, base) for base in reversed(primer))

def compute_kmp_table(pattern):
    """Compute the prefix table (LPS array) for KMP search."""
    m = len(pattern)
    lps = [0] * m
    j = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(dna, primer_rev):
    """Search for occurrences of the reverse complement primer in the DNA sequence using KMP."""
    n, m = len(dna), len(primer_rev)
    lps = compute_kmp_table(primer_rev)
    positions = []
    i = j = 0  # Pointers for DNA and primer_rev

    while i < n:
        if primer_rev[j] == dna[i]:
            i += 1
            j += 1
        
        if j == m:  # Full match found
            positions.append(i - j + 1)
            j = lps[j - 1]
        elif i < n and primer_rev[j] != dna[i]:
            j = lps[j - 1] if j != 0 else 0
            if j == 0:
                i += 1

    return positions

def run_button_click():
    """Handle the 'Result' button click, process input, and find primer binding sites."""
    dna = dna_entry.get().upper().strip()
    primer = primer_entry.get().upper().strip()

    if not dna or not primer:
        messagebox.showerror("Input Error", "Please enter both DNA sequence and primer.")
        return

    primer_rev = reverse_complement(primer)
    positions = kmp_search(dna, primer_rev)

    if positions:
        result_label.config(text=f"Primer binds at positions: {positions}\nTotal matches: {len(positions)}", font=("Arial", 16))
    else:
        result_label.config(text="No primer binding sites found.", font=("Arial", 16))

def upload_file():
    """Allow the user to upload a DNA sequence from a text file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            dna_sequence = file.read().strip()
            dna_entry.delete(0, tk.END)
            dna_entry.insert(0, dna_sequence)

# GUI Setting

root = tk.Tk()
root.title("Primer Binding Detection")
root.configure(bg="aliceblue")
root.geometry("900x700")  # Set window size

#  Header 
head_label = tk.Label(root, text=" Primer_Hunter ", font=("Arial", 40, "bold"), bg="aliceblue", fg="teal")
head_label.pack(pady=20, anchor="center")

# Image Display 
try:
    image = Image.open("dna.png")  # Replace with actual image file path
    image = image.resize((1310, 250))  # Resize image
    photo = ImageTk.PhotoImage(image)

    # Label for Image
    image_label = tk.Label(root, image=photo, bg="teal")
    image_label.Image = photo
    image_label.place(x=100, y=100)  # Adjusted position
except Exception as e:
    print(f"Error loading image: {e}")



#  Input Fields 
dna_label = tk.Label(root, text="DNA Sequence:", font=("Arial", 20), bg="teal", fg="white")
dna_label.place(x=100, y=400)

dna_entry = tk.Entry(root, width=50, font=("Arial", 18))
dna_entry.place(x=350, y=400)

upload_button = tk.Button(root, text="Upload DNA File", command=upload_file, font=("Arial", 14), bg="lightblue")
upload_button.place(x=100, y=465)

primer_label = tk.Label(root, text="Primer Sequence:", font=("Arial", 20), bg="teal", fg="white")
primer_label.place(x=100, y=520)

primer_entry = tk.Entry(root, width=40, font=("Arial", 18))
primer_entry.place(x=350, y=520)



# Buttons & Result Label 
run_button = tk.Button(root, text="Find Binding Sites & Positions ", command=run_button_click, font=("Arial", 20), bg="lightblue")
run_button.place(x=100, y=600)

result_label = tk.Label(root, text="Primer binding sites will be displayed here:", font=("Arial", 20), bg="aliceblue", fg="black")
result_label.place(x=100, y=690)

# Start GUI 
root.mainloop()
