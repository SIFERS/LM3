import argparse
import matplotlib.pyplot as plt
import warnings

# Suppress all warnings
warnings.filterwarnings('ignore')
try:
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['TeX Gyre Termes']  # O usa otra fuente serif que prefieras
    plt.rcParams['mathtext.fontset'] = 'cm'  # Para las ecuaciones en modo matemático
except Exception:
    pass  # Silently continue if font setting fails
    

elementos_quimicos = {
    1: ('H', '#FFFFFF'),   # Hidrógeno (Blanco)
    2: ('He', '#D9FFFF'),  # Helio (Cian)
    3: ('Li', '#CC80FF'),  # Litio (Violeta)
    4: ('Be', '#C2FF00'),  # Berilio (Verde claro)
    5: ('B', '#FFB5B5'),   # Boro (Rosa)
    6: ('C', '#909090'),   # Carbono (Gris oscuro)
    7: ('N', '#3050F8'),   # Nitrógeno (Azul)
    8: ('O', '#FF0D0D'),   # Oxígeno (Rojo)
    9: ('F', '#90E050'),   # Flúor (Verde claro)
    10: ('Ne', '#B3E3F5'), # Neón (Azul claro)
    11: ('Na', '#AB5CF2'), # Sodio (Púrpura)
    12: ('Mg', '#8AFF00'), # Magnesio (Verde)
    13: ('Al', '#BFA6A6'), # Aluminio (Gris claro)
    14: ('Si', '#F0C8A0'), # Silicio (Beige)
    15: ('P', '#FF8000'),  # Fósforo (Naranja)
    16: ('S', '#FFFF30'),  # Azufre (Amarillo)
    17: ('Cl', '#1FF01F'), # Cloro (Verde)
    18: ('Ar', '#80D1E3'), # Argón (Azul claro)
    19: ('K', '#8F40D4'),  # Potasio (Púrpura)
    20: ('Ca', '#3DFF00'), # Calcio (Verde)
    26: ('Fe', '#E06633'), # Hierro (Naranja oscuro)
    29: ('Cu', '#C88033'), # Cobre (Marrón)
    47: ('Ag', '#C0C0C0'), # Plata (Gris plata)
    79: ('Au', '#FFD123')  # Oro (Dorado)
}

def expand_range(value):
    """Expande un intervalo dado como '885-890' a una lista de números consecutivos."""
    if '-' in value:
        start, end = map(int, value.split('-'))
        return list(range(start, end + 1))
    else:
        return [int(value)]  # Retorna un solo valor como una lista
def obtener_primeros_valores(lista_de_listas):
    # Obtener el primer valor de cada lista, asegurándose de que la lista no esté vacía
    primeros_valores = [sublista[0] for sublista in lista_de_listas if sublista]
    return primeros_valores

def process_text(text):
    lines = text.strip().splitlines()
    
    words_list = []
    values_list = []
    index_word = []
    dictionary = {}
    additional_data = []
    
    parsing_dict = False
    parsing_additional_data = False
    current_key = 1
    
    for line in lines:
        line = line.strip()
        
        # Check for an empty line to switch between sections
        if not line:
            if not parsing_dict:
                parsing_dict = True
            else:
                parsing_additional_data = True
            continue
        
        if not parsing_dict:
            # Before empty line: Process key:value data, separate by commas
            if ':' in line:
                word, values = line.split(':')
                words_list.append(word.strip())
                word_values = []
                for v in values.split(','):
                    v = v.strip()
                    word_values.extend(expand_range(v))  # Expande los rangos en números consecutivos
                values_list.append(word_values)  # Esta lista será una lista de listas
                index_word = obtener_primeros_valores(values_list)        

        elif parsing_additional_data:
            # After second empty line: Parse the additional block of data
            columns = line.split()
            additional_data.extend(map(int, columns))
        
        else:
            # After first empty line: Parse two-column data
            columns = line.split()
            if len(columns) == 2:
                key = int(columns[0])
                try:
                    value = float(columns[1])  # Permitir decimales
                except ValueError:
                    value = 0  # Asigna un valor por defecto si no se puede convertir
                # Fill in any missing keys with value 0
                while current_key < key:
                    dictionary[current_key] = 0
                    current_key += 1
                
                # Add the actual key-value pair
                dictionary[key] = value
                current_key += 1
    
    # Crear una lista de valores en el orden de words_list
    ordered_values = []
    for word in words_list:
        # Asegurarse de que hay valores correspondientes
        if values_list:  # Si values_list no está vacío
            corresponding_values = values_list.pop(0)  # Extrae la lista de valores
            ordered_values.extend(corresponding_values)  # Añade esos valores a ordered_values

    return words_list, ordered_values, dictionary, index_word, additional_data

