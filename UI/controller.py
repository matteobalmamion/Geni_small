import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.clean()
        self._min, self._max=self._model.create_graph()
        nodes,edge=self._model.describeGrpah()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {len(nodes)} Numero di archi: {len(edge)}"))
        self._view.txt_result.controls.append(ft.Text(f"Informazioni sui pesi degli archi - valore minimo: {self._min[2]} e valore massimo {self._max[2]}"))
        self._view.update_page()

    def handle_countedges(self, e):
        try:
            self._soglia=float(self._view.txt_name.value)
        except ValueError:
            self._view.txt_result2.controls.append(ft.Text("Errore, inserire un valore numerico"))
            self._view.update_page()
            return
        if self._soglia <self._min[2] or self._soglia>self._max[2]:
            self._view.txt_result2.controls.append(ft.Text("Errore, inserire un valore numerico all'interno della soglia"))
            self._view.update_page()
            return
        minori,maggiori,uguali=self._model.searchEdges(self._soglia)
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso maggiore della soglia: {len(maggiori)}"))

        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso minore della soglia: {len(minori)}"))

        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso uguale della soglia: {len(uguali)}"))
        self._view.update_page()
    def handle_search(self, e):
        path=self._model.getPath(self._soglia)