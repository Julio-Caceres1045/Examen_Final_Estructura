import os
import graphviz
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Estudiante:
    def __init__(self, id_estudiante, nombre, apellido, edad):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

class Nodo:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        if self.raiz is None:
            self.raiz = Nodo(estudiante)
        else:
            self._insertar(self.raiz, estudiante)

    def _insertar(self, nodo_actual, estudiante):
        if estudiante.id_estudiante < nodo_actual.estudiante.id_estudiante:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(estudiante)
            else:
                self._insertar(nodo_actual.izquierdo, estudiante)
        elif estudiante.id_estudiante > nodo_actual.estudiante.id_estudiante:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(estudiante)
            else:
                self._insertar(nodo_actual.derecho, estudiante)

    def buscar(self, id_estudiante):
        return self._buscar(self.raiz, id_estudiante)

    def _buscar(self, nodo_actual, id_estudiante):
        if nodo_actual is None:
            return None
        if id_estudiante == nodo_actual.estudiante.id_estudiante:
            return nodo_actual.estudiante
        elif id_estudiante < nodo_actual.estudiante.id_estudiante:
            return self._buscar(nodo_actual.izquierdo, id_estudiante)
        else:
            return self._buscar(nodo_actual.derecho, id_estudiante)

    def eliminar(self, id_estudiante):
        self.raiz = self._eliminar(self.raiz, id_estudiante)

    def _eliminar(self, nodo_actual, id_estudiante):
        if nodo_actual is None:
            return nodo_actual

        if id_estudiante < nodo_actual.estudiante.id_estudiante:
            nodo_actual.izquierdo = self._eliminar(nodo_actual.izquierdo, id_estudiante)
        elif id_estudiante > nodo_actual.estudiante.id_estudiante:
            nodo_actual.derecho = self._eliminar(nodo_actual.derecho, id_estudiante)
        else:
            if nodo_actual.izquierdo is None:
                return nodo_actual.derecho
            elif nodo_actual.derecho is None:
                return nodo_actual.izquierdo

            nodo_minimo_mayor = self._obtener_minimo(nodo_actual.derecho)
            nodo_actual.estudiante = nodo_minimo_mayor.estudiante
            nodo_actual.derecho = self._eliminar(nodo_actual.derecho, nodo_minimo_mayor.estudiante.id_estudiante)

        return nodo_actual

    def _obtener_minimo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def listar_estudiantes(self):
        estudiantes = []
        self._recorrido_inorden(self.raiz, estudiantes)
        return estudiantes

    def _recorrido_inorden(self, nodo, estudiantes):
        if nodo is not None:
            self._recorrido_inorden(nodo.izquierdo, estudiantes)
            estudiantes.append(nodo.estudiante)
            self._recorrido_inorden(nodo.derecho, estudiantes)

    def guardar_estudiantes_en_archivo(self, nombre_archivo):
        estudiantes = self.listar_estudiantes()
        with open(nombre_archivo, 'w') as f:
            for estudiante in estudiantes:
                f.write(f'ID: {estudiante.id_estudiante}, Nombre: {estudiante.nombre}\n')

    def dibujar_arbol(self):
        if self.raiz is None:
            return None

        def agregar_aristas(grafico, nodo):
            if nodo.izquierdo is not None:
                grafico.edge(str(nodo.estudiante.id_estudiante), str(nodo.izquierdo.estudiante.id_estudiante))
                agregar_aristas(grafico, nodo.izquierdo)
            if nodo.derecho is not None:
                grafico.edge(str(nodo.estudiante.id_estudiante), str(nodo.derecho.estudiante.id_estudiante))
                agregar_aristas(grafico, nodo.derecho)

        dot = graphviz.Digraph()
        dot.node(str(self.raiz.estudiante.id_estudiante), str(self.raiz.estudiante.id_estudiante))
        agregar_aristas(dot, self.raiz)
        dot.render('abb', format='png', cleanup=True)

