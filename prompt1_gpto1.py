import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Costanti fisiche
g = 9.81
rho = 1.225
Cd = 0.47   # coefficiente di drag (simile a una sfera, da variare)
A = 0.005   # area effettiva sezione freccia (m^2), da regolare
m = 0.02    # massa freccia (kg), da regolare
v_base = 30 # velocità di uscita "teorica" (m/s) prima delle perdite

# Parametri di "perdita" dell'arco e dell'elasticità (molto semplificato)
k_arco = 0.85       # efficienza arco (0-1)
k_elastic = 0.95    # perdita su elasticità freccia (0-1)

# Finestra Tkinter per controlli
root = tk.Tk()
root.title("Simulazione Tiro Freccia")

# Variabile per l'angolo di lancio (in gradi)
angle_var = tk.DoubleVar(value=45.0)

def update_angle(val):
    """Aggiorna l'angolo di lancio."""
    angle = angle_var.get()
    angle_label.config(text=f"Angolo di lancio: {angle:.1f}°")

def launch_simulation():
    angle_deg = angle_var.get()
    theta = np.radians(angle_deg)

    # Calcolo velocità iniziale reale tenendo conto delle perdite
    v0 = v_base * k_arco * k_elastic

    # Tempo di simulazione e step
    t_max = 5.0
    dt = 0.01
    t_points = np.arange(0, t_max, dt)

    # --- Traiettoria teorica ---
    x_theo = v0 * np.cos(theta) * t_points
    y_theo = v0 * np.sin(theta) * t_points - 0.5 * g * t_points**2

    # --- Traiettoria reale (integrazione numerica con attrito) ---
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)

    x, y = [0], [0]  # posizione iniziale

    for i in range(1, len(t_points)):
        v = np.sqrt(vx**2 + vy**2)

        # Forza di drag
        F_drag = 0.5 * Cd * rho * A * v**2

        # Direzione della velocità
        drag_x = -(F_drag/m) * (vx / v)
        drag_y = -(F_drag/m) * (vy / v)

        # Aggiorno velocità
        vx = vx + (drag_x) * dt
        vy = vy - g * dt + (drag_y) * dt

        # Aggiorno posizione
        x.append(x[-1] + vx*dt)
        y.append(y[-1] + vy*dt)

        # Se la freccia tocca il suolo, interrompo
        if y[-1] <= 0:
            break

    # Plot con matplotlib
    plt.figure(figsize=(7,5))
    plt.plot(x_theo, y_theo, 'r--', label='Teorica (no attrito)')
    plt.plot(x, y, 'b-', label='Reale (con attrito)')
    plt.title(f"Tiro con angolo = {angle_deg:.1f}°")
    plt.xlabel("Distanza (m)")
    plt.ylabel("Altezza (m)")
    plt.legend()
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.show()

# Label e slider per l'angolo
angle_label = tk.Label(root, text=f"Angolo di lancio: {angle_var.get()}°")
angle_label.pack(pady=5)

angle_scale = tk.Scale(root, from_=0, to=90, orient=tk.HORIZONTAL,
                       variable=angle_var, resolution=1.0,
                       command=update_angle)
angle_scale.pack(pady=5)

# Pulsante per lanciare la simulazione
launch_button = tk.Button(root, text="Lancia Freccia", command=launch_simulation)
launch_button.pack(pady=10)

root.mainloop()
