import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Costanti fisiche
g = 9.81  # accelerazione di gravità (m/s^2)

class FrecciaSimulatore(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulazione Tiro Freccia")

        # Parametri iniziali
        self.angle_deg = tk.DoubleVar(value=45.0)    # angolo di lancio in gradi
        self.velocity = tk.DoubleVar(value=30.0)     # velocità iniziale (m/s)
        
        # Layout generale: una frame di sinistra per i controlli, e una per il grafico
        self.left_frame = ttk.Frame(self, padding="10 10 10 10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.right_frame = ttk.Frame(self, padding="5 5 5 5")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Creo i controlli nella left_frame
        self.create_controls(self.left_frame)

        # Creo la figura matplotlib nella right_frame
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Disegno iniziale
        self.update_plot()

    def create_controls(self, container):
        # Slider per l'angolo
        ttk.Label(container, text="Angolo di lancio (°):").pack(pady=5)
        angle_scale = ttk.Scale(
            container, from_=0, to=90, orient=tk.HORIZONTAL,
            variable=self.angle_deg, command=lambda x: self.update_plot()
        )
        angle_scale.pack(fill=tk.X, padx=5)

        # Slider per la velocità iniziale
        ttk.Label(container, text="Velocità Iniziale (m/s):").pack(pady=5)
        velocity_scale = ttk.Scale(
            container, from_=5, to=100, orient=tk.HORIZONTAL,
            variable=self.velocity, command=lambda x: self.update_plot()
        )
        velocity_scale.pack(fill=tk.X, padx=5)

        # Pulsante per aggiornare “manualmente” (se preferisci)
        # In questo caso abbiamo già "update_plot()" dentro i command delle slider
        # ma se vuoi un pulsante dedicato puoi aggiungerlo:
        # 
        # update_button = ttk.Button(container, text="Aggiorna", command=self.update_plot)
        # update_button.pack(pady=10)

    def update_plot(self):
        # Pulisce l'axes
        self.ax.clear()

        # Legge i parametri
        angle = np.radians(self.angle_deg.get())
        v0 = self.velocity.get()

        # Genero un array di tempi
        # stimo un tempo massimo: tempo di volo approssimato con formula 2*v0*sin(theta)/g
        t_flight = 2 * v0 * np.sin(angle) / g  
        t = np.linspace(0, t_flight, 100)

        # Calcolo la traiettoria teorica (senza attrito)
        x_theo = v0 * np.cos(angle) * t
        y_theo = v0 * np.sin(angle) * t - 0.5 * g * t**2

        # Disegno la traiettoria teorica tratteggiata
        self.ax.plot(x_theo, y_theo, 'r--', label='Traiettoria Teorica')

        # Disegno la "freccia" (arrow) che mostra la direzione e l'intensità della velocità iniziale
        # Per comodità, la disegno partendo dall'origine (0,0).
        # dx, dy = lunghezza orizzontale/verticale
        arrow_length_scale = 0.2  # fattore per ridurre la freccia sul grafico
        dx = v0 * np.cos(angle) * arrow_length_scale
        dy = v0 * np.sin(angle) * arrow_length_scale

        self.ax.arrow(
            0, 0, dx, dy,
            width=0.02,  # spessore "fusto" della freccia
            head_width=0.5, head_length=0.5,  # dimensioni della punta
            length_includes_head=True,
            color='blue',
            label='Velocità Iniziale'
        )

        # Imposto i limiti dell’asse
        # Potrei farlo in base al range della traiettoria
        max_x = max(x_theo) * 1.1
        max_y = max(y_theo) * 1.1
        self.ax.set_xlim(0, max_x if max_x > 0 else 10)
        self.ax.set_ylim(0, max_y if max_y > 0 else 10)

        self.ax.set_xlabel("Distanza (m)")
        self.ax.set_ylabel("Altezza (m)")
        self.ax.set_title("Tiro con Freccia - Traiettoria Teorica")
        self.ax.legend()
        self.ax.grid(True)

        # Aggiorno il canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = FrecciaSimulatore()
    app.mainloop()