class ABBApp:
    def __init__(self, root):
        self.abb = ArbolBinarioBusqueda()
        self.root = root
        self.root.title("Árbol Binario de Búsqueda")

        # Crear Frame para la entrada de datos
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Entrada y etiqueta para ID
        self.lbl_id = tk.Label(self.frame, text="ID del Estudiante")
        self.lbl_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(self.frame)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        # Entrada y etiqueta para nombre
        self.lbl_nombre = tk.Label(self.frame, text="Nombre del Estudiante")
        self.lbl_nombre.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        # Entrada y etiqueta para apellido
        self.lbl_apellido = tk.Label(self.frame, text="Apellido del Estudiante")
        self.lbl_apellido.grid(row=2, column=0, padx=5, pady=5)
        self.entry_apellido = tk.Entry(self.frame)
        self.entry_apellido.grid(row=2, column=1, padx=5, pady=5)

        # Entrada y etiqueta para edad
        self.lbl_edad = tk.Label(self.frame, text="Edad del Estudiante")
        self.lbl_edad.grid(row=3, column=0, padx=5, pady=5)
        self.entry_edad = tk.Entry(self.frame)
        self.entry_edad.grid(row=3, column=1, padx=5, pady=5)

        # Agregar un espacio en blanco
        tk.Label(self.frame, text="").grid(row=4, column=0, columnspan=2)

        # Botones
        self.btn_agregar = tk.Button(self.frame, text="Agregar Estudiante", command=self.agregar_estudiante)
        self.btn_agregar.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.btn_buscar = tk.Button(self.frame, text="Buscar Estudiante", command=self.buscar_estudiante)
        self.btn_buscar.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        self.btn_eliminar = tk.Button(self.frame, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        self.btn_eliminar.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        self.btn_listar = tk.Button(self.frame, text="Listar Estudiantes", command=self.listar_estudiantes)
        self.btn_listar.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        self.btn_dibujar = tk.Button(self.frame, text="Dibujar Árbol", command=self.dibujar_arbol)
        self.btn_dibujar.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

        # Canvas para mostrar el árbol
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

    def agregar_estudiante(self):
        try:
            id_estudiante = int(self.entry_id.get())
            nombre_estudiante = self.entry_nombre.get()
            apellido_estudiante = self.entry_apellido.get()
            edad_estudiante = int(self.entry_edad.get())

            # Verificar si el ID ya está en uso
            if self.abb.buscar(id_estudiante) is not None:
                messagebox.showerror("Error", "ID ya está en uso.")
                return

            self.abb.insertar(Estudiante(id_estudiante, nombre_estudiante, apellido_estudiante, edad_estudiante))
            messagebox.showinfo("Éxito", f"Estudiante {nombre_estudiante} agregado correctamente.")
            self.actualizar_canvas()
        except ValueError:
            messagebox.showerror("Error", "ID y Edad deben ser números enteros.")

    def buscar_estudiante(self):
        try:
            id_estudiante = int(self.entry_id.get())
            estudiante = self.abb.buscar(id_estudiante)
            if estudiante:
                messagebox.showinfo("Resultado de búsqueda",
                                    f'ID: {estudiante.id_estudiante}, Nombre: {estudiante.nombre}, Apellido: {estudiante.apellido}, Edad: {estudiante.edad}')
            else:
                messagebox.showinfo("Resultado de búsqueda", "Estudiante no encontrado")
        except ValueError:
            messagebox.showerror("Error", "ID debe ser un número entero.")


    def eliminar_estudiante(self):
        try:
            id_estudiante = int(self.entry_id.get())
            self.abb.eliminar(id_estudiante)
            messagebox.showinfo("Éxito", f"Estudiante con ID {id_estudiante} eliminado correctamente.")
            self.actualizar_canvas()
        except ValueError:
            messagebox.showerror("Error", "ID debe ser un número entero.")

    def listar_estudiantes(self):
        nombre_archivo = "estudiantes.txt"
        self.abb.guardar_estudiantes_en_archivo(nombre_archivo)
        messagebox.showinfo("Lista de Estudiantes", f'Estudiantes listados en {nombre_archivo}')

    def dibujar_arbol(self):
        self.abb.dibujar_arbol()
        self.actualizar_canvas()

    def actualizar_canvas(self):
        self.canvas.delete("all")
        if os.path.exists('abb.png'):
            img = Image.open('abb.png')
            img = img.resize((800, 600), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

if __name__ == "__main__":
    root = tk.Tk()
    app = ABBApp(root)
    root.mainloop()
