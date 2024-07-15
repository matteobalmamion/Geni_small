import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._nMin=0

    def handle_graph(self, e):
        self._view.txt_result.clean()
        self._model.create_graph()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumberOfNodes()} Numero di archi: {self._model.getNumberOfEdges()}"))
        self._view.txt_result.controls.append(ft.Text(
            f"Informazioni sui pesi degli archi: Peso minimo: {self._model.getMinEdge()} Numero di archi: {self._model.getMaxEdge()}"))
        self._view.update_page()
    def handle_countedges(self, e):
        self._view.txt_result2.clean()
        try:
            self._nMin=float(self._view.txt_name.value)
        except ValueError:
            self._view.txt_result2.controls.append(ft.Text(
                f"Errore, inserire un numero"))
            self._view.update_page()
            return
        min,max,ug=self._model.countEdges(self._nMin)
        self._view.txt_result2.controls.append(ft.Text(
            f"Numero di archi con peso maggiore della soglia: {max}"))

        self._view.txt_result2.controls.append(ft.Text(
            f"Numero di archi con peso minore della soglia: {min}"))

        self._view.txt_result2.controls.append(ft.Text(
            f"Numero di archi con peso uguale alla soglia: {ug}"))
        self._view.update_page()

    def handle_search(self, e):

        self._model.search_path(self._nMin)
        self._view.txt_result3.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.computeWeightPath(self._model._solBest))}"))
        path=self._model.getSolBest()
        for edge in path:
            self._view.txt_result3.controls.append(ft.Text(f"{edge[0]} --> {edge[1]}: {edge[2]}"))
        self._view.update_page()