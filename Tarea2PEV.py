import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import time

class IniciarSesion(tk.Frame): #Ventana de inicio de sesión, aparecerá cada que se abra el programa
    def __init__(self, master):
        super().__init__(master, bg='#B2FFF9') #Color de fondo
        self.master = master

        tk.Label(self, text="Usuario:", bg='#B2FFF9', fg='black').pack() #Campo de usuario
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack()

        tk.Label(self, text="Contraseña:", bg='#B2FFF9', fg='black').pack() #Campo para contraseña
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion, bg='lightblue', fg='black').pack()
        tk.Button(self, text="Registrar", command=self.master.show_registrar_usuario, bg='lightgreen', fg='black').pack()

    def iniciar_sesion(self): #Efectuar el inicio de sesión
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        for user in Data.usuarios:
            if user.nombre == usuario and user.password == password:
                self.master.usuario_actual = user
                self.master.show_gestion_citas(user)
                return

        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

class RegistrarUsuario(tk.Frame): #Registro de usuarios
    def __init__(self, master):
        super().__init__(master, bg='#B2FFF9')  #Color de fondo para el campo de registro
        self.master = master

        tk.Label(self, text="Nombre de usuario:", bg='#B2FFF9', fg='black').pack()
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack()

        tk.Label(self, text="Contraseña:", bg='#B2FFF9', fg='black').pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Button(self, text="Registrar", command=self.registrar_usuario, bg='lightblue', fg='black').pack()
        tk.Button(self, text="Volver", command=self.master.show_iniciar_sesion, bg='lightcoral', fg='black').pack()

    def registrar_usuario(self): #Método para registrar usuario
        nombre = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not nombre or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Verificar si el usuario ya existe
        for user in Data.usuarios:
            if user.nombre == nombre:
                messagebox.showerror("Error", "El usuario ya existe.")
                return

        # Crear nuevo usuario
        nuevo_usuario = Usuario(nombre, password)
        Data.usuarios.append(nuevo_usuario)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")

        self.master.show_iniciar_sesion()
        
class Cita: #Clase para definir citas
    def __init__(self, paciente, nombre_medico, especialidad, fecha, hora):
        self.paciente = paciente
        self.nombre_medico = nombre_medico
        self.especialidad = especialidad
        self.fecha = fecha
        self.hora = hora

    def __str__(self): #Devolver parámetros introducidos cuando se agende una cita
        return f"Cita del/la paciente {self.paciente} con el médico/a {self.especialidad} de {self.nombre_medico} el {self.fecha} a las {self.hora}"

class Usuario: #Clase para usuario con sus datos
    def __init__(self, nombre, password, es_admin=False):
        self.nombre = nombre
        self.password = password
        self.es_admin = es_admin
        self.citas = []

class Data: #Clase para almacenar usuarios
    usuarios = [] #Al inicio no habrá ninguno

class AppCitasMedicas(tk.Tk): #Clase con la interfaz de la aplicación
    def __init__(self):
        super().__init__()
        self.title("SISTEMA DE CITAS MÉDICAS")
        self.geometry("400x400")
        self.configure(bg='#B2FFF9')
        self.current_frame = None
        self.usuario_actual = None
        self.reloj_label = tk.Label(self, font=("Arial", 12), bg='#B2FFF9', fg='black')
        self.reloj_label.pack(pady=5)
        self.actualizar_reloj()
        self.show_iniciar_sesion()

    def actualizar_reloj(self): #Fecha y hora en tiempo real
        """Actualiza la hora en tiempo real."""
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.reloj_label.config(text=f"Fecha y Hora: {now}")
        self.after(1000, self.actualizar_reloj)

    def show_iniciar_sesion(self): #Método que muestra ventana de iniciar sesión
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = IniciarSesion(self)
        self.current_frame.pack()

    def show_registrar_usuario(self): #Método que muestra ventana de registro
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegistrarUsuario(self)
        self.current_frame.pack()

    def show_gestion_citas(self, usuario): #Método que muestra la ventana de gestión de citas
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = GestionCitas(self, usuario)
        self.current_frame.pack()

