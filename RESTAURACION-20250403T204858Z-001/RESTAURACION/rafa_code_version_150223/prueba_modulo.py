from lib import Molecule, MolecularPlanarity, damGen, log2, HomoLumo

mol = Molecule("y18-F-iso2-HSE-6311G.xyz")
mol.graph()



planarity = MolecularPlanarity("y18-Cl-simplif-HSE-TD-6311G.xyz")
planarity.planarity()
print("SPD:{} MPP:{}".format(planarity.SPD_round,  planarity.MPP_round))


labels=['molecula','otra molecula','prueba','algo mas','molecula final','La que sea']
accep = [6.5,6.9,6.5,6.9,7.8,4.7]
donor = [4.2,4.5,4.6,3.5,2.1,3.5]

dam = damGen(accep, donor, labels)
dam.show()



com=log2("y18-Br-iso2-HSE-6311G.log")
com.convert("xyz")



Gap = HomoLumo("y18-Br-iso2-HSE-6311G.log")
Gap.calculate()
print(Gap.Show())


