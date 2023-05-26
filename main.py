from tkinter import *
from tkinter import messagebox,ttk
from tkinter import filedialog
import requests
import os
class Window:
    def __init__(self):
        self.root=Tk()
        self.root.title=self.root.title("Downloader")
        self.geometry=self.root.geometry("400x300")
        self.frameUpper=Frame(self.root)
        self.frameUpper.pack(pady=20)
        self.urlLabel=Label(self.frameUpper,text="Enter URL ",font=("Times",12))
        self.urlLabel.pack(side="left")
        self.urlInput=Entry(self.frameUpper,width=25,font=("Times",13),borderwidth=3)
        self.urlInput.pack(side="right",padx=20)
        self.frameUpper2=Frame(self.root)
        self.frameUpper2.pack(pady=20)
        self.selectPath=Button(self.frameUpper2,text="Select Path to Save File with Extension",command=self.selectPathFunction,font=("Times",11))
        self.selectPath.pack(side="top")
        self.frameUpper3=Frame(self.root)
        self.frameUpper3.pack()
        self.downloadButton=Button(self.frameUpper3,text="Start Download",command=self.startDownload,font=("Times",11))
        self.downloadButton.pack(side="left")
        self.cancelButton=Button(self.frameUpper3,text="Cancel/Delete download",command=self.cancelDownload,font=("Times",11))
        self.frameUpper4=Frame(self.root,pady=20)
        self.frameUpper4.pack()
        self.frameUpper5=Frame(self.frameUpper4)
        self.frameUpper5.pack(side="bottom")
        self.cancelButton.pack(side="right",padx=9)
        self.root.mainloop()
        self.fileP=""
        self.cancelProcess=False
    
    def selectPathFunction(self):
        self.fileP=filedialog.asksaveasfilename()
        if("." not in self.fileP):
             messagebox.askokcancel("Error","Please Provide Extension with File Name.")
             self.urlInput.delete(0,END)
        elif(len(self.fileP.split(".")[1])<2):
             messagebox.askokcancel("Error","Please Provide Extension with File Name.")
             self.urlInput.delete(0,END)
        else:
            self.pathLabel=Label(self.frameUpper2,text=self.fileP,pady=10)
            self.pathLabel.pack(side="bottom")
     
    def cancelDownload(self):
        try:
            confirm=messagebox.askyesno("Cancel","Do you really want to Cancel ?")
            print(confirm)
            messagebox.askokcancel("Download Cancellation","Done..")
            if(confirm):
                self.cancelProcess=True
                os.remove(self.fileP)
                print("Done")
        except:
             message=messagebox.askokcancel("Error","No File in Progress.")
    

    def startDownload(self):
        self.progress=ttk.Progressbar(self.frameUpper4,orient="horizontal",length=200,maximum=100)
        self.progress["value"]=0
        self.progress.pack(side="top")
        self.showPercentage=Label(self.frameUpper5,text=0,pady=10,font=("Times",13,"bold"))
        self.per=Label(self.frameUpper5,text="% Completed",pady=10,font=("Times",13,"bold"))
        self.per.pack(side="right")
        self.showPercentage.pack(side="left")
        try:
           self.data=requests.get(self.urlInput.get())
           self.totalSize=int(self.data.headers.get("content-length"))
           self.blocksize=10000
           with open(f"{self.fileP}","wb") as f:
                    for data in self.data.iter_content(self.blocksize):
                          oldpercentage=int(self.showPercentage["text"])
                          newPercentage=int(oldpercentage)+int((self.blocksize*100)/self.totalSize)
                          self.showPercentage["text"]=newPercentage
                          self.progress["value"]=newPercentage
                          f.write(data)
                    self.showPercentage["text"]=100
                    self.progress["value"]=100
                    completeMessage=messagebox.askokcancel("Done","Downloading Completed Successfully.")
        except (Exception):
            self.messageBox=messagebox.askokcancel("Warning ⚠️","Please Enter a Valid URL.")
            
        self.root.mainloop()



Window()
        