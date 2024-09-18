import tkinter as tk
from tkinter import filedialog, messagebox
import re

# Expresiones regulares para el análisis léxico
token_specs = [
    ('NUMBER', r'\d+'),  # Números
    ('ID', r'[A-Za-z_]\w*'),  # Identificadores
    ('OP', r'[+*/%=<>]'),  # Operadores aritméticos y comparativos
    ('EQ', r'=='),  # Igualdad
    ('LE', r'<='),  # Menor o igual
    ('GE', r'>='),  # Mayor o igual
    ('RESERVED', r'\b(entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso)\b'),  # Palabras reservadas
    ('SIGN', r'[(){}";]'),  # Signos
    ('SKIP', r'[ \t]+'),  # Espacios en blanco
    ('NEWLINE', r'\n'),  # Nuevas líneas
    ('MISMATCH', r'.'),  # Cualquier otro carácter
]


# Analizador Léxico
def tokenize(code):
    tokens = []
    line_number = 1
    for line in code.splitlines():
        pos = 0
        while pos < len(line):
            match = None
            for token_spec in token_specs:
                kind, pattern = token_spec
                regex = re.compile(pattern)
                match = regex.match(line, pos)
                if match:
                    text = match.group(0)
                    if kind == 'NEWLINE':
                        line_number += 1
                    elif kind == 'SKIP':
                        pass
                    elif kind == 'MISMATCH':
                        messagebox.showerror("Error léxico", f"Token no válido en línea {line_number}: '{text}'")
                    else:
                        tokens.append((text, kind))
                    pos = match.end(0)
                    break
        line_number += 1
    return tokens


# Función para abrir un archivo
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, code)


# Función para analizar el contenido del archivo
def analyze():
    code = text_area.get(1.0, tk.END)
    tokens = tokenize(code)

    if tokens:
        result_window = tk.Toplevel(root)
        result_window.title("Resultados del Análisis Léxico")

        token_list = tk.Text(result_window, height=15, width=50)
        token_list.pack(padx=10, pady=10)

        token_list.insert(tk.END, "TOKEN\tTIPO\n")
        token_count = {}

        for token, kind in tokens:
            token_list.insert(tk.END, f"{token}\t{kind}\n")
            token_count[kind] = token_count.get(kind, 0) + 1

        # Mostrar conteo de tokens
        token_list.insert(tk.END, "\nCANTIDAD POR TIPO:\n")
        for kind, count in token_count.items():
            token_list.insert(tk.END, f"{kind}: {count}\n")


# Configuración de la ventana principal
root = tk.Tk()
root.title("Simulador de Analizador Léxico")

# Área de texto para mostrar el contenido del archivo
text_area = tk.Text(root, height=15, width=50)
text_area.pack(padx=10, pady=10)

# Botón para abrir archivo
open_button = tk.Button(root, text="Abrir archivo", command=open_file)
open_button.pack(pady=5)

# Botón para iniciar análisis léxico
analyze_button = tk.Button(root, text="Analizar", command=analyze)
analyze_button.pack(pady=5)

root.mainloop()
