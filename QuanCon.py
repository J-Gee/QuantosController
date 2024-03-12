import time
import mettler_toledo_device_CUSTOM
import pandas as pd
import datetime
import tkinter as tk



'''
NOTES:
Make sure to get module "mettler_toledo_device" !!!
Set dir to output location
e.g.
C:/Users/(User)/Documents/
'''
dir = "C:/Users/sgjgee2/OneDrive - The University of Liverpool/temp_hiden/pre-weighed vial dump/"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        #self.create_graph()


    def create_widgets(self):

        # Target segment
        self.target_label = tk.Label(root, text="Target dispense (mg):")
        self.target_label.place(relx =0.01, rely = 0.5)
        self.target_entry = tk.Entry(root, width = 6)
        self.target_entry.place(relx =0.21, rely = 0.5)

        # Tolerance segment
        self.tolerance_label = tk.Label(root, text="Tolerance (%):")
        self.tolerance_label.place(relx =0.25, rely = 0.5)
        self.tolerance_entry = tk.Entry(root, width = 6)
        self.tolerance_entry.place(relx =0.39, rely = 0.5)

        # Repeats segment
        self.repeats_label = tk.Label(root, text="Repeats (#):")
        self.repeats_label.place(relx =0.46, rely = 0.5)
        self.repeats_entry = tk.Entry(root, width=6)
        self.repeats_entry.place(relx =0.58, rely = 0.5)

        # Command segment
        self.command_label = tk.Label(root, text="Command:")
        self.command_label.place(relx =0.05, rely = 0.9)
        self.command_entry = tk.Entry(root, width = 40)
        self.command_entry.place(relx =0.18, rely = 0.9)
        self.command_button = tk.Button(root, text='>', command=Command, height = 1)
        self.command_button.place(relx =0.6, rely = 0.895)

        # Progress segment
        self.progress_text = tk.StringVar()
        self.progress_text.set("Waiting for input")
        self.progress_label = tk.Label(root, textvariable=self.progress_text)
        self.progress_label.place(relx =0.13, rely = 0.7)

        # Create buttons(Start, stop, quit, beep, toggle AS, HeadInfo, SampleInfo)
        self.start_button = tk.Button(root, text='Start', command=Start, width = 10)
        self.start_button.place(relx =0.1, rely = 0.57)
        self.stop_button = tk.Button(root, text='Stop', command=Stop, width = 10)
        self.stop_button.place(relx =0.25, rely = 0.57)

        self.beep_button = tk.Button(root, text="Beep", command=Beep, width = 10)
        #self.beep_button.place(relx =0.1, rely = 0.1)


        self.check_weight_label = tk.Label(root, text="Check weight - name:")
        self.check_weight_label.place(relx =0.05, rely = 0.205)
        self.check_weight_vials_label = tk.Label(root, text="#vials:")
        self.check_weight_vials_label.place(relx =0.47, rely = 0.205)
        self.check_weight_ent = tk.Entry(root, width = 20)
        self.check_weight_ent.place(relx =0.26, rely = 0.205)
        self.check_weight_repeats_ent = tk.Entry(root, width = 5)
        self.check_weight_repeats_ent.place(relx =0.54, rely = 0.205)
        self.check_weight_repeats_ent.insert(0, "30")
        self.check_weight_go = tk.Button(root, text='>', command=Weigh_cycle, height = 1)
        self.check_weight_go.place(relx =0.61, rely = 0.205)



    def get_parameters(self):
        self.target = self.target_entry.get()
        self.tolerance = self.tolerance_entry.get()
        self.repeats = self.repeats_entry.get()
        if self.target == "":
            return "Error - please set target"
        if self.tolerance == "":
            return "Error - please set tolerance"
        if self.repeats == "":
            self.repeats = 0
        return self.target, self.tolerance, self.repeats

    def get_batchnum(self):
        self.batchnum = self.check_weight_ent.get()
        if self.batchnum == "":
            return "Error - Batch number required"
        return self.batchnum
    def get_vials(self):
        self.vials = (self.check_weight_repeats_ent.get())
        if self.vials == "":
            return "Error - Please state how many vials for weighing"
        return int(self.vials)

    def get_command(self):
        self.command = self.command_entry.get()
        return self.command

    def update_progress(self, input):
        self.progress_text.set(input)
        app.update()



