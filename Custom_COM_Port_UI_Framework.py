import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from serial.tools import list_ports


class SerialPortApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Serial Port App")
        self.geometry("800x600")
        self.serial_config = None # ALL pages can access the serial port config

        # Container for all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Register all pages
        for F in (HomePage, SetupSerialPage, SendFileOncePage,
                  ContinuousSendPage, StreamingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Home Page", font=("Arial", 20)).pack(pady=20)

        ttk.Button(self, text="Set Up Serial Connection",
                   command=lambda: controller.show_frame(SetupSerialPage)).pack(pady=10)

        ttk.Button(self, text="Exit", command=controller.destroy).pack(pady=10)

        # Store references to the buttons so we can enable them later
        self.send_once_btn = ttk.Button(self, text="Send a File Once",
                                        command=lambda: controller.show_frame(SendFileOncePage))
        self.send_once_btn.pack(pady=10)
        self.send_once_btn.state(["disabled"])

        self.send_cont_btn = ttk.Button(self, text="Continuously Send a Data Signal",
                                        command=lambda: controller.show_frame(ContinuousSendPage))
        self.send_cont_btn.pack(pady=10)
        self.send_cont_btn.state(["disabled"])


# ---------------------------------------------------------
# SETUP SERIAL CONNECTION PAGE
# ---------------------------------------------------------
import serial  # Needed for parity constants

class SetupSerialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # This will store the final configuration dictionary
        self.serial_config = {}

        tk.Label(self, text="Set Up Serial Connection", font=("Arial", 18)).pack(pady=10)

        # -----------------------------
        # COM PORT SELECTION
        # -----------------------------
        tk.Label(self, text="Select COM Port:").pack()
        self.com_var = tk.StringVar()
        self.com_combo = ttk.Combobox(self, textvariable=self.com_var)
        self.refresh_com_ports()
        self.com_combo.pack()

        # -----------------------------
        # BAUD RATE (int > 0)
        # -----------------------------
        tk.Label(self, text="Enter Baud Rate (ints > 0):").pack()
        self.baud_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.baud_var).pack()

        # -----------------------------
        # DATA BITS (Combobox: 5, 6, 7, 8)
        # -----------------------------
        tk.Label(self, text="Select Data Bits:").pack()

        self.data_bits_var = tk.StringVar()
        self.data_bits_combo = ttk.Combobox(
            self,
            textvariable=self.data_bits_var,
            values=["5", "6", "7", "8"],
            state="readonly"
        )
        self.data_bits_combo.pack()

        # -----------------------------
        # STOP BITS (Combobox: 1, 1.5, 2)
        # -----------------------------
        tk.Label(self, text="Select Stop Bits:").pack()

        self.stop_bits_var = tk.StringVar()
        self.stop_bits_combo = ttk.Combobox(
            self,
            textvariable=self.stop_bits_var,
            values=["1", "1.5", "2"],
            state="readonly"
        )
        self.stop_bits_combo.pack()

        # -----------------------------
        # PARITY (Horizontal Radio Buttons)
        # -----------------------------
        tk.Label(self, text="Parity:").pack()
        parity_frame = tk.Frame(self)
        parity_frame.pack()

        self.parity_var = tk.StringVar(value="N")

        ttk.Radiobutton(parity_frame, text="None", value="N",
                        variable=self.parity_var).pack(side="left", padx=10)
        ttk.Radiobutton(parity_frame, text="Even", value="E",
                        variable=self.parity_var).pack(side="left", padx=10)
        ttk.Radiobutton(parity_frame, text="Odd", value="O",
                        variable=self.parity_var).pack(side="left", padx=10)

        # -----------------------------
        # FLOW CONTROL (Horizontal Radio Buttons)
        # -----------------------------
        tk.Label(self, text="Flow Control:").pack()
        flow_frame = tk.Frame(self)
        flow_frame.pack()

        self.flow_var = tk.StringVar(value="None")

        ttk.Radiobutton(flow_frame, text="None", value="None",
                        variable=self.flow_var).pack(side="left", padx=10)
        ttk.Radiobutton(flow_frame, text="Xon/Xoff", value="xonxoff",
                        variable=self.flow_var).pack(side="left", padx=10)
        ttk.Radiobutton(flow_frame, text="RTS/CTS", value="rts/cts",
                        variable=self.flow_var).pack(side="left", padx=10)

        # -----------------------------
        # FINALIZE CONFIG BUTTON
        # -----------------------------
        ttk.Button(self, text="Show Current Config", 
                         command=self.show_config).pack(pady=10)

        ttk.Button(self, text="Finalize Serial Config",
                         command=self.finalize_config).pack(pady=20)

        ttk.Button(self, text="Back to Home",
                         command=lambda: controller.show_frame(HomePage)).pack()

    # ---------------------------------------------------------
    # VALIDATION HELPERS
    # ---------------------------------------------------------
    def validate_int_gt_zero(self, value):
        try:
            return int(value) > 0
        except:
            return False

    def validate_float_gt_zero(self, value):
        try:
            return float(value) > 0
        except:
            return False

    # ---------------------------------------------------------
    # COM PORT SCAN
    # ---------------------------------------------------------
    def refresh_com_ports(self):
        ports = [port.device for port in list_ports.comports()]
        self.com_combo["values"] = ports

    # ---------------------------------------------------------
    # BUILD THE CONFIG SETTINGS IF ANY
    # ---------------------------------------------------------
    def show_config(self):
        config = self.controller.serial_config

        if not config:
            messagebox.showinfo("Serial Config", "No configuration has been saved yet.")
            return

        # Build a readable multi-line string
        config_text = (
            f"Port: {config['port']}\n"
            f"Baudrate: {config['baudrate']}\n"
            f"Data Bits (bytesize): {config['bytesize']}\n"
            f"Stop Bits: {config['stopbits']}\n"
            f"Parity: {config['parity']}\n"
            f"Xon/Xoff: {config['xonxoff']}\n"
            f"RTS/CTS: {config['rtscts']}\n"
            f"Timeout: {config['timeout']}"
        )

        messagebox.showinfo("Current Serial Configuration", config_text)

    # ---------------------------------------------------------
    # BUILD THE CONFIG DICTIONARY
    # ---------------------------------------------------------
    def finalize_config(self):
        port = self.com_var.get()
        baud_rate = self.baud_var.get()
        data_bits = self.data_bits_var.get()
        stop_bits = self.stop_bits_var.get()
        parity = self.parity_var.get()
        flow_control = self.flow_var.get()

        # Validate everything before building dictionary
        if not port.startswith("COM"):
            messagebox.showerror("Error", "Invalid COM port.")
            return
        if not self.validate_int_gt_zero(baud_rate):
            messagebox.showerror("Error", "Invalid baud rate.")
            return
        if not self.validate_int_gt_zero(data_bits):
            messagebox.showerror("Error", "Invalid data bits.")
            return
        if not self.validate_float_gt_zero(stop_bits):
            messagebox.showerror("Error", "Invalid stop bits.")
            return

        parity_dict = {
            "N": serial.PARITY_NONE,
            "E": serial.PARITY_EVEN,
            "O": serial.PARITY_ODD
        }

        flow_dict = {
            "None": False,
            "xonxoff": True,
            "rts/cts": False  # RTS/CTS handled separately
        }

        # Build final dictionary
        self.controller.serial_config = {
            "port": port,
            "baudrate": int(baud_rate),
            "bytesize": int(data_bits),
            "stopbits": float(stop_bits),
            "parity": parity_dict.get(parity, serial.PARITY_NONE),
            "xonxoff": flow_dict.get(flow_control, False),
            "rtscts": (flow_control == "rts/cts"),
            "timeout": 1
        }

        # ENABLE THE 'SEND FILE' BUTTONS ON HOME PAGE
        home = self.controller.frames[HomePage]
        home.send_once_btn.state(["!disabled"])
        home.send_cont_btn.state(["!disabled"])

        messagebox.showinfo("Serial Config Saved",
                            "Serial configuration stored successfully!")

        print("CONFIG STORED:", self.controller.serial_config)  # For debugging


