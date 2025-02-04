import tkinter as tk
import math

# Costanti fisiche e parametri della simulazione
g = 9.81         # Accelerazione di gravità (m/s^2)
dt = 0.02        # Passo temporale (s)
m = 0.1          # Massa della freccia (kg)
k = 0.02         # Fattore di attrito (drag); da regolare in base al modello

# Parametri per la rappresentazione grafica
scale = 5           # 1 metro corrisponde a 5 pixel
canvas_width = 800
canvas_height = 600
origin_x = 50       # Origine per la x (in pixel)
origin_y = canvas_height - 50  # Origine per la y (in pixel)

def to_canvas_coords(x, y):
    """
    Converte le coordinate fisiche (in metri) in coordinate canvas (in pixel).
    Nota: l'asse y viene capovolto (y=0 in basso).
    """
    return origin_x + x * scale, origin_y - y * scale

class SimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulazione Tiro Freccia")
        
        # Canvas per il disegno
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(side=tk.TOP)
        
        # Frame dei controlli
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.BOTTOM)
        
        # Controllo per l'inclinazione dell'arco (in gradi)
        tk.Label(control_frame, text="Inclinazione Arco (°)").grid(row=0, column=0)
        self.bow_inclination_var = tk.DoubleVar(value=0)
        self.bow_inclination_scale = tk.Scale(control_frame, variable=self.bow_inclination_var,
                                              from_=-45, to=45, orient=tk.HORIZONTAL)
        self.bow_inclination_scale.grid(row=0, column=1)
        
        # Controllo per l'angolo di lancio (in gradi)
        tk.Label(control_frame, text="Angolo di Lancio (°)").grid(row=1, column=0)
        self.launch_angle_var = tk.DoubleVar(value=45)
        self.launch_angle_scale = tk.Scale(control_frame, variable=self.launch_angle_var,
                                           from_=0, to=90, orient=tk.HORIZONTAL)
        self.launch_angle_scale.grid(row=1, column=1)
        
        # Controllo per la velocità iniziale (in m/s)
        tk.Label(control_frame, text="Velocità Iniziale (m/s)").grid(row=2, column=0)
        self.initial_speed_var = tk.DoubleVar(value=50)
        self.initial_speed_scale = tk.Scale(control_frame, variable=self.initial_speed_var,
                                            from_=10, to=100, orient=tk.HORIZONTAL)
        self.initial_speed_scale.grid(row=2, column=1)
        
        # Pulsante per avviare la simulazione
        self.launch_button = tk.Button(control_frame, text="Lancia", command=self.start_simulation)
        self.launch_button.grid(row=3, column=0, columnspan=2)
        
        # Stato della simulazione
        self.simulation_running = False
        self.actual_trajectory = []       # Lista dei punti della traiettoria reale
        self.theoretical_trajectory = []  # Lista dei punti della traiettoria teorica
        
    def start_simulation(self):
        """Inizializza i parametri e pre-computa la traiettoria teorica, poi avvia l'animazione."""
        # Pulizia del canvas
        self.canvas.delete("all")
        self.simulation_running = True
        
        # Lettura dei parametri impostati
        bow_inclination = self.bow_inclination_var.get()  # in gradi
        launch_angle = self.launch_angle_var.get()        # in gradi
        initial_speed = self.initial_speed_var.get()      # in m/s
        
        # Calcolo dell'efficienza: si assume che la velocità efficace sia massima a 0°.
        # (Si usa cos(inclinazione) – vedi ad es. trattamenti semplificati sull'energia elastica)
        efficiency = math.cos(math.radians(bow_inclination))
        effective_speed = initial_speed * efficiency
        
        # Calcolo dei componenti iniziali della velocità per la freccia reale
        theta = math.radians(launch_angle)
        self.vx = effective_speed * math.cos(theta)
        self.vy = effective_speed * math.sin(theta)
        
        # Posizione iniziale (metri)
        self.x = 0
        self.y = 0
        
        # Pre-calcolo della traiettoria teorica (senza attrito)
        self.theoretical_trajectory = []
        t = 0
        while True:
            x_theo = initial_speed * math.cos(theta) * t
            y_theo = initial_speed * math.sin(theta) * t - 0.5 * g * t**2
            if y_theo < 0:
                break
            self.theoretical_trajectory.append((x_theo, y_theo))
            t += dt
        
        # Disegno della traiettoria teorica come linea tratteggiata in rosso
        if len(self.theoretical_trajectory) > 1:
            points = []
            for (xt, yt) in self.theoretical_trajectory:
                cx, cy = to_canvas_coords(xt, yt)
                points.extend([cx, cy])
            self.canvas.create_line(points, fill="red", dash=(4, 2))
        
        # Inizializzazione della traiettoria reale
        self.actual_trajectory = [(self.x, self.y)]
        
        # Avvio del loop di animazione
        self.update_simulation()
        
    def update_simulation(self):
        """Aggiorna la posizione e la velocità della freccia integrando le equazioni del moto."""
        if not self.simulation_running:
            return
        
        # Calcolo della velocità (modulo)
        v = math.sqrt(self.vx**2 + self.vy**2)
        
        # Accelerazioni:
        # - La componente x è influenzata solo dall'attrito: a_x = - (k/m) * v * vx
        # - La componente y è influenzata dalla gravità e dall'attrito: a_y = -g - (k/m) * v * vy
        ax = - (k/m) * v * self.vx
        ay = -g - (k/m) * v * self.vy
        
        # Aggiornamento delle velocità (in m/s)
        self.vx += ax * dt
        self.vy += ay * dt
        
        # Aggiornamento della posizione (in m)
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Aggiungi il nuovo punto alla traiettoria reale se sopra il suolo
        if self.y >= 0:
            self.actual_trajectory.append((self.x, self.y))
        else:
            self.simulation_running = False  # Termina la simulazione quando la freccia colpisce il suolo
        
        # Pulizia e ridisegno dell'animazione (tag "arrow" per gli oggetti aggiornabili)
        self.canvas.delete("arrow")
        
        # Disegna la traiettoria reale come linea blu
        if len(self.actual_trajectory) > 1:
            points = []
            for (xa, ya) in self.actual_trajectory:
                cx, cy = to_canvas_coords(xa, ya)
                points.extend([cx, cy])
            self.canvas.create_line(points, fill="blue", tags="arrow")
        
        # Disegna la freccia (rappresentata come un piccolo cerchio nero)
        cx, cy = to_canvas_coords(self.x, self.y)
        r = 5  # raggio in pixel
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black", tags="arrow")
        
        # Programma il prossimo aggiornamento se la simulazione è ancora attiva
        if self.simulation_running:
            self.master.after(int(dt*1000), self.update_simulation)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