def sort_values(values, index,atoms):
    valuesToGraph = []
    sort_atoms = []
    for x in index:
        valuesToGraph.append(values.get(x))
        sort_atoms.append(atoms[x-1])

    return valuesToGraph,sort_atoms
def get_ticks(idex,markers):
    sections = []
    puntos_medios = []
    for x in markers:
        sections.append(idex.index(x))
    sections.append(len(idex))

    # Iterar sobre los valores para obtener los puntos medios entre cada par consecutivo
    for i in range(1, len(sections)):
        punto_medio = (sections[i - 1] + sections[i]) / 2
        puntos_medios.append(punto_medio)    
    return puntos_medios,sections    

def calculate_averages(values, sections):
    section_averages = []
    all_values = []
    
    # Calculate averages for each section with full precision
    for i in range(len(sections)-1):
        start = sections[i]
        end = sections[i+1]
        section_values = values[start:end]
        section_average = sum(section_values)/len(section_values)
        section_averages.append(section_average)
        all_values.extend(section_values)
    
    # Calculate both types of overall averages
    overall_average_sections = sum(section_averages)/len(section_averages)  # promedio de promedios
    overall_average_raw = sum(all_values)/len(all_values)  # promedio de todos los datos
    
    return section_averages, overall_average_sections, overall_average_raw

def main():
    # Argument parser para leer el archivo de entrada
    parser = argparse.ArgumentParser(description='Procesa un archivo de texto.')
    parser.add_argument('file', type=str, help='Ruta al archivo de texto')
    
    # Leer los argumentos de la línea de comandos
    args = parser.parse_args()
    file = args.file
    name = file.split('.')[0]

    # Abrir el archivo y leer su contenido
    with open(file, 'r') as file:
        text = file.read()

    # Procesar el contenido del archivo
    words_list, ordered_values, result_dict,index_word,additional_data= process_text(text)

    to_graph,sort_atoms = sort_values(result_dict,ordered_values,additional_data)
    ticks,sections = get_ticks(ordered_values,index_word)
    
    # Calculate averages
    section_averages, overall_average_sections, overall_average_raw = calculate_averages(to_graph, sections)

    # Print section averages and overall average
    print("\n\t\t\tAverage values for each section:")
    print("-" * 70)
    total_values = 0
    for i in range(len(section_averages)):
        start = sections[i]
        end = sections[i+1]
        n_values = end - start
        total_values += n_values
        print(f"Section '{words_list[i]}' ({n_values} values): {section_averages[i]:.6f} kcal/mol")
    print("-" * 70)
    print(f"Overall average (average of section averages): {overall_average_sections:.6f} kcal/mol")
    print(f"Overall average (from all {total_values} raw values): {overall_average_raw:.6f} kcal/mol")
    print("\nNote:\nThe difference occurs because first method gives equal weight to each section,")
    print("while the second method weights each value equally, regardless of its section.\n")
    print("-" * 70)
    # Imprimir los resultados
    #print("Words list:", words_list)
    #print("Index:", ordered_values)
    #print("Values:", result_dict)
    #print("Index Word:", index_word)
    #print("graph:", to_graph)
    #print(get_ticks(ordered_values,index_word))
    #print(additional_data)
    #print(sort_atoms)
    #print(len(ordered_values))
    #print(len(additional_data))
    


    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))

    # Asignar colores usando un bucle
    colores = [elementos_quimicos[numero_atomico][1] for numero_atomico in sort_atoms]

    # First plot section averages (to put them behind the bars)
    for i in range(len(section_averages)):
        start = sections[i]
        end = sections[i+1]
        plt.hlines(y=section_averages[i], xmin=start-0.5, xmax=end-0.5, 
                colors='#0064ff', linestyles='--', alpha=0.7, zorder=1,
                label='Section average' if i == 0 else "")

    # Plot overall average
    plt.hlines(y=overall_average_sections, xmin=-0.5, xmax=len(sort_atoms)-0.5, 
            colors='#ff0032', linestyles='--', alpha=0.8, zorder=1,
            label='Overall average')

    # Then plot the bars (they will be on top)
    ax.bar(range(len(to_graph)), to_graph, color=colores, edgecolor='black', zorder=2)

    # Etiqueta del eje Y
    plt.ylabel('ESP promedio (kcal/mol)', fontsize=16)
    plt.xlim(-1,len(sort_atoms))
    plt.yticks(fontsize=16)

    # Eliminar las etiquetas (ticks) del eje X
    plt.xticks(ticks,words_list,fontsize=16)  # No mostrar etiquetas en el eje X

    # Plot vertical section dividers
    for sec in sections[1:-1]: #ZNCG: lo modifique para que no imprima la primer y ultima linea vertical
        plt.axvline(x=sec-0.5, color='black', linestyle='--', linewidth=1)

    # Add legend
    plt.legend(fontsize=12)
    
    # Mostrar el gráfico
    plt.show()


if __name__ == "__main__":
    main()
