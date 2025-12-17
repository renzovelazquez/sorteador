import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

class SorteadorGrandeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sorteador de Imágenes - Pantalla Grande")
        self.master.geometry("850x950") # Un poco más alto para el nuevo botón
        
        self.ruta_carpeta = ""
        self.imagenes_totales = []
        self.imagenes_pendientes = []
        self.imagen_tk = None 
        self.archivo_historial = "historial_sorteo.txt"

        self.configurar_gui()

    def configurar_gui(self):
        frame_controles = tk.Frame(self.master)
        frame_controles.pack(pady=10)

        self.label_contador = tk.Label(frame_controles, text="Esperando carpeta...", font=('Arial', 16, 'bold'), fg='blue')
        self.label_contador.pack()

        self.boton_sortear = tk.Button(self.master, text="✨ SORTEAR PRÓXIMO ✨", command=self.sortear_proxima, 
                                       font=('Arial', 18, 'bold'), bg='#4CAF50', fg='white', padx=50)
        self.boton_sortear.pack(pady=10)
        
        self.label_imagen = tk.Label(self.master, bg="#2c3e50") 
        self.label_imagen.pack(expand=True, fill="both", padx=20, pady=10)

        self.label_nombre_archivo = tk.Label(self.master, text="", font=('Consolas', 12, 'italic'))
        self.label_nombre_archivo.pack(pady=5)

        # --- SECCIÓN DE BOTONES INFERIORES ---
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(side="bottom", pady=20)

        # Botón Ver Historial
        tk.Button(btn_frame, text="📂 Ver Historial", command=self.abrir_historial_txt).pack(side="left", padx=5)
        
        # NUEVO: Botón Reiniciar Sorteo
        self.boton_reiniciar = tk.Button(btn_frame, text="🔄 Reiniciar Sorteo", command=self.reiniciar_sorteo, 
                                         bg="#f39c12", fg="white", font=('Arial', 10, 'bold'))
        self.boton_reiniciar.pack(side="left", padx=5)

        # Botón Cambiar Carpeta
        tk.Button(btn_frame, text="📁 Cambiar Carpeta", command=self.seleccionar_carpeta).pack(side="left", padx=5)

    def reiniciar_sorteo(self):
        """Restablece la lista de pendientes con todas las imágenes de la carpeta actual."""
        if not self.imagenes_totales:
            messagebox.showwarning("Aviso", "No hay imágenes cargadas para reiniciar.")
            return
        
        confirmar = messagebox.askyesno("Reiniciar", "¿Estás seguro de que quieres volver a incluir todas las imágenes en el sorteo?")
        if confirmar:
            self.imagenes_pendientes = list(self.imagenes_totales)
            self.actualizar_contador()
            self.label_imagen.config(image='', text="Sorteo reiniciado. ¡Listo para empezar!")
            self.label_nombre_archivo.config(text="")
            
            # Opcional: Anotar el reinicio en el historial
            with open(self.archivo_historial, "a", encoding="utf-8") as f:
                f.write(f"\n--- Sorteo Reiniciado: {datetime.now().strftime('%H:%M:%S')} ---\n")
            
            messagebox.showinfo("Hecho", "El bombo está lleno de nuevo.")

    def seleccionar_carpeta(self):
        nueva_ruta = filedialog.askdirectory()
        if nueva_ruta:
            self.ruta_carpeta = nueva_ruta
            self.cargar_imagenes()

    def cargar_imagenes(self):
        extensiones = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        try:
            archivos = os.listdir(self.ruta_carpeta)
            self.imagenes_totales = [os.path.join(self.ruta_carpeta, f) for f in archivos if f.lower().endswith(extensiones)]
            if not self.imagenes_totales:
                messagebox.showwarning("Error", "No hay imágenes válidas.")
                return
            self.imagenes_pendientes = list(self.imagenes_totales)
            self.actualizar_contador()
            self.label_imagen.config(image='', text="Carpeta cargada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_contador(self):
        self.label_contador.config(text=f"Restantes: {len(self.imagenes_pendientes)} / {len(self.imagenes_totales)}")

    def sortear_proxima(self):
        if not self.imagenes_pendientes:
            messagebox.showinfo("Fin", "Ya no quedan imágenes. Pulsa 'Reiniciar Sorteo' para volver a empezar.")
            return

        ruta = self.imagenes_pendientes.pop(random.randrange(len(self.imagenes_pendientes)))
        self.mostrar_imagen(ruta)
        self.actualizar_contador()
        self.label_nombre_archivo.config(text=os.path.basename(ruta))
        
        with open(self.archivo_historial, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {os.path.basename(ruta)}\n")

    def mostrar_imagen(self, ruta):
        try:
            img = Image.open(ruta)
            img.thumbnail((750, 750)) 
            self.imagen_tk = ImageTk.PhotoImage(img)
            self.label_imagen.config(image=self.imagen_tk, text="")
        except:
            self.label_imagen.config(image='', text="Error al cargar imagen")

    def abrir_historial_txt(self):
        if os.path.exists(self.archivo_historial):
            os.startfile(self.archivo_historial) if os.name == 'nt' else os.system(f'open "{self.archivo_historial}"')

if __name__ == '__main__':
    root = tk.Tk()
    app = SorteadorGrandeApp(root)
    root.mainloop()