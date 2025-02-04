import tkinter as tk
import math

# Costanti fisiche e parametri della simulazione
g = 9.81         # Accelerazione di gravità (m/s^2)
dt = 0.02        # Passo temporale (s)
m = 0.1          # Massa della freccia (kg)
k = 0.02         # Coefficiente di attrito (drag)
# La velocità iniziale sarà ora parametrica (in m/s)

# Parametri per la rappresentazione grafica
scale_factor = 5           # 1 metro corrisponde a 5 pixel
canvas_width = 800
canvas_height = 600
origin_x = 50              # Origine in x (in pixel)
origin_y = canvas_height - 50  # Origine in y (in pixel)

def to_canvas_coords(x, y):
    """
    Converte coordinate fisiche (in metri) in coordinate canvas (in pixel).
    Nota: l'asse y viene capovolto (y=0 in basso).
    """
    return origin_x + x * scale_factor, origin_y - y * scale_factor

class SimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulazione Tiro Freccia")
        
        # Layout: frame dei controlli a sinistra, canvas a destra
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # Variabili per i parametri
        self.bow_inclination_var = tk.DoubleVar(value=0)   # Inclinazione arco in gradi
        self.launch_angle_var = tk.DoubleVar(value=45)       # Angolo di lancio in gradi
        self.initial_speed_var = tk.DoubleVar(value=50)      # Velocità iniziale in m/s
        
        # Creazione dei controlli
        tk.Label(self.control_frame, text="Parametri", font=("Arial", 14)).pack(pady=5)
        
        tk.Label(self.control_frame, text="Inclinazione Arco (°)").pack()
        self.bow_inclination_scale = tk.Scale(self.control_frame, variable=self.bow_inclination_var,
                                              from_=-45, to=45, orient=tk.HORIZONTAL,
                                              command=self.update_preview)
        self.bow_inclination_scale.pack()
        
        tk.Label(self.control_frame, text="Angolo di Lancio (°)").pack()
        self.launch_angle_scale = tk.Scale(self.control_frame, variable=self.launch_angle_var,
                                           from_=0, to=90, orient=tk.HORIZONTAL,
                                           command=self.update_preview)
        self.launch_angle_scale.pack()
        
        tk.Label(self.control_frame, text="Velocità Iniziale (m/s)").pack()
        self.initial_speed_scale = tk.Scale(self.control_frame, variable=self.initial_speed_var,
                                            from_=10, to=100, orient=tk.HORIZONTAL,
                                            command=self.update_preview)
        self.initial_speed_scale.pack()
        
        self.launch_button = tk.Button(self.control_frame, text="Lancia", command=self.start_simulation)
        self.launch_button.pack(pady=10)
        
        # Stato della simulazione
        self.simulation_running = False
        self.actual_trajectory = []       # Punti della traiettoria reale
        self.theoretical_trajectory = []  # Punti della traiettoria teorica
        
        # Mostra subito il preview con i parametri iniziali
        self.update_preview()
    
    def update_preview(self, *args):
        """
        Aggiorna il preview della traiettoria teorica e la posizione iniziale ogni volta che
        viene modificato un parametro. Se la simulazione è in esecuzione non si aggiornano i preview.
        """
        if self.simulation_running:
            return
        
        # Rimuove eventuali preview precedenti
        self.canvas.delete("preview")
        
        # Legge i parametri correnti
        bow_inclination = self.bow_inclination_var.get()   # gradi
        launch_angle = self.launch_angle_var.get()           # gradi
        initial_speed = self.initial_speed_var.get()         # m/s
        
        theta = math.radians(launch_angle)
        
        # Calcola la traiettoria teorica (senza attrito) utilizzando la velocità iniziale immessa.
        # Nota: in questo preview non consideriamo l'efficienza ridotta per inclinazione.
        trajectory = []
        t = 0
        while True:
            x_theo = initial_speed * math.cos(theta) * t
            y_theo = initial_speed * math.sin(theta) * t - 0.5 * g * t**2
            if y_theo < 0:
                break
            trajectory.append((x_theo, y_theo))
            t += dt
        
        if len(trajectory) > 1:
            points = []
            for (xt, yt) in trajectory:
                cx, cy = to_canvas_coords(xt, yt)
                points.extend([cx, cy])
            # Disegna la linea tratteggiata in rosso
            self.canvas.create_line(points, fill="red", dash=(4,2), tags="preview")
        
        # Disegna la posizione iniziale (freccia o piccolo cerchio in nero in (0,0))
        cx, cy = to_canvas_coords(0, 0)
        r = 5
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="black", tags="preview")
    
    def start_simulation(self):
        """
        Avvia la simulazione reale: pulisce il canvas, calcola la traiettoria teorica e
        integra le equazioni del moto con attrito, mostrando l'animazione.
        """
        # Pulisce il canvas (rimuove preview e eventuali tracciati precedenti)
        self.canvas.delete("all")
        self.simulation_running = True
        
        # Legge i parametri correnti
        bow_inclination = self.bow_inclination_var.get()   # gradi
        launch_angle = self.launch_angle_var.get()           # gradi
        initial_speed = self.initial_speed_var.get()         # m/s
        
        theta = math.radians(launch_angle)
        # Calcola l'efficienza: la velocità effettiva si riduce con l'inclinazione dell'arco
        efficiency = math.cos(math.radians(bow_inclination))
        effective_speed = initial_speed * efficiency
        
        # Componenti della velocità per la simulazione reale
        self.vx = effective_speed * math.cos(theta)
        self.vy = effective_speed * math.sin(theta)
        
        # Posizione iniziale in metri
        self.x = 0
        self.y = 0
        
        # Pre-calcola la traiettoria teorica (senza attrito) utilizzando la velocità iniziale
        self.theoretical_trajectory = []
        t = 0
        while True:
            x_theo = initial_speed * math.cos(theta) * t
            y_theo = initial_speed * math.sin(theta) * t - 0.5 * g * t**2
            if y_theo < 0:
                break
            self.theoretical_trajectory.append((x_theo, y_theo))
            t += dt
        
        # Disegna la traiettoria teorica come linea tratteggiata in rosso
        if len(self.theoretical_trajectory) > 1:
            points = []
            for (xt, yt) in self.theoretical_trajectory:
                cx, cy = to_canvas_coords(xt, yt)
                points.extend([cx, cy])
            self.canvas.create_line(points, fill="red", dash=(4,2))
        
        # Inizializza la traiettoria reale
        self.actual_trajectory = [(self.x, self.y)]
        
        # Avvia il loop di aggiornamento della simulazione
        self.update_simulation()
    
    def update_simulation(self):
        """Integra il moto della freccia e aggiorna l'animazione in tempo reale."""
        if not self.simulation_running:
            return
        
        # Calcola il modulo della velocità
        v = math.sqrt(self.vx**2 + self.vy**2)
        
        # Accelerazioni: attrito (drag) e gravità
        ax = - (k / m) * v * self.vx
        ay = -g - (k / m) * v * self.vy
        
        # Aggiorna le componenti della velocità e la posizione
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        if self.y >= 0:
            self.actual_trajectory.append((self.x, self.y))
        else:
            self.simulation_running = False  # Termina la simulazione se la freccia raggiunge il suolo
        
        # Aggiorna l'animazione: cancella gli elementi con tag "arrow" e ridisegna la traiettoria reale e la freccia
        self.canvas.delete("arrow")
        if len(self.actual_trajectory) > 1:
            points = []
            for (xa, ya) in self.actual_trajectory:
                cx, cy = to_canvas_coords(xa, ya)
                points.extend([cx, cy])
            self.canvas.create_line(points, fill="blue", tags="arrow")
        
        # Disegna la freccia attuale come un piccolo cerchio nero
        cx, cy = to_canvas_coords(self.x, self.y)
        r = 5
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="black", tags="arrow")
        
        # Programma il prossimo aggiornamento se la simulazione è ancora attiva
        if self.simulation_running:
            self.master.after(int(dt * 1000), self.update_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
