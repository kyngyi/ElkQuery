import dropCalendar
import tkinter
from tkinter import messagebox
import elasticRequest
import elasticsearch
import exceptions
import DataFormatter
import pandastable
import StaticValues


class AdvSearchWindow():

    def __init__(self, frame):
        self.frame = frame
        self.initWindow()

    def generate_table(self, dataframe):
        topframe = tkinter.Toplevel()
        topframe.geometry('1920x1000+00+00')
        topframe.title('Table')
        table = pandastable.Table(topframe, dataframe=dataframe,
                      showtoolbar=True, showstatusbar=True)
        table.show()

    def initWindow(self):

        def click(event=None):


            # Initialise elasticsearch request handler passing Elasticsearch Address
            a = StaticValues.StaticValues()
            requestHandler = elasticRequest.elasticRequest(a.get_elasticsearch_server())

            # Check if queries are empty else add the queries to request body
            if self.check_if_empty(entry_box1.get(), entry_box2.get(), entry_box3.get(), entry_box4.get()):
                requestHandler.set_minimum_matches(0)
            else:
                requestHandler.add_search_term(entry_box1.get())
                requestHandler.add_search_term(entry_box2.get())
                requestHandler.add_search_term(entry_box2.get())
                requestHandler.add_search_term(entry_box3.get())
                requestHandler.add_search_term(entry_box4.get())

            # Checking logger checkbuttons
            is_adapter_selected = False
            for i in var:
                if var[i].get() != 0:
                    is_adapter_selected = True
                    requestHandler.add_logger_name(str(i))

            if not is_adapter_selected:
                print("Please select at least one adapter")
                messagebox.showerror("Error", "Please check at least one Program")
                return

            # Checking Max Results entry
            if self.contains_value((request_entry_box.get())):
                requestHandler.change_max_results((request_entry_box.get()))

            if self.contains_value(datepicker1.get()):
                requestHandler.set_from_date(datepicker1.get())

            if self.contains_value(datepicker2.get()):
                requestHandler.set_to_date(datepicker2.get())

            try:
                r = requestHandler.send_request()
            except elasticsearch.exceptions.ConnectionError:
                print("Exception Caught!")
                messagebox.showerror("Error", "Connection Error, Unable to connect to server")
                return
            except exceptions.noDataFoundError:
                print("No search results found!")
                messagebox.showerror("Error", "No Results found!")
                return
            except Exception as e:
                messagebox.showerror("Error", "UNKNOWN ERROR")
                print(e)
                return

            data_formatter = DataFormatter.DataFormatter(r)
            to_display = data_formatter.get_display()
            self.generate_table(to_display)

        datepicker1 = dropCalendar.Datepicker(self.frame)
        datepicker1.place(x=520, y=38)

        datepicker2 = dropCalendar.Datepicker(self.frame)
        datepicker2.place(x=520, y=85)

        datetext1 = tkinter.Label(self.frame, text="Date Range")
        datetext1.place(x=555, y=10)

        datetext2 = tkinter.Label(self.frame, text="From")
        datetext2.place(x=480, y=38)

        datetext3 = tkinter.Label(self.frame, text="To")
        datetext3.place(x=480, y=85)

        request_number_text = tkinter.Label(self.frame, text="Max Results:")
        request_number_text.place(x=480, y=130)

        request_entry_box = tkinter.Entry(self.frame)
        request_entry_box.config(width=5)
        request_entry_box.place(x=580, y=130)

        cfm_btn = tkinter.Button(self.frame, text="CONFIRM", command=click)
        cfm_btn.place(x=535, y=170)

        query_instruction = tkinter.Label(self.frame, text="Enter Queries!")
        query_instruction.place(x=230, y=40)

        entry_box1 = tkinter.Entry(self.frame)
        entry_box1.bind('<Return>', click)
        entry_box1.place(x=200, y=80)

        entry_box2 = tkinter.Entry(self.frame)
        entry_box2.bind('<Return>', click)
        entry_box2.place(x=200, y=115)

        entry_box3 = tkinter.Entry(self.frame)
        entry_box3.bind('<Return>', click)
        entry_box3.place(x=200, y=150)

        entry_box4 = tkinter.Entry(self.frame)
        entry_box4.bind('<Return>', click)
        entry_box4.place(x=200, y=185)

        serverList = ['ewalletproxy_server', 'fevoadapter_server', 'ltaewalletadapter', 'ntaadapter_server',
                      'ntamanager_server', 'trustadapter_server', 'umaadapter_server', 'walletservice_server']

        var = dict()
        # Load adapter_dict
        a = StaticValues.StaticValues()
        adapter_dict = a.get_adapter_dict()
        x = 0
        for i in serverList:
            var[i] = tkinter.IntVar()
            var[i].set(0)
            chk = tkinter.Checkbutton(self.frame, text=adapter_dict[i], variable=var[i], onvalue=1, offvalue=0)
            chk.grid(row=x ,column=0, ipadx=10, ipady=2)
            x += 1
            chk.toggle()

    # Checks if string that is passed in contains a value
    def contains_value(self, value):
        if value != "":
            return True
        else:
            return False

    # Checks if 4 strings passed in are empty
    def check_if_empty(self, string1, string2, string3, string4):
        if ((not self.contains_value(string1)) & (not self.contains_value(string2)) & (not self.contains_value(string3))
                & (not self.contains_value(string4))):
            return True
        else:
            return False


# Adjusts window size and initial window position, returns string for root.geometry
def root_settings(root):
    root.resizable(False, False)
    w = 800
    h = 300
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    return "%dx%d+%d+%d" % (w, h, x, y)


if __name__ =='__main__':
    root = tkinter.Tk()
    root.title('ELK Interface')
    root.geometry(root_settings(root))
    app = AdvSearchWindow(root)
    root.mainloop()
