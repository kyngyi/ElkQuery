from tkinter import *
from tkinter import messagebox
import elasticsearch.exceptions
import Exceptions
from pandastable import Table
import DropCalendar
import AdvSearchWindow
import ElasticRequest
import DataFormatter


class Window(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    # Generates the popup pandastable, linked to dataframe
    def generate_table(self, dataframe):
        topframe = Toplevel()
        topframe.geometry('1920x1000+00+00')
        topframe.title('Table')
        table = Table(topframe, dataframe=dataframe,
                      showtoolbar=True, showstatusbar=True)
        table.show()

    def initUI(self):

        def advanced_options_click():
            topframe = Toplevel()
            topframe.geometry(root_settings(topframe))
            topframe.title('Advanced Search')
            AdvSearchWindow.AdvSearchWindow(topframe)

        def click():
            print("Event Triggered")

            # Initialise elasticsearch request handler passing Elasticsearch Address
            requestHandler = ElasticRequest.elasticRequest('http://10.2.5.21:9200')

            requestHandler.add_search_term(entry_box.get())
            try:
                r = requestHandler.send_request()
            except elasticsearch.exceptions.ConnectionError:
                print("Exception Catched!")
                messagebox.showerror("Error", "Connection Error, Unable to connect to server")
                return
            except Exceptions.noDataFoundError:
                print("No search results found!")
                messagebox.showerror("Error", "No Results found!")
                return
            # except Exception as e:
            #     messagebox.showerror("Error", "UNKNOWN ERROR")
            #     print(e)
            #     return
            data_formatter = DataFormatter.DataFormatter(r)
            to_display = data_formatter.get_display()
            self.generate_table(to_display)

        self.master.title("ELK")
        self.pack(fill=BOTH, expand=1)

        instruction = Label(self, text="Enter NRIC/ CAN")
        instruction.place(x=300, y=270)

        entry_id = StringVar()
        entry_box = Entry(self, textvariable=entry_id)
        entry_box.place(x=300, y=295)

        # instruction = Label(self, text="Additional Search Query (Optional)")
        # instruction.place(x=300, y=320)

        entry_id2 = "fck"
        # entry_box2 = Entry(self, textvariable=entry_id2)
        # entry_box2.place(x=300, y=345)

        adv_btn = Button(self, text="MORE OPTIONS", command=advanced_options_click)
        adv_btn.place(x=320, y=330)

        cfm_btn = Button(self, text="CONFIRM", command=click)
        cfm_btn.place(x=335, y=370)


def main():
    root = Tk()
    root.geometry(root_settings(root))
    app = Window()
    root.mainloop()


# Adjusts window size and initial window position, returns string for root.geometry
def root_settings(root):
    root.resizable(False, False)
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    return "%dx%d+%d+%d" % (w, h, x, y)


if __name__ == '__main__':
    main()