class GestionCitas(tk.Frame): #Clase con el sistema de gestión de citas
    def __init__(self, master, usuario):
        super().__init__(master, bg='#B2FFF9')  
        self.master = master
        self.usuario = usuario

        tk.Label(self, text=f"Bienvenido/a {self.usuario.nombre}", bg='#B2FFF9', fg='black').pack()
        self.citas_listbox = tk.Listbox(self)
        self.citas_listbox.pack()

        tk.Button(self, text="Agendar Cita", command=self.agendar_cita, bg='lightblue', fg='black').pack()
        tk.Button(self, text="Eliminar Cita", command=self.eliminar_cita, bg='lightcoral', fg='black').pack()
        tk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion, bg='lightyellow', fg='black').pack()

    def actualizar_lista_citas(self): #Método para actualizar citas
        self.citas_listbox.delete(0, tk.END)
        if self.usuario.es_admin:
            for user in Data.usuarios:
                for cita in user.citas:
                    self.citas_listbox.insert(tk.END, f"{user.nombre}: {cita}")
        else:
            for cita in self.usuario.citas:
                self.citas_listbox.insert(tk.END, cita)

    def existe_cita(self, fecha, hora): #Método para evitar citas con la misma fecha y/o hora
        """Verifica si ya existe una cita en la misma fecha y hora."""
        for user in Data.usuarios:
            for cita in user.citas:
                if cita.fecha == fecha and cita.hora == hora:
                    return True
        return False

    def agendar_cita(self): #Método para agendar citas
        paciente = self.usuario.nombre
        especialidad = simpledialog.askstring("Especialidad", "Ingrese la especialidad médica:")
        nombre_medico = simpledialog.askstring("Médico", "Ingrese el nombre del médico:")
        fecha = simpledialog.askstring("Fecha", "Ingrese la fecha (YYYY-MM-DD):")
        hora = simpledialog.askstring("Hora", "Ingrese la hora (HH:MM):")

        if not (especialidad and fecha and hora): #If para obligar al usuario a rellenar todos los campos
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            fecha_datetime = datetime.strptime(fecha, "%Y-%m-%d")  # Validar fecha
            hora_datetime = datetime.strptime(hora, "%H:%M")  # Validar hora
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha u hora incorrecto.")
            return
        
        cita_datetime = datetime.combine(fecha_datetime.date(), hora_datetime.time()) #Juntar variables fecha y hora en una sola

        now = datetime.now() #Variable que representa el método actual

        if cita_datetime < now: #If para evitar fechas y horas anteriores a la actual
            messagebox.showerror("Error", "No se puede agendar una cita antes de la fecha y hora actuales.")
        if self.existe_cita(fecha, hora):
            messagebox.showerror("Error", "Ya existe una cita en esa fecha y hora.")
            return

        nueva_cita = Cita(paciente, especialidad, nombre_medico, fecha, hora) #Juntar las variables necearias para crear una nueva cita
        self.usuario.citas.append(nueva_cita)
        self.actualizar_lista_citas()
        messagebox.showinfo("Éxito", "Cita agendada correctamente.")

    def eliminar_cita(self): #Método para eliminar una cita
        seleccion = self.citas_listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione una cita para eliminar.")
            return

        self.usuario.citas.pop(seleccion[0])
        self.actualizar_lista_citas()
        messagebox.showinfo("Eliminado", "La cita ha sido eliminada correctamente.")

    def cerrar_sesion(self): #Método para cerrar cesión
        self.master.show_iniciar_sesion()

if __name__ == "__main__": #If que permite el funcionamiento de la aplicación con su respectiva interfaz gráfica
    app = AppCitasMedicas()
    app.mainloop()
