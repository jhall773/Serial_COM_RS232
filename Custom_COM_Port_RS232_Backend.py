import serial
from tkinter import messagebox

def send_file(settings, file_name):
    """Send a file over the configured serial connection."""
    try:
        with serial.Serial(**settings) as ser:
            with open(file_name, "rb") as file:
                file_data = file.read()
                ser.write(file_data)
                messagebox.showinfo("File Sent", f"File '{file_name}' sent successfully!")
                print(f"File '{file_name}' sent successfully!")
                return  # Exit function after successful send

    except FileNotFoundError:
        messagebox.showerror(message="Error: File not found. Please check the path.")
        print("Error: File not found. Please check the path.")

    except PermissionError:
        messagebox.showerror(message="Error: Permission denied. This path is not aceptable as a readable file.\n(You might have entered a directory instead of a file.)")
        print("Error: Permission denied. This path is not aceptable as a readable file. (You might have entered a directory instead of a file.)")

    except serial.SerialException as e:
        messagebox.showerror(message=f"Serial connection error: {e}")
        print(f"Serial connection error: {e}")

    except TypeError as e:
        messagebox.showerror(message="You may not have set-up the needed settings for your 'Serial Connection' yet.\n\nPlease be sure that you have pressed the 'Set Up Serial Connection' button and set-up a 'Serial Connection' before sending data.")
        print(f"Other 'Set-up/Connection' Error: {e}")

    except ValueError:
        messagebox.showerror(message=f"Your 'Serial Connection' settings have stop bit or data bit sizes that are  invalid.")

def send_signal(settings, file_name):
    """Continuoulsy send data over the configured serial connection."""
    try:
        with serial.Serial(**settings) as ser:
            with open(file_name, "rb") as file:
                file_data = file.read()
                ser.write(file_data)

    except FileNotFoundError:
        messagebox.showerror(message="Error: File not found. Please check the path.")
        print("Error: File not found. Please check the path.")

    except PermissionError:
        messagebox.showerror(message="Error: Permission denied. This path is not aceptable as a readable file.\n(You might have entered a directory instead of a file.)")
        print("Error: Permission denied. This path is not aceptable as a readable file. (You might have entered a directory instead of a file.)")

    except serial.SerialException as e:
        messagebox.showerror(message=f"Serial connection error: {e}")
        print(f"Serial connection error: {e}")

    except TypeError as e:
            messagebox.showerror(message="You may not have set-up the needed settings for your 'Serial Connection' yet.\n\nPlease be sure that you have pressed the 'Set Up Serial Connection' button and set-up a 'Serial Connection' before sending data.")
            print(f"Other 'Set-up/Connection' Error: {e}")

    except ValueError:
            messagebox.showerror(message=f"Your 'Serial Connection' settings have stop bit or data bit sizes that are  invalid.")
