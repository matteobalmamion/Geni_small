from model.model import Model

myModel=Model()
myModel.createGraph()
node,edge=myModel.descriviGrafo()
print(len(node))
print(len(edge))
path,cost=myModel.search_path("golgi")
print(path)
print(cost)