# ---------------------------------------------------------
# SEND FILE ONCE PAGE
# ---------------------------------------------------------
class SendFileOncePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="Send a File Once", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Select a file from program directory:").pack()

        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(self, textvariable=self.file_var)
        self.refresh_files()
        self.file_combo.pack()

        ttk.Button(self, text="Send File", command=self.send_file).pack(pady=10)

        ttk.Button(self, text="Back to Home",
                   command=lambda: controller.show_frame(HomePage)).pack(pady=20)

    def refresh_files(self):
        files = [f for f in os.listdir(".") if os.path.isfile(f)]
        self.file_combo["values"] = files

    def send_file(self):
        filename = self.file_var.get()
        # Inserting the backend send-file function:
        from Custom_COM_Port_RS232_Backend import send_file as backend_send_file
        backend_send_file(self.controller.serial_config, filename)

# ---------------------------------------------------------
# CONTINUOUS SEND PAGE
# ---------------------------------------------------------
class ContinuousSendPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="Continuously Send Data", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Select a file from program directory:").pack()

        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(self, textvariable=self.file_var)
        self.refresh_files()
        self.file_combo.pack()

        ttk.Button(self, text="Start Continuous Sending",
                   command=self.start_stream).pack(pady=10)

        ttk.Button(self, text="Back to Home",
                   command=lambda: controller.show_frame(HomePage)).pack(pady=20)

    def refresh_files(self):
        files = [f for f in os.listdir(".") if os.path.isfile(f)]
        self.file_combo["values"] = files

    def start_stream(self):
        filename = self.file_var.get()
        self.controller.frames[StreamingPage].set_filename(filename)
        self.controller.show_frame(StreamingPage)


# ---------------------------------------------------------
# STREAMING PAGE (DOTS WINDOW)
# ---------------------------------------------------------
class StreamingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.running = False
        self.filename = None

        tk.Label(self, text="Streaming Data...", font=("Arial", 18)).pack(pady=10)

        self.text_box = tk.Text(self, height=15, width=60)
        self.text_box.pack()

        ttk.Button(self, text="Stop Sending", command=self.stop_stream).pack(pady=10)

    def set_filename(self, filename):
        self.filename = filename
        self.running = True
        self.stream_dots()

    def stream_dots(self):
        if not self.running:
            return

        # Backend: write dot to file here
        from Custom_COM_Port_RS232_Backend import send_signal as backend_send_signal
        backend_send_signal(self.controller.serial_config, self.filename)

        self.text_box.insert("end", ".")
        self.text_box.see("end")

        # Repeat every 200 ms
        self.after(200, self.stream_dots)

    def stop_stream(self):
        self.running = False
        self.text_box.delete("1.0", "end") # <-- clears all the dots
        messagebox.showinfo("Stopping", "Stopping continuous signal...\nReturn to Main Menu...")
        self.controller.show_frame(HomePage)


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app = SerialPortApp()
    app.mainloop()
    config = app.frames[SetupSerialPage].serial_config