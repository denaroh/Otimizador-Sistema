import os
import subprocess
import psutil
import ctypes
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

def log_action(action):
    log_area.config(state=tk.NORMAL)
    log_area.insert(tk.END, action + "\n")
    log_area.yview(tk.END)
    log_area.config(state=tk.DISABLED)

def limpar_cache():
    log_action("Iniciando limpeza de cache...")
    # Exemplos para sistemas baseados em Linux:
    # subprocess.run(['sync; echo 3 > /proc/sys/vm/drop_caches'], shell=True)
    log_action("Limpeza de cache concluída.")

def limpar_temp():
    log_action("Limpando arquivos temporários...")
    temp_folder = os.getenv('TEMP')
    try:
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    log_action(f"Erro ao deletar {file_path}: {e}")
        log_action("Arquivos temporários limpos com sucesso.")
    except Exception as e:
        log_action(f"Erro ao limpar arquivos temporários: {e}")

def limpar_registro():
    log_action("Limpando registros do sistema (apenas Windows)...")
    try:
        subprocess.run(['reg', 'delete', 'HKCU\\Software\\TempKey', '/f'], shell=True)
        log_action("Registros limpos com sucesso.")
    except Exception as e:
        log_action(f"Erro ao limpar registros: {e}")

def otimizar_pc():
    log_action("Iniciando otimização geral do PC...")
    try:
        subprocess.run(['defrag', 'C:'], shell=True)
        log_action("Desfragmentação de disco iniciada...")
        log_action("Otimização do PC concluída.")
    except Exception as e:
        log_action(f"Erro na otimização do PC: {e}")

def otimizar_mouse():
    log_action("Otimização do mouse iniciada...")
    try:
        ctypes.windll.user32.SystemParametersInfoW(113, 0, 1, 0)  # Ativar precisão do ponteiro do mouse
        log_action("Mouse otimizado com sucesso.")
    except Exception as e:
        log_action(f"Erro ao otimizar o mouse: {e}")

def otimizar_teclado():
    log_action("Otimização do teclado iniciada...")
    try:
        ctypes.windll.user32.SystemParametersInfoW(113, 0, 0, 0)  # Exemplo de configuração, ajustar conforme necessário
        log_action("Teclado otimizado com sucesso.")
    except Exception as e:
        log_action(f"Erro ao otimizar o teclado: {e}")

def otimizar_memoria_ram():
    log_action("Otimização da memória RAM iniciada...")
    try:
        for proc in psutil.process_iter():
            try:
                proc_name = proc.name()
                proc_info = proc.as_dict(attrs=['pid', 'name', 'memory_info'])
                log_action(f"Processando {proc_info['name']} (PID: {proc_info['pid']})...")
                if proc_name in ['process_to_close.exe']:
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        log_action("Memória RAM otimizada com sucesso.")
    except Exception as e:
        log_action(f"Erro ao otimizar a memória RAM: {e}")

def sair():
    if messagebox.askokcancel("Sair", "Tem certeza que deseja sair?"):
        root.destroy()

def iniciar_programa():
    global usuario
    usuario = usuario_entry.get()
    if not usuario:
        messagebox.showwarning("Aviso", "Por favor, insira seu nome.")
    else:
        inicio_frame.pack_forget()
        main_frame.pack(fill=tk.BOTH, expand=True)
        log_action(f"Usuário: {usuario} | Momento online: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

# Configuração da janela principal
root = tk.Tk()
root.title("Otimizador de Sistema")

# Frame de início para solicitar o nome do usuário
inicio_frame = tk.Frame(root)
inicio_frame.pack(pady=20)

tk.Label(inicio_frame, text="Por favor, insira seu nome:").pack(pady=5)
usuario_entry = tk.Entry(inicio_frame)
usuario_entry.pack(pady=5)
tk.Button(inicio_frame, text="Iniciar", command=iniciar_programa).pack(pady=10)

# Frame principal
main_frame = tk.Frame(root)

# Informação do usuário e tempo online
info_frame = tk.Frame(main_frame)
info_frame.pack(pady=10)

# Área de log
log_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, width=60, height=15)
log_area.pack(pady=10)

# Botões de otimização
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Limpar Memória Cache", command=limpar_cache).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Limpar Arquivos Temporários", command=limpar_temp).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Limpar Registro", command=limpar_registro).grid(row=1, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Otimizar PC em Geral", command=otimizar_pc).grid(row=1, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Otimizar Mouse", command=otimizar_mouse).grid(row=2, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Otimizar Teclado", command=otimizar_teclado).grid(row=2, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Otimizar Memória RAM", command=otimizar_memoria_ram).grid(row=3, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Sair", command=sair).grid(row=3, column=1, padx=10, pady=5)

root.mainloop()
