import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceNode=None


    def handle_graph(self, e):
        self._view.txt_result.clean()
        self._model.createGraph()
        nodes,edges=self._model.descriviGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {len(nodes)} nodi e {len(edges)} archi"))
        listDD = map(lambda x: ft.dropdown.Option(data=x,
                                                  text=x,
                                                  on_click=self.getSelectedNode), nodes)
        self._view.ddLocalizzazione.options.extend(listDD)
        self._view.update_page()
    def getSelectedNode(self,e):
        print("getSelectedNode called")
        if e.control.data is None:
            self._choiceNode = None
        else:
            self._choiceNode = e.control.data
        print(self._choiceNode)
    def handle_statistiche(self, e):
        self._view.txt_result2.clean()
        if self._choiceNode==None:
            self._view.txt_result2.controls.append(ft.Text("Errore, selezionare un tipo"))
            self._view.update_page()
            return
        connection=self._model.getConnected(self._choiceNode)
        self._view.txt_result2.controls.append(ft.Text(f"adiacenti a: {self._choiceNode}"))
        for c in connection:
            self._view.txt_result2.controls.append(ft.Text(f"{c[0]}: {c[1]}"))
        self._view.update_page()

    def handle_search(self, e):
        self._view.txt_result3.clean()
        if self._choiceNode==None:
            self._view.txt_result3.controls.append(ft.Text("Errore, selezionare un tipo"))
            self._view.update_page()
            return
        path, cost=self._model.search_path(self._choiceNode)
        self._view.txt_result3.controls.append(ft.Text(f"Trovato percorso di lunghezza: {cost}"))
        for p in path:
            self._view.txt_result3.controls.append(ft.Text(f"{p[0]} --> {p[1]}: costo {p[2]}"))
        self._view.update_page()