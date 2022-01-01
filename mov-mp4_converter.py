import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import filedialog
import os
from tkinter import messagebox
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class MOV_MP4_Converter:
    def __init__(self, master):

        self.master = master

        # Give the Widget a name.
        master.title("MOV to MP4 converter")
        # Give the Widget a size.
        master.geometry("800x500")
        
        # Set the overall fontsize to 12 instead of 10.
        font.nametofont("TkDefaultFont").configure(size=12)

        # Set the style to 'clam'.
        style = ttk.Style()
        style.theme_use("clam")

        # Set the widget's background.
        master["background"] = "#e6e6e6"
        
        # Create some custom styles.
        style.configure("Background.TLabel", background="#e6e6e6")

        style.configure(
            "Buttons.TButton", background="#c2c2c2",
            bordercolor="black",
            relief="solid",
        )
        style.map(
            "Buttons.TButton",
            background=[("active", "#919a9e")],
            font=[("active",  ("TkDefaultFont", 12, "bold"))]
        )

        # Center labels.
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        all_mov_paths = []

        self.label = ttk.Label(master,
        style="Background.TLabel", text="Convert .MOV files to .MP4 files"
        )
        self.label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        mov_listbox = tk.Listbox(master, height=10, width=60)
        mov_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        mov_listbox.insert("end", "No .MOV files have been selcted.")

        x = tk.IntVar()

        def get_mov():
            '''open file explorer and let them select a .MOV files'''
            mov_paths = list(
                filedialog.askopenfilenames(
                    initialdir="\\Users", title="Select .MOV files", filetypes=(
                        ("mov files", "*.mov"),
                    )
                )
            )
            
            if mov_paths:
                for path in mov_paths:
                    if path not in all_mov_paths:
                        all_mov_paths.append(path)

            if x.get() == 1:
                mov_listbox.delete(0,'end')

            if all_mov_paths:
                for mov_path in all_mov_paths:
                    if x.get() == 0:
                        mov_listbox.delete(0, 'end')
                        x.set(1)

                    mov_listbox.insert("end", mov_path)

        btn_get_mov = ttk.Button(
            master, text='Select .MOV files',
            style="Buttons.TButton",
            command=lambda: [get_mov(), convert_btn_state()]
        )
        btn_get_mov.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        def delete_mov():
            '''Delete selection from listbox'''
            selection = mov_listbox.curselection()
            try:
                mov_listbox.delete(selection[0])
                all_mov_paths.pop(selection[0])
            except:
                pass
            if len(all_mov_paths) == 0 and not mov_listbox.get(0):
                mov_listbox.insert("end", "No .MOV files have been selcted.")

        btn_delete_mov = ttk.Button(
            master,
            text='Delete Selection',
            style="Buttons.TButton",
            command=lambda: [delete_mov(), convert_btn_state()]
        )
        btn_delete_mov.grid(row=2, column=1, padx=10, pady=10, sticky="EW")

        def convert_btn_state():
            if len(all_mov_paths) > 0:
                convert_button['state'] = 'normal'
                convert_button['text'] = 'Convert'
            else:
                convert_button['state'] = 'disabled'
                convert_button['text'] = 'First select .mov files'

        def convert():
            for path in all_mov_paths:
                mov_path = path[:-3] + "MP4"
                os.rename(path, mov_path)

            all_mov_paths.clear()
            mov_listbox.delete(0,'end')
            mov_listbox.insert("end", "No .MOV files have been selcted.")
            convert_btn_state()
            messagebox.showinfo(
                "Conversion Completed", "All .MOV files have succesfully been converted\nto their original location."
            )

        convert_button = ttk.Button(
            master,
            text="No .MOV Files Selected",
            style="Buttons.TButton", 
            command=lambda: convert(),
            state="disabled"
        )
        convert_button.grid(row=2, column=2, padx=10, pady=10, sticky="EW")
                
root = tk.Tk()
my_gui = MOV_MP4_Converter(root)
root.mainloop()