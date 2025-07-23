import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pypdf import PdfWriter


class PdfMenu(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("PDF Viewer")
        self.master.geometry("600x400")
        

        combiner_button = ttk.Button(self, text="Combine PDFs", command=self.combiner)
        combiner_button.pack(pady=10)

        self.button_showinfo = ttk.Button(self, text="Show Info", command=self.popup_showinfo)
        self.button_showinfo.pack()
        
        self.master.bind("<Return>", lambda *args: self.combiner()) # backup for button click
        self.pack()

    def popup_showinfo(self):
        messagebox.showwarning("Title", "Wrong value")

    
    def combiner(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        PdfCombiner(self.master)

class PdfCombiner(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pdf_files = []
        self.pdf_image = None
        self.master.title("PDF Combiner")
        self.master.geometry("600x400")
        self.grid()
        self.refresh_display()

        
    
    def refresh_display(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.add_pdf_button()
        self.display_files()
        self.combine_button()
    
    def move_left(self, index=None):
        
        if index > 0:
            self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
            self.refresh_display()
            

    def move_right(self, index=None):
        
        if index < len(self.pdf_files) - 1:
            self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
            self.refresh_display()
    
    
    
    def add_pdf_button(self):
        add_pdf_button = ttk.Button(self, text="Add PDF", command=self.file_explorer)
        add_pdf_button.grid(row=0, column=0, sticky="ew")
        
    
        
    def display_files(self):
        for files_list_index, file in enumerate(self.pdf_files):
            
            # Displays the file name
            file_label = ttk.Label(self, text=file.rsplit('/')[-1])  # Display only the file name
            file_label.grid(row=1, column=files_list_index * 2, padx=10, pady=10)
            
            # Displays the pdf image icon for each PDF file
            self.pdf_image = tk.PhotoImage(file="assets/PDF_file_icon.png").subsample(10)  # Adjust the subsample values as needed
            image_label = ttk.Label(self, image=self.pdf_image)
            image_label.grid(row=2, column=files_list_index * 2, columnspan=2, padx=10, pady=10)
            image_label.image = self.pdf_image # this confuses me but it is necessary to keep a reference to the image ?
            
            # add buttons
            # lambda idx=files_list_index sets the fucntion argument to the current index
            # so that the correct index is passed when the button is clicked
            left_button = ttk.Button(self, text="Left", command=lambda idx=files_list_index: self.move_left(index=idx))
            left_button.grid(row=3, column=files_list_index * 2, padx=5, pady=5)

            right_button = ttk.Button(self, text="Right",  command=lambda idx=files_list_index: self.move_right(index=idx))
            right_button.grid(row=3, column=files_list_index * 2 + 1, padx=5, pady=5)
    def file_explorer(self):
        # Placeholder for file explorer functionality
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Pdf", "*.pdf"),
                                                       ("all files", "*.*")))
        
        if filename:
            self.pdf_files.append(filename)
            self.refresh_display()
            
            
    def combine_button(self):
        combine_button = ttk.Button(self, text="Combine PDFs", command=self.combine_pdfs)
        combine_button.grid(row=0, column=1, sticky="se")
        
    def combine_pdfs(self):
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Not enought PDF's", "You must have more than 1 PDF to combine")
            return
        filename = filedialog.asksaveasfilename(initialdir = "/",
                                          title = "Save the file", defaultextension= "*.pdf", initialfile="cobined.pdf", 
                                          filetypes = (("Pdf", "*.pdf"),
                                                       ("all files", "*.*")))
        
        if filename:
            merger = PdfWriter()

            for pdf in self.pdf_files:
                merger.append(pdf)

            merger.write(filename)
            merger.close()
            self.pdf_files = []
            self.refresh_display()
root = tk.Tk()
PdfMenu(root)
root.mainloop()