def Start():
    print("Start")
    if "Error" in app.get_parameters():
        print(app.get_parameters())
    else:
        target, tolerance, repeats = app.get_parameters()
        print("Target is: {}mg, tolerance is: {}%, # of repeats is: {}".format(target, tolerance, repeats))
        dev.command("QRD 1 1 5 " + target) #set target
        time.sleep(2)
        dev.command("QRD 1 1 6 " + tolerance) # set tolerance
        time.sleep(2)

        open('dispensesFile.txt', 'w').close() # clears file - change to making new files in future

        for i in range(int(repeats)):
            dev.command("@") #sets quantos to determined state
            #dev.command("QRA 60 8 0")  # sets pos to pos 0
            app.update_progress("Preparing to dose - Vial {}".format(i + 1))

            time.sleep(10)
            print(dev.command("QRA 61 1"))  # Start dosing into current position
            app.update_progress("Dosing - Vial {}".format(i + 1))
            dispensing = True
            while dispensing == True:
                time.sleep(10)
                dispense_response = dev.command("QRA") #r1 will always be 1, r2 will be 'B' if not dispensing or 'I' if dispensing, r3 will be blank or '2'
                print(dispense_response)

                if 'B' in dispense_response:
                    print("cycle {} complete".format(i+1))
                    dispensing = False

                    print(dev.get_weight())







def Weigh_cycle():
    if "Error" in app.get_batchnum():
        print(app.get_batchnum())
    else:
        batchnum = app.get_batchnum()
        vials = app.get_vials()
        print("Running process, please wait")
        time.sleep(5)
        dev.command("QRA 60 8 0")
        time.sleep(10)
        dev.zero_stable()
        r = []
        df = pd.DataFrame()

    #edit in range for # of vials

        for i in range(vials):
            dev.command(("QRA 60 8 {}").format(i+1))
            time.sleep(10)
            cVial = True

            while cVial:
                try:
                    r = dev.command("S")
                    break
                except:
                    print("Unstable weight - retrying in 5s")
                    #dev.command("@")
                    time.sleep(10)
            print(("Vial {}: " + r[0]).format(i+1))
            df = df.append({"pre_dispense":r[0]}, ignore_index=True)
        #print(df)
        d1 = datetime.datetime.now()
        d2 = d1.strftime("%d%m%Y_%H%M%S")

        df.to_csv((dir + "Batch_{}.csv").format(batchnum))
        print(("Batch {a} dumped in {b}").format(a=batchnum, b=dir))

        time.sleep(5)
        dev.command("QRA 60 8 0")



def Stop():
    print(dev.command("QRA 61 4"))
    print("Stop")
def HeadInfo():
    dev.command("QRD 2 4 11")
    print("HeadInfo")
def SampleInfo():
    dev.command("QRD 2 4 12")
    print("SampleInfo")
def Beep():
    print(dev.get_commands())
    print("Beep")
def ToggleAntiStatic():
    dev.command("QRD 1 1 15 1") #on
    #dev.command("QRD 1 1 15 0") #off
    print("ToggleAS")
def Quit():
    print("Quit")
    exit()
def Command():
    print(dev.command(app.get_command()))





# ser = serial.Serial(
#    port='COM1',
#    baudrate=9600,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS, timeout=1, rtscts=0
# )
# ser.isOpen()
# print(ser)
# print('Connected to: ' + ser.portstr)

try:
    dev =mettler_toledo_device_CUSTOM.MettlerToledoDevice(port="COM1")
    print(dev.get_serial_number())
    print(dev.get_commands())
    dev.beep()
except:
    print("No device found")


LARGE_FONT = ("Arial", 10)


# updates graph after dispense
# Root window in tk
root = tk.Tk()
root.geometry('600x600')
root.resizable(False, False)
root.title('QuanCom')

app = Application(master=root)


app.mainloop()