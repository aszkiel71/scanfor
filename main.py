import tkinter as tk
from tkinter import filedialog, scrolledtext

def load_files():
    files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    file_list.set("\n".join(files))


def similarity(word1, word2):
    word1, word2 = word1.lower(), word2.lower()
    matches = sum((min(word1.count(char), word2.count(char)) for char in set(word1)))
    return matches / max(len(word1), 1)


def search():
    files = file_list.get().split("\n")
    search_word = word_entry.get()
    threshold = float(threshold_entry.get()) / 100
    results_box.config(state=tk.NORMAL)
    results_box.delete(1.0, tk.END)

    for file in files:
        if not file.strip():
            continue
        try:
            counter = 0
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    words = line.split()
                    counter += 1
                    for word in words:
                        if similarity(search_word, word) >= threshold:
                            results_box.insert(tk.END, f"Plik: {file}\nZnaleziono: {word} w linii: {line.strip()}, linijka nr {counter}\n\n")
        except Exception as e:
            results_box.insert(tk.END, f"Błąd przy otwieraniu {file}: {str(e)}\n")

    results_box.config(state=tk.DISABLED)


root = tk.Tk()
root.title("ScanFor")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

file_list = tk.StringVar()
root.configure(bg="lightgray")
tk.Button(frame, text="Wybierz pliki", command=load_files).grid(row=0, column=0, pady=5)
tk.Label(frame, textvariable=file_list, wraplength=400, justify="left").grid(row=1, column=0, columnspan=2, pady=5)

tk.Label(frame, text="Szukane słowo:").grid(row=2, column=0, sticky="w")
word_entry = tk.Entry(frame)
word_entry.grid(row=2, column=1, pady=5)

tk.Label(frame, text="Minimalne dopasowanie (%):").grid(row=3, column=0, sticky="w")
threshold_entry = tk.Entry(frame)
threshold_entry.insert(0, "80")
threshold_entry.grid(row=3, column=1, pady=5)

tk.Button(frame, text="Szukaj", command=search).grid(row=4, column=0, columnspan=2, pady=10)

results_box = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
results_box.pack(padx=10, pady=10)

root.mainloop()