# Serial_COM_RS232
I made the application designed here for an electrical engineer to specify communication preferences between a laptop/PC and an external device over serial COM ports using the RS232 standard connector. This application was tested by writing messages from my laptop/PC to an Arduino R4 Minima's memory. A similar test can be run using a simple text (.txt) file for the data sending and a wired connection (like a USB cable) from a laptop COM port to another device.

Note: I was unfamiliar with the topic of serial and COM port connections, and at first was not even aware of the coding applications of a "Serial, Non-network, non-socket based" application. So, I did some research on what COM ports are and got more help from Microsoft's Copiolot AI, which led me to an open-source python library called **pyserial**. Here is the conversation: https://copilot.microsoft.com/shares/1fnCtcT6P7pspaPatv3Kd

Another Note: I used Microsoft's Copilot AI to help me create code for a **Tkinter UI** for the application. You can see the conversation where we discussed my wireframes and design decisions and here: https://copilot.microsoft.com/shares/UTi18hDGX2F7LeYqvf7XG
