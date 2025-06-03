import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Ejecutables - PyInstaller")
        self.root.geometry("850x500")
        self.root.minsize(750, 400)

        # Variables
        self.script_path = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.extra_files = []
        self.onefile = tk.BooleanVar(value=True)
        self.noconsole = tk.BooleanVar(value=True)

        # GUI
        self.build_gui()

    def build_gui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        # === Parte superior ===
        ttk.Label(frame, text="Script principal (.py):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.script_path, width=70).grid(row=0, column=1, sticky="ew")
        ttk.Button(frame, text="Buscar", command=self.select_script).grid(row=0, column=2)

        ttk.Label(frame, text="Icono (.ico):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.icon_path, width=70).grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Buscar", command=self.select_icon).grid(row=1, column=2)

        ttk.Label(frame, text="Archivos adicionales:").grid(row=2, column=0, sticky="nw")
        self.extra_label = ttk.Label(frame, text="(Ninguno)", wraplength=500, justify="left")
        self.extra_label.grid(row=2, column=1, sticky="w")
        ttk.Button(frame, text="Agregar", command=self.add_extra_files).grid(row=2, column=2)

        ttk.Checkbutton(frame, text="Un solo archivo (--onefile)", variable=self.onefile).grid(row=3, column=1, sticky="w")
        ttk.Checkbutton(frame, text="Sin consola (--noconsole)", variable=self.noconsole).grid(row=4, column=1, sticky="w")

        ttk.Button(frame, text="Generar ejecutable", command=self.run_in_thread).grid(row=5, column=1, pady=10)

        # === Consola de salida ===
        self.console_output = tk.Text(frame, height=12, wrap="word", state="disabled")
        self.console_output.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        scrollbar = ttk.Scrollbar(frame, command=self.console_output.yview)
        scrollbar.grid(row=6, column=3, sticky="ns")
        self.console_output.configure(yscrollcommand=scrollbar.set)

        # === Barra de progreso (inicialmente oculta) ===
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(row=7, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        self.progress.grid_remove()  # Ocultar al inicio

        # Ajuste dinámico
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def log(self, message):
        self.console_output.config(state="normal")
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)
        self.console_output.config(state="disabled")

    def select_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            self.script_path.set(path)

    def select_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if path:
            self.icon_path.set(path)

    def add_extra_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.extra_files.extend(files)
            self.extra_label.config(text="\n".join(self.extra_files[-5:]) + ("..." if len(self.extra_files) > 5 else ""))

    def run_in_thread(self):
        thread = threading.Thread(target=self.run_pyinstaller)
        thread.start()

    def run_pyinstaller(self):
        script = self.script_path.get()
        if not script:
            messagebox.showerror("Error", "Debes seleccionar un archivo .py")
            return

        # Mostrar barra de carga
        self.progress.grid()
        self.progress.start()

        cmd = ["pyinstaller"]
        if self.onefile.get():
            cmd.append("--onefile")
        if self.noconsole.get():
            cmd.append("--noconsole")
        if self.icon_path.get():
            cmd.append(f"--icon={self.icon_path.get()}")
        for file in self.extra_files:
            cmd.append(f"--add-data={file};.")

        cmd.append(script)
        self.log("Ejecutando: " + " ".join(cmd))

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in iter(process.stdout.readline, ''):
                self.log(line.strip())
            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                self.log("✅ Ejecutable generado correctamente.")
            else:
                self.log("❌ PyInstaller terminó con errores.")
        except Exception as e:
            self.log(f"❌ Error al ejecutar PyInstaller:\n{e}")
        finally:
            self.progress.stop()
            self.progress.grid_remove()

# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    app = PyInstallerGUI(root)
    root.mainloop()
