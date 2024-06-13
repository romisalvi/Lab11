import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self.year=None
        self.color=None
        self.node=None

    def fillDD(self):
        for i in range(2015,2019):
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))
        self._listColor=self._model.getColors()
        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(str(c)))



    def handle_graph(self, e):
        self._view.txtOut.controls.clear()

        self.year=self._view._ddyear.value
        self.color=self._view._ddcolor.value
        if self.year=="" or self.color=="" or self.year is None or self.color is None:
            self._view.create_alert("Non hai scelto colore o anno")
            self._view.update_page()
            return
        self._model.creaGrafo(self.year,self.color)
        self._view.txtOut.controls.append(ft.Text(f"Grafo creato correttamente con {len(self._model.g.nodes)} nodi  e {len(self._model.g.edges)} sarchi! "))
        edges,nodirip=self._model.getPesanti()
        for e in edges:
            self._view.txtOut.controls.append(ft.Text(
                f"{e[0]}--->{e[1]}, peso = {e[2]}"))
        self._view.txtOut.controls.append(ft.Text(
            f"Nodi ripetuti:{nodirip}"))
        self.fillDDProduct()
        self._view.update_page()


        pass



    def fillDDProduct(self):
        self._view._ddnode.options.clear()
        for v in self._model.vertici:
            self._view._ddnode.options.append(ft.dropdown.Option(v.Product_number))



    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        self.node=self._view._ddnode.value
        if self.node=="" or self.node is None:
            self._view.create_alert("Non hai ancora selezionato un nodo source")
            self._view.update_page()
            return
        self._model.getBP(self.node)
        self._view.txtOut2.controls.append(ft.Text(f"numero di archi max: {self._model.lenMax}"))
        self._view.update_page()





        pass
