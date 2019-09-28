from tkinter import Tk
from tkinter.ttk import Frame, Button, Label, Style
import game.Yamb as yamb


class Example(Frame):

    def __init__(self):
        """
        Left - table played by custom neural network trained with genetic algorithm (selection, crossover and mutation)
        Right - table played by keras neural network trained with labels generated with csp (backpropagation)
        """
        super().__init__()
        # self.left =
        self.master.title("Yamb")
        Style().configure("TButton", padding=(10, 10, 10, 10),
                          font='serif 20')

        # left columns
        self.columnconfigure(0, pad=3)      # header (1 to 6, min, max, straight ...)
        self.columnconfigure(1, pad=3)      # top2bot
        self.columnconfigure(2, pad=3)      # free
        self.columnconfigure(3, pad=3)      # bot2top
        self.columnconfigure(4, pad=3)      # first
        self.columnconfigure(5, pad=3)      # top&bot
        self.columnconfigure(6, pad=3)      # middle

        self.columnconfigure(7, pad=10)      # padding

        # right columns
        self.columnconfigure(8, pad=3)      # header (1 to 6, min, max, straight ...)
        self.columnconfigure(9, pad=3)      # top2bot
        self.columnconfigure(10, pad=3)     # free
        self.columnconfigure(11, pad=3)     # bot2top
        self.columnconfigure(12, pad=3)     # first
        self.columnconfigure(13, pad=3)     # top&bot
        self.columnconfigure(14, pad=3)     # middle

        # rows
        self.rowconfigure(0, pad=3)         # headers (top2bot, free, bot2top, first, top&bot, middle)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)
        self.rowconfigure(6, pad=3)
        self.rowconfigure(7, pad=3)         # min
        self.rowconfigure(8, pad=3)         # max
        self.rowconfigure(9, pad=3)         # straight
        self.rowconfigure(10, pad=3)        # threes
        self.rowconfigure(11, pad=3)        # full
        self.rowconfigure(12, pad=3)        # fours
        self.rowconfigure(13, pad=3)        # yamb

        # init headers
        Label(self, text="∇", borderwidth=6, relief="solid").grid(row=0, column=1)
        Label(self, text="∇Δ", borderwidth=3, relief="solid").grid(row=0, column=2)
        Label(self, text="Δ", borderwidth=3, relief="solid").grid(row=0, column=3)
        Label(self, text="R", borderwidth=3, relief="solid").grid(row=0, column=4)
        Label(self, text="↕", borderwidth=3, relief="solid").grid(row=0, column=5)
        Label(self, text="↔", borderwidth=3, relief="solid").grid(row=0, column=6)

        Label(self, text="   ", borderwidth=3, relief="flat").grid(row=0, column=7)

        Label(self, text="∇", borderwidth=3, relief="solid").grid(row=0, column=9)
        Label(self, text="∇Δ", borderwidth=3, relief="solid").grid(row=0, column=10)
        Label(self, text="Δ", borderwidth=3, relief="solid").grid(row=0, column=11)
        Label(self, text="R", borderwidth=3, relief="solid").grid(row=0, column=12)
        Label(self, text="↕", borderwidth=3, relief="solid").grid(row=0, column=13)
        Label(self, text="↔", borderwidth=3, relief="solid").grid(row=0, column=14)

        Label(self, text="1", borderwidth=3, relief="solid").grid(row=1, column=0)
        Label(self, text="2", borderwidth=3, relief="solid").grid(row=2, column=0)
        Label(self, text="3", borderwidth=3, relief="solid").grid(row=3, column=0)
        Label(self, text="4", borderwidth=3, relief="solid").grid(row=4, column=0)
        Label(self, text="5", borderwidth=3, relief="solid").grid(row=5, column=0)
        Label(self, text="6", borderwidth=3, relief="solid").grid(row=6, column=0)
        Label(self, text="min", borderwidth=3, relief="solid").grid(row=7, column=0)
        Label(self, text="max", borderwidth=3, relief="solid").grid(row=8, column=0)
        Label(self, text="kenta", borderwidth=3, relief="solid").grid(row=9, column=0)
        Label(self, text="triling", borderwidth=3, relief="solid").grid(row=10, column=0)
        Label(self, text="ful", borderwidth=3, relief="solid").grid(row=11, column=0)
        Label(self, text="kare", borderwidth=3, relief="solid").grid(row=12, column=0)
        Label(self, text="yamb", borderwidth=3, relief="solid").grid(row=13, column=0)

        Label(self, text="1", borderwidth=3, relief="solid").grid(row=1, column=8)
        Label(self, text="2", borderwidth=3, relief="solid").grid(row=2, column=8)
        Label(self, text="3", borderwidth=3, relief="solid").grid(row=3, column=8)
        Label(self, text="4", borderwidth=3, relief="solid").grid(row=4, column=8)
        Label(self, text="5", borderwidth=3, relief="solid").grid(row=5, column=8)
        Label(self, text="6", borderwidth=3, relief="solid").grid(row=6, column=8)
        Label(self, text="min", borderwidth=3, relief="solid").grid(row=7, column=8)
        Label(self, text="max", borderwidth=3, relief="solid").grid(row=8, column=8)
        Label(self, text="kenta", borderwidth=3, relief="solid").grid(row=9, column=8)
        Label(self, text="triling", borderwidth=3, relief="solid").grid(row=10, column=8)
        Label(self, text="ful", borderwidth=3, relief="solid").grid(row=11, column=8)
        Label(self, text="kare", borderwidth=3, relief="solid").grid(row=12, column=8)
        Label(self, text="yamb", borderwidth=3, relief="solid").grid(row=13, column=8)

        # init zeroes
        for column_index in range(1, 15):
            if column_index == 8 or column_index == 7:  # header
                continue
            for row_index in range(1, 14):
                Label(self, text="0", borderwidth=3, relief="flat").grid(row=row_index, column=column_index)
        self.pack()

    # def paint_table(self, talbe):


if __name__ == '__main__':
    root = Tk()
    app = Example()
    root.mainloop()

