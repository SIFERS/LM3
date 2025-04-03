class Graph:

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

    def __init__(self,file):
        self.text = ""
        self.file = file
        self.words_list = ""
        self.ordered_values = ""
        self.result_dict = ""
        self.index_word = ""
        self.additional_data = ""
        self.to_graph = ""
        self.sort_atoms = ""
        self.ticks = ""
        self.sections= ""
        self.section_averages = ""
        self.overall_average_sections = ""
        self.overall_average_raw = ""

        

    def open_file(self):
        with open(self.file, 'r') as file:
            self.text = file.read()

    def test(self):
        print(self.text)

    def expand_range(self,value):
        """Expande un intervalo dado como '885-890' a una lista de números consecutivos."""
        if '-' in value:
            start, end = map(int, value.split('-'))
            return list(range(start, end + 1))
        else:
            return [int(value)]  # Retorna un solo valor como una lista

    def obtener_primeros_valores(self,lista_de_listas):
        # Obtener el primer valor de cada lista, asegurándose de que la lista no esté vacía
        primeros_valores = [sublista[0] for sublista in lista_de_listas if sublista]
        return primeros_valores

    def process_text(self):
        text = self.text
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
                        word_values.extend(self.expand_range(v))  # Expande los rangos en números consecutivos
                    values_list.append(word_values)  # Esta lista será una lista de listas
                    index_word = self.obtener_primeros_valores(values_list)        

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
        self.words_list = words_list
        self.ordered_values = ordered_values
        self.result_dict = dictionary
        self.index_word = index_word
        self.additional_data = additional_data

    def sort_values(self):
        values = self.result_dict
        index = self.ordered_values
        atoms = self.additional_data
        valuesToGraph = []
        sort_atoms = []
        for x in index:
            valuesToGraph.append(values.get(x))
            sort_atoms.append(atoms[x-1])

        self.to_graph = valuesToGraph
        self.sort_atoms = sort_atoms

    def get_ticks(self):


        idex = self.ordered_values
        markers = self.index_word
        sections = []
        puntos_medios = []
        for x in markers:
            sections.append(idex.index(x))
        sections.append(len(idex))

        # Iterar sobre los valores para obtener los puntos medios entre cada par consecutivo
        for i in range(1, len(sections)):
            punto_medio = (sections[i - 1] + sections[i]) / 2
            puntos_medios.append(punto_medio)    
        self.ticks =puntos_medios
        self.sections = sections       

    def calculate_averages(self):
        values = self.to_graph
        sections = self.sections
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
        
        self.section_averages = section_averages
        self.overall_average_sections = overall_average_sections
        self.overall_average_raw = overall_average_raw

    def show_average(self):
        print("\n\t\t\tAverage values for each section:")
        print("-" * 70)
        total_values = 0
        for i in range(len(self.section_averages)):
            start = self.sections[i]
            end =self. sections[i+1]
            n_values = end - start
            total_values += n_values
            print(f"Section '{self.words_list[i]}' ({n_values} values): {self.section_averages[i]:.6f} kcal/mol")
        print("-" * 70)
        print(f"Overall average (average of section averages): {self.overall_average_sections:.6f} kcal/mol")
        print(f"Overall average (from all {total_values} raw values): {self.overall_average_raw:.6f} kcal/mol")
        print("\nNote:\nThe difference occurs because first method gives equal weight to each section,")
        print("while the second method weights each value equally, regardless of its section.\n")
        print("-" * 70)

    def calculate(self):
        self.open_file()
        self.process_text()
        self.sort_values()
        self.get_ticks()
        self.calculate_averages()
        self.show_average()
