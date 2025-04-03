from molecule_lib import open_file_xyz, Molecule

file = open_file_xyz("y18-Cl-simplif-HSE-TD-6311G.xyz")
file2 = open_file_xyz("pm6-1-unit-opt-HSE-TD-6311G.xyz")
mol = Molecule(file2)
mol.graph()

