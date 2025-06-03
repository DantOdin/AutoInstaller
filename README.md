# AutoInstaller



## 🧰 Generador de Ejecutables con PyInstaller (GUI)

Esta aplicación te permite crear ejecutables `.exe` fácilmente desde archivos `.py` utilizando una interfaz gráfica con Tkinter (usando ttk). Internamente se apoya en PyInstaller y permite configurar opciones comunes como:

- Empaquetado en un solo archivo (--onefile)
- Ocultar la consola (--noconsole)
- Agregar íconos personalizados (--icon)
- Incluir archivos adicionales (--add-data)
- Ver la salida en tiempo real en una consola integrada
- Barra de carga durante la ejecución

## 🔧 Requisitos

1. Python 3.7 o superior  
2. Instalar PyInstaller con pip:

    pip install pyinstaller

## 📦 Instalación

Simplemente descarga el archivo `pyinstaller_gui.py` y ejecútalo:

    python pyinstaller_gui.py

O bien, compílalo tú mismo con PyInstaller para usarlo como ejecutable:

    pyinstaller --noconsole --onefile --icon=tu_icono.ico pyinstaller_gui.py

## 🖱️ Uso

1. Selecciona el archivo `.py` que deseas empaquetar.
2. (Opcional) Selecciona un archivo `.ico` para el ícono del ejecutable.
3. (Opcional) Agrega archivos extra si tu script los necesita (--add-data).
4. Marca las opciones:
   - Un solo archivo (--onefile)
   - Sin consola (--noconsole)
5. Haz clic en "Generar ejecutable".
6. El resultado se encuentra en la carpeta `dist/`.

Durante el proceso, la salida de PyInstaller aparecerá en tiempo real en la consola integrada, y verás una barra de progreso animada mientras se ejecuta.

## 🧠 Estructura del Código

El código está dividido en las siguientes secciones:

1. Variables y Layout de la ventana

   Se definen las opciones disponibles y se construye la interfaz con ttk.Frame, ttk.Entry, ttk.Button, ttk.Checkbutton, etc.

2. Selección de archivos

   Funciones para abrir ventanas de diálogo:
   - select_script(): seleccionar el archivo `.py`
   - select_icon(): seleccionar el `.ico`
   - add_extra_files(): seleccionar archivos adicionales

3. Generación del comando PyInstaller

   Se arma dinámicamente según las opciones seleccionadas.

4. Ejecución y captura de salida

   Se usa subprocess.Popen() para capturar la salida línea por línea y se imprime en un Text() con Scrollbar.

5. Barra de progreso

   La barra solo aparece mientras se ejecuta PyInstaller.

## 🗂️ Estructura de carpetas tras compilar

/dist/
  tu_programa.exe     <- Ejecutable final
/build/
  ...                 <- Archivos temporales
*.spec                <- Archivo de configuración PyInstaller

Puedes borrar build/ y .spec si no los necesitas.

## 📄 Licencia

Este proyecto es de código abierto. Puedes usarlo, modificarlo y distribuirlo libremente. pero porfavor siempre informa del autor.

## 📬 Soporte

Si tienes dudas o ideas para mejorar esta herramienta, ¡no dudes en contribuir!

