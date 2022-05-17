from tkinter import *
from tkinter.filedialog import askdirectory


class DemoApp:
    def __init__(self):
        self.root = Tk()
        self.root.title('DemoApp')
        # Label
        self.mylabel = Label(self.root, text='Hello', width=10)
        self.mylabel.grid(row=0, column=0)
        self.mylabel = Label(self.root, text='Hello', width=5)
        self.mylabel.grid(row=1, column=0)
        self.mylabel1 = Label(self.root, text='Hello1', bg='red', fg='white')
        self.mylabel1.grid(row=0, column=1)
        self.mylabel2 = Label(self.root, text='Hello2')
        self.mylabel2.grid(row=1, column=2)
        # Button
        self.mybtn = Button(self.root, text='Click', command=self.click_me)
        self.mybtn.grid(row=2, column=0)
        self.mybtn = Button(self.root, text='Choose', command=self.choose)
        self.mybtn.grid(row=2, column=2)
        # Entry
        self.myentry = Entry(self.root, width=8)
        self.myentry.grid(row=2, column=1)
        # # Text
        # self.mytext = Text(self.root, width=10, height=5)
        # self.mytext.grid(row=3, column=0)
        # Listbox
        self.fruit_list = ['Apple', 'Orange', 'Strawberry', 'Peach']
        self.mylistbox = Listbox(self.root, border=0, selectmode=MULTIPLE)
        self.mylistbox.grid(row=3, column=0, columnspan=4, pady=10)
        self.mylistbox.configure(justify=CENTER)
        for fruit in self.fruit_list:
            self.mylistbox.insert(END, fruit)
        # File directory selection
        self.my_directory_entry = Entry(self.root, state='readonly')
        self.my_directory_entry.grid(row=4, column=0, columnspan=2, padx=10)
        self.ask_directory_btn = Button(self.root, text='Directory', command=self.ask_directory)
        self.ask_directory_btn.grid(column=2, row=4)

        self.root.mainloop()

    def click_me(self):
        print("Clicked")
        print(self.myentry.get())
        self.myentry.delete(0, END)
        self.myentry.insert(END, 'Clicked')

    def choose(self):
        selection_list = []
        for selection_index in self.mylistbox.curselection():
            selection_list.append(self.fruit_list[selection_index])
        print(selection_list)

    def ask_directory(self):
        path = askdirectory()
        self.my_directory_entry.config(state='normal')
        self.my_directory_entry.insert(END, path)
        self.my_directory_entry.config(state='readonly')


if __name__ == '__main__':
    d = DemoApp()
