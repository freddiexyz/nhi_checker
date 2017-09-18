import logging as lg
from tkinter import *

class Checksum:

    alpha = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    
    def __init__(self, root):
        "Initializes an instance of the Checksum class, launches main window"
        self.frame = Frame(root)
        self.label = Label(self.frame, text="Enter NHI:")
        self.entry = Entry(self.frame)
        self.button = Button(self.frame, text="Go", command=self.button_press)
        
        self.frame.pack(ipady=20)
        self.label.pack(side=LEFT)
        self.entry.pack(side=LEFT)
        self.button.pack(side=LEFT)

        lg.basicConfig(level=lg.INFO,
                       filename='../NHI.log',
                       style='{', format='{asctime} {message}',
                       datefmt='%Y/%m/%d %H:%M:%S')
        
        root.mainloop()
    

    @staticmethod
    def validate(NHI):
        "Validates that given NHI matches format AAANNNN --> Bool"
        if len(NHI) == 7:
            if str.isalpha(NHI[:3]) and str.isnumeric(NHI[3:]):
                if 'i' not in NHI[:3] and 'o' not in NHI[:3]:
                    return True
        return False

    
    @staticmethod
    def check(NHI):
        "Checks that given NHI is valid --> Bool"
        check_digit = int(NHI[6])
        rest_sum = sum([(Checksum.alpha.find(NHI[i]) + 1) * range(7,4,-1)[i] for i in range(3)]
                       + [int(NHI[i+3]) * range(4,1,-1)[i] for i in range(3)])
        check_sum = (rest_sum % 11)
        if check_sum != 0:
            check_sum = (11 - check_sum) % 10
            if check_sum == check_digit:
                return True
        return False


    @staticmethod
    def log_result(result, NHI):
        if result:
            is_valid = 'Valid'
        else:
            is_valid = 'Invalid'
        lg.info('{} {}'.format(NHI, is_valid))
        

    def express_result(self, result):
        if result:
            color = 'green'
        else:
            color = 'red'
        self.frame.config(bg=color)
        self.label.config(bg=color)
    
    
    def button_press(self):
        "Wrapper function for button press event"
        self.NHI = self.entry.get().strip().upper()
        if Checksum.validate(self.NHI):
            if Checksum.check(self.NHI):
                self.express_result(1)
                Checksum.log_result(1, self.NHI)
                return
            Checksum.log_result(0, self.NHI)
        self.express_result(0)

    

if __name__ == '__main__':
    Checksum(Tk())
