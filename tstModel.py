from model.model import Model

myModel=Model()
min,max=myModel.create_graph()
nodes,edges=myModel.describeGrpah()

minori,maggiori ,uguali=myModel.searchEdges(3)

path, cost=myModel.searchPath(3)
print(path)
print(cost)