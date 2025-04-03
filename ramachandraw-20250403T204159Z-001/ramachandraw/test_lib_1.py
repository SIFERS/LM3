
import numpy as np
from ramachandraw.parser import get_phi_psi
from ramachandraw.utils import fetch_pdb, plot

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D




# PDB id
pdb_id = "1mbn"

plot(fetch_pdb(pdb_id), cmap="viridis", alpha=0.75, dpi=100, save=True, show=False, filename="plot.png")
# Draw the Ramachandran plot
plot,density_map = plot(fetch_pdb(pdb_id))

# Generate a dictionary to store the (phi, psi) torsion angles
torsion_angles = get_phi_psi(fetch_pdb(pdb_id))


# Definir los límites permitidos para el mapa de densidad (esto depende de tus datos)
density_threshold = 1.487e-04  # Este es un valor de ejemplo; debes ajustarlo según sea necesario

# Función para verificar si los ángulos están dentro del área permitida
def verificar_angulos_en_mapa(torsion_angles, density_map, threshold):
    resultados = {}
    
    for residuo, angulos in torsion_angles.items():
        phi, psi = angulos
        # Convertir los ángulos en índices válidos para el mapa de densidad
        # Aquí asumo que los ángulos están en grados y deben escalarse a los índices de la matriz
        # Ajusta el siguiente código según el rango de tu mapa de densidad
        
        # Convertir ángulos negativos a positivos si es necesario
        phi_idx = int((phi + 180) / 360 * density_map.shape[0]) % density_map.shape[0]
        psi_idx = int((psi + 180) / 360 * density_map.shape[1]) % density_map.shape[1]
        
        # Verificar el valor en el mapa de densidad
        densidad = density_map[phi_idx, psi_idx]
        dentro_area = densidad > threshold
        
        resultados[residuo] = {
            'Ángulos': (phi, psi),
            'Densidad': densidad,
            'Dentro del área permitida': dentro_area
        }
    
    return resultados

# Llamar a la función para verificar los ángulos
resultados_verificacion = verificar_angulos_en_mapa(torsion_angles, density_map, density_threshold)

# Mostrar los resultados
"""
for residuo, resultado in resultados_verificacion.items():
    print(f"Residuo: {residuo}")
    print(f"  Ángulos: {resultado['Ángulos']}")
    print(f"  Densidad: {resultado['Densidad']}")
    print(f"  Dentro del área permitida: {resultado['Dentro del área permitida']}")


"""

# Ajustar el código para que la entrada sea una matriz z y los planos xy vayan de -180 a 180


#density_map *= 10e08
# Crear una matriz con las alturas de los puntos (z)
z = np.array(density_map)


# Crear una malla de puntos en el plano xy
x = np.linspace(-180, 180, z.shape[0])
y = np.linspace(-180, 180, z.shape[1])
x, y = np.meshgrid(x, y)

# Crear una figura y un eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definir los límites de magnitudes de 10
magnitudes = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]

# Crear una lista de colores para cada rango
colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'cyan', 'magenta']

# Graficar los valores en diferentes colores basados en su magnitud
for i in range(len(magnitudes)-1):
    # Crear una máscara para los valores en el rango actual
    mask = (z >= magnitudes[i]) & (z < magnitudes[i+1])
    ax.plot_surface(x, y, np.where(mask, z, np.nan), color=colors[i], alpha=0.8)

# Añadir una barra de colores (opcional, para visualización)
# Nota: La barra de colores no reflejará los valores exactos, ya que los colores se asignan manualmente
#fig.colorbar(ax.plot_surface(x, y, np.nan, color='blue', alpha=0.8), ax=ax, shrink=0.5, aspect=5)

# Etiquetas de los ejes
ax.set_xlabel('Eje X (-180 a 180)')
ax.set_ylabel('Eje Y (-180 a 180)')
ax.set_zlabel('Altura Z')

# Mostrar la gráfica

"""
# Crear una malla de puntos en el plano xy
x = np.linspace(-180, 180, z.shape[0])
y = np.linspace(-180, 180, z.shape[1])
x, y = np.meshgrid(x, y)

# Crear una figura y un eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definir los límites de magnitudes de 10
magnitudes = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'cyan', 'magenta']

# Graficar los valores en diferentes colores basados en su magnitud
for i in range(len(magnitudes)-1):
    mask = (z >= magnitudes[i]) & (z < magnitudes[i+1])
    ax.plot_surface(x, y, np.where(mask, z, np.nan), color=colors[i], alpha=0.8)

# Añadir contornos para resaltar los cambios en magnitudes
# Los contornos se dibujan en 2D para resaltar las transiciones de una magnitud a otra
ax.contour(x, y, z, levels=magnitudes, colors='black', linestyles='solid')

# Ajustar los límites del eje Z
ax.set_zlim(np.min(z), np.max(z))

# Etiquetas de los ejes
ax.set_xlabel('Eje X (-180 a 180)')
ax.set_ylabel('Eje Y (-180 a 180)')
ax.set_zlabel('Altura Z')
"""
# Mostrar la gráfica
plt.show()