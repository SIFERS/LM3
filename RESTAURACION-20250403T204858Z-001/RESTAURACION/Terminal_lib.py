from lib import Molecule, MolecularPlanarity, damGen, log2, HomoLumo

from sys import argv


func = argv [1]
file = argv [2]
try:
  option = argv [3]
  
except IndexError() :
    option = ""


if (func == "1"):
    
    mol = Molecule(file)
    mol.graph()

elif (func == "2"):

    planarity = MolecularPlanarity(file)
    planarity.planarity()
    print("SPD:{} MPP:{}".format(planarity.SPD_round,  planarity.MPP_round))
    
elif (func == "3"):
    com=log2(file)
    com.convert(option)
    
elif (func == "4"):
    Gap = HomoLumo(file)
    Gap.calculate()
    print(Gap.Show())
    