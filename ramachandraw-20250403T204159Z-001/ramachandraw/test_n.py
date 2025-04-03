
import math

# Lista de valores pequeños a evaluar
valores = [1e-9,1.48e-9, 5e-8, 3e-7, 2e-6, 1e-5, 5e-4, 2e-3]

# Función para clasificar por magnitud
def clasificar_por_magnitud(valores):
    # Diccionario para almacenar los resultados por magnitud
    clasificacion = {}
    
    for valor in valores:
        if valor > 0:
            # Obtener el exponente (orden de magnitud) del valor
            magnitud = math.floor(math.log10(valor))
            print (magnitud)
            
            # Crear una lista para cada magnitud
            if magnitud not in clasificacion:
                clasificacion[magnitud] = []
            
            # Agregar el valor a su respectiva magnitud
            clasificacion[magnitud].append(valor)
    
    return clasificacion

# Clasificar los valores
resultados = clasificar_por_magnitud(valores)

# Imprimir los resultados
for magnitud, numeros in resultados.items():
    print(f"Valores en el rango de 10^{magnitud}: {numeros}")
