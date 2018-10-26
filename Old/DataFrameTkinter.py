from tkinter import *
from pandastable import Table


class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, dataFrame, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('1920x700+00+00')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        self.table = pt = Table(f, dataframe=dataFrame,
                                showtoolbar=True, showstatusbar=True)
        pt.adjustColumnWidths(30)

        pt.show()
        return
