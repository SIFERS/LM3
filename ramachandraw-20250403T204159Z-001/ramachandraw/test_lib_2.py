import numpy as np
import matplotlib.pyplot as plt

# Ejemplo de los ángulos de torsión (reemplaza con tus valores)
torsion_angles = {
    'A:LEU2': [-45.79, 133.57],
    'A:SER3': [-49.57, 150.06],
    'A:GLU4': [-45.41, -59.95],
    'A:GLY5': [-50.40, -55.19],
    # Añade más ángulos según sea necesario
}

# Ejemplo del mapa de densidad (reemplaza con tus valores)
density_map = np.array([
    [6.18e-07, 1.21e-06, 1.73e-06],
    [9.03e-07, 1.65e-06, 2.25e-06],
    [1.13e-06, 1.93e-06, 2.53e-06],
    [2.42e-06, 4.86e-06, 8.21e-06]
    # Agrega más filas aquí según tu mapa de densidad
])

# Definir los límites permitidos para el mapa de densidad
density_threshold = 1e-06  # Este es un valor de ejemplo; ajústalo según sea necesario

# Función para verificar si los ángulos están dentro del área permitida
def verificar_angulos_en_mapa(torsion_angles, density_map, threshold):
    resultados = []
    
    # Recorremos cada residuo y sus ángulos
    for residuo, angulos in torsion_angles.items():
        # Aquí extraemos phi y psi de los ángulos de torsión
        phi, psi = angulos  # 'angulos' es una lista o tupla con [phi, psi]

        # Convertir ángulos en índices válidos para el mapa de densidad
        # Estos índices se calculan para el acceso a la matriz density_map
        phi_idx = int((phi + 180) / 360 * density_map.shape[0]) % density_map.shape[0]
        psi_idx = int((psi + 180) / 360 * density_map.shape[1]) % density_map.shape[1]
        
        # Verificar el valor en el mapa de densidad
        densidad = density_map[phi_idx, psi_idx]
        dentro_area = densidad > threshold
        
        # Guardar los resultados de verificación
        resultados.append((phi, psi, dentro_area, residuo))
    
    return resultados

# Verificar los ángulos
resultados_verificacion = verificar_angulos_en_mapa(torsion_angles, density_map, density_threshold)

# Generar la gráfica de los ángulos
plt.figure(figsize=(8, 6))

# Separar los puntos que están dentro y fuera del área permitida
dentro_phi = [phi for phi, psi, dentro, res in resultados_verificacion if dentro]
dentro_psi = [psi for phi, psi, dentro, res in resultados_verificacion if dentro]
fuera_phi = [phi for phi, psi, dentro, res in resultados_verificacion if not dentro]
fuera_psi = [psi for phi, psi, dentro, res in resultados_verificacion if not dentro]

# Graficar los puntos
plt.scatter(dentro_phi, dentro_psi, color='green', label='Dentro del área permitida', s=100, marker='o')
plt.scatter(fuera_phi, fuera_psi, color='red', label='Fuera del área permitida', s=100, marker='x')

# Etiquetas de los residuos
for phi, psi, dentro, residuo in resultados_verificacion:
    plt.text(phi, psi, residuo, fontsize=9, ha='right')

# Configurar los límites de los ejes y etiquetas
plt.xlim([-180, 180])
plt.ylim([-180, 180])
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel("Phi (°)")
plt.ylabel("Psi (°)")
plt.title("Gráfica de Ángulos de Torsión (Phi, Psi)")
plt.legend()

# Mostrar la gráfica
plt.grid(True)
plt.show()
