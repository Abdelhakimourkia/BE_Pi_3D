import open3d as o3d
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



class ConfigurationWindow  :
    def __init__(self , root):
        self.root = root
        self.root.title("model finder")
        self.root.geometry("400x400")
        self.curdir = "./models"
        self.source_model_path = None
        self.target_model_path = None
        self.scale = tk.StringVar(value="manuel")
        self.create_menu()
    

    def create_menu(self) :
        frame = tk.Frame(self.root)
        frame.pack()
        ttk.Button(self.root , text= "Import source model" , command=self.import_source_model).pack(pady=10)
        ttk.Button(self.root , text= "Import target model" , command=self.import_target_model).pack(pady=10)
        ttk.Label(self.root, text= "What method of rescaling you want to use :") .pack(pady=10)
        ttk.Combobox(state="readonly" , values=["mesh resolution" 
                                                             , "scale ratio icp"
                                                             , "manuel"
                                                             , "ransac matching"] , textvariable=self.scale).pack(pady= 10)
        self.bt =ttk.Button(text="Start registration" , command=self.close , state=tk.DISABLED)
        self.bt.pack(pady=10)


    def close(self) :
        self.root.destroy()

    def import_source_model(self) :
        file_path = self.find_file()
        if file_path :
            self.source_model_path = file_path
            self.update_button_state()

    def import_target_model(self) :
        file_path = self.find_file()
        if file_path :
            self.target_model_path = file_path
            self.update_button_state()
    

    def find_file(self) :
        file_path = filedialog.askopenfilename(
            title="Choose a 3D Model",
            initialdir=self.curdir,
            filetypes=[
                ("PLY Files", "*.ply"),
            ],
        )
        return file_path
    
    def update_button_state(self):
        if self.source_model_path and self.target_model_path:
            self.bt.config(state=tk.NORMAL)


if __name__ == "__main__":

    root = tk.Tk()
 
    app = ConfigurationWindow(root )
    root.mainloop()
        

