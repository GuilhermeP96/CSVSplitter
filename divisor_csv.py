import pandas as pd
import os
import chardet
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Função para detectar charset automaticamente
def detect_charset(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))  # Lê uma amostra do arquivo
    return result['encoding']

# Função para detectar separador automaticamente
def detect_separator(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as f:
        first_line = f.readline()
    possible_separators = [',', ';', '\t', '|']
    sep = max(possible_separators, key=first_line.count)
    return sep

# Função para atualizar os exemplos de formato de dados
def update_format_examples(*args):
    if format_var.get() == "BR":
        decimal_example.config(text="Exemplo: 1.234,56")
        date_example.config(text="Exemplo: 31/12/2023")
        time_example.config(text="Exemplo: 23:59")
    elif format_var.get() == "EUA":
        decimal_example.config(text="Exemplo: 1,234.56")
        date_example.config(text="Exemplo: 12/31/2023")
        time_example.config(text="Exemplo: 11:59 PM")
    elif format_var.get() == "EU":
        decimal_example.config(text="Exemplo: 1 234,56")
        date_example.config(text="Exemplo: 2023-12-31")
        time_example.config(text="Exemplo: 23:59")
    elif format_var.get() == "UK":
        decimal_example.config(text="Exemplo: 1,234.56")
        date_example.config(text="Exemplo: 31-12-2023")
        time_example.config(text="Exemplo: 23:59")
    else:  # Manter Original
        decimal_example.config(text="Manter valores originais")
        date_example.config(text="Manter datas originais")
        time_example.config(text="Manter horários originais")

# Função para converter dados para o formato selecionado
def convert_data_format(data, origin_format, target_format):
    for col in data.columns:
        try:
            if "date" in col.lower():
                if origin_format == "auto":
                    data[col] = pd.to_datetime(data[col], errors='coerce')
                else:
                    data[col] = pd.to_datetime(data[col], format=origin_format, errors='coerce')
                if target_format == "BR":
                    data[col] = data[col].dt.strftime('%d/%m/%Y')
                elif target_format == "EUA":
                    data[col] = data[col].dt.strftime('%m/%d/%Y')
                elif target_format == "EU":
                    data[col] = data[col].dt.strftime('%Y-%m-%d')
                elif target_format == "UK":
                    data[col] = data[col].dt.strftime('%d-%m-%Y')
            else:
                if target_format in ["BR", "EU", "UK"]:
                    data[col] = data[col].str.replace(".", ",")
                elif target_format == "EUA":
                    data[col] = data[col].str.replace(",", ".")
        except Exception as e:
            log_text.insert(tk.END, f"Erro ao formatar a coluna '{col}': {e}\n")
            log_text.see(tk.END)
    return data

# Função para dividir o CSV com base nas configurações do usuário
def split_csv(file_path, max_rows, charset, separator, format_option, origin_format, target_format, dest_charset, dest_separator):
    try:
        data = pd.read_csv(file_path, encoding=charset, sep=separator, dtype=str)

        if format_option != "Manter Original":
            data = convert_data_format(data, origin_format, target_format)

        file_dir, file_name = os.path.split(file_path)
        file_name, file_ext = os.path.splitext(file_name)
        
        total_chunks = (len(data) // max_rows) + (1 if len(data) % max_rows != 0 else 0)
        progress_bar["maximum"] = total_chunks

        file_count = 1
        for i in range(0, len(data), max_rows):
            chunk = data[i:i + max_rows]
            output_file = os.path.join(file_dir, f"{file_name}_{file_count}{file_ext}")
            chunk.to_csv(output_file, index=False, encoding=dest_charset, sep=dest_separator, quoting=1)
          
            log_message = f"Arquivo salvo: {output_file}"
            log_text.insert(tk.END, log_message + "\n")
            log_text.see(tk.END)
            progress_bar["value"] = file_count
            root.update_idletasks()
            file_count += 1
        
        messagebox.showinfo("Sucesso", "CSV dividido com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        log_text.insert(tk.END, f"Erro: {e}\n")
        log_text.see(tk.END)

# Função para abrir o seletor de arquivo e detectar charset e separador
def select_file():
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo CSV de origem",
        filetypes=[("CSV Files", "*.csv")]
    )
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)
    
    # Detecção automática do charset e separador, se selecionado
    if charset_var.get() == "auto":
        detected_charset = detect_charset(file_path)
        charset_var.set(detected_charset)
    if separator_var.get() == "auto":
        detected_separator = detect_separator(file_path, charset_var.get())
        separator_var.set(detected_separator)

# Função para atualizar as opções de origem ao selecionar o formato
def update_origin_options(*args):
    if format_var.get() != "Manter Original":
        origin_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        origin_format_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    else:
        origin_label.grid_remove()
        origin_format_dropdown.grid_remove()

# Função chamada ao clicar no botão "Dividir CSV"
def on_split_button_click():
    file_path = entry_file_path.get()
    try:
        max_rows = int(entry_max_rows.get())
        charset = charset_var.get()
        separator = separator_var.get() if separator_var.get() != "Personalizar" else custom_separator.get()
        format_option = format_var.get()
        origin_format = origin_format_var.get()
        target_format = format_var.get()
        dest_charset = dest_charset_var.get()
        dest_separator = dest_separator_var.get() if dest_separator_var.get() != "Personalizar" else custom_dest_separator.get()
        log_text.delete("1.0", tk.END)
        progress_bar["value"] = 0
        split_csv(file_path, max_rows, charset, separator, format_option, origin_format, target_format, dest_charset, dest_separator)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de registros.")

# Cria a janela principal
root = tk.Tk()
root.title("CSV Splitter")

# Configura redimensionamento das colunas
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(9, weight=1)

# Elemento para selecionar o arquivo
tk.Label(root, text="Arquivo CSV:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_file_path = tk.Entry(root, width=40)
entry_file_path.grid(row=0, column=1, padx=10, pady=5, sticky="we")
btn_browse = tk.Button(root, text="Selecionar", command=select_file)
btn_browse.grid(row=0, column=2, padx=10, pady=5)

# Elemento para definir o número máximo de registros
tk.Label(root, text="Máx. registros por CSV:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_max_rows = tk.Entry(root, width=10)
entry_max_rows.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Charset de origem com detecção automática (padrão "auto")
tk.Label(root, text="Charset de Origem:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
charset_var = tk.StringVar(value="auto")
charset_dropdown = tk.OptionMenu(root, charset_var, "auto", "windows-1252", "utf-8", "ISO-8859-1")
charset_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Separador de origem com detecção automática (padrão "auto")
tk.Label(root, text="Separador de Origem:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
separator_var = tk.StringVar(value="auto")
separator_dropdown = tk.OptionMenu(root, separator_var, "auto", ";", ",", "\t", "|", "Personalizar")
separator_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")
custom_separator = tk.Entry(root, width=5)
custom_separator.grid(row=3, column=2, padx=10, pady=5, sticky="w")
custom_separator.grid_remove()

separator_var.trace("w", lambda *args: custom_separator.grid() if separator_var.get() == "Personalizar" else custom_separator.grid_remove())

# Opções de formatação com exemplos
tk.Label(root, text="Formato de Dados:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
format_var = tk.StringVar(value="Manter Original")
format_var.trace("w", update_origin_options)
format_var.trace("w", update_format_examples)
format_dropdown = tk.OptionMenu(root, format_var, "Manter Original", "BR", "EUA", "EU", "UK")
format_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Exemplos de formatação
decimal_example = tk.Label(root, text="")
decimal_example.grid(row=4, column=2, padx=10, pady=5, sticky="w")
date_example = tk.Label(root, text="")
date_example.grid(row=4, column=3, padx=10, pady=5, sticky="w")
time_example = tk.Label(root, text="")
time_example.grid(row=4, column=4, padx=10, pady=5, sticky="w")

# Opções de formato de origem
origin_label = tk.Label(root, text="Formato de Origem:")
origin_format_var = tk.StringVar(value="auto")
origin_format_dropdown = tk.OptionMenu(root, origin_format_var, "auto", "BR", "EUA", "EU", "UK")

# Charset de destino
tk.Label(root, text="Charset de Destino:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
dest_charset_var = tk.StringVar(value="windows-1252")
dest_charset_dropdown = tk.OptionMenu(root, dest_charset_var, "windows-1252", "utf-8", "ISO-8859-1")
dest_charset_dropdown.grid(row=6, column=1, padx=10, pady=5, sticky="w")

# Separador de destino
tk.Label(root, text="Separador de Destino:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
dest_separator_var = tk.StringVar(value=";")
dest_separator_dropdown = tk.OptionMenu(root, dest_separator_var, ";", ",", "\t", "|", "Personalizar")
dest_separator_dropdown.grid(row=7, column=1, padx=10, pady=5, sticky="w")
custom_dest_separator = tk.Entry(root, width=5)
custom_dest_separator.grid(row=7, column=2, padx=10, pady=5, sticky="w")
custom_dest_separator.grid_remove()

dest_separator_var.trace("w", lambda *args: custom_dest_separator.grid() if dest_separator_var.get() == "Personalizar" else custom_dest_separator.grid_remove())

# Barra de progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky="we")

# Caixa de texto para o log com barra de rolagem
tk.Label(root, text="Log do Processo:").grid(row=9, column=0, padx=10, pady=5, sticky="nw")
log_frame = tk.Frame(root)
log_frame.grid(row=10, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
log_text = tk.Text(log_frame, width=60, height=10, wrap="word")
log_text.grid(row=0, column=0, sticky="nsew")

scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=log_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
log_text["yscrollcommand"] = scrollbar.set

log_frame.grid_rowconfigure(0, weight=1)
log_frame.grid_columnconfigure(0, weight=1)

# Botão para dividir o CSV
btn_split = tk.Button(root, text="Dividir CSV", command=on_split_button_click)
btn_split.grid(row=11, column=1, padx=10, pady=20)

root.mainloop()
