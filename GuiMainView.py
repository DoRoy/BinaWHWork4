
from Classifier.NB_User import NB_User
import shutil
import string
import tkinter
from tkinter import *
from tkinter import filedialog


import os



class FlowerGui(Frame):

    def __init__(self,master):
        self.master = master

        Frame.__init__(self, master)
        self.grid()

        self.nb_user = None

        self.XstartPixel = 40
        self.YstartPixel = 80


        label_0 = Label(self.master, text="Naive Bayes Classifier", width=20, font=("bold", 30))
        label_0.place( x = self.XstartPixel + 80, y = self.YstartPixel + 0)

        # Directory input
        label_folderPath = Label(self.master, text="Directory Path", width=10, font=("bold", 10))
        label_folderPath.place( x = self.XstartPixel + 130, y = self.YstartPixel + 130)
        self.entry_folderPath_text = StringVar()
        self.entry_folderPath = Entry(self.master, textvariable=self.entry_folderPath_text, width=30)
        self.entry_folderPath.place(x =self.XstartPixel + 240, y =self.YstartPixel + 130)

        # Bins input
        label_bins = Label(self.master, text="Discretization Bins", width=15, font=("bold", 10))
        label_bins.place( x = self.XstartPixel + 100,  y = self.YstartPixel + 160)
        self.entry_bins_text = StringVar()
        self.entry_bins = Entry(self.master, textvariable=self.entry_bins_text, width=10)
        self.entry_bins.place(x =self.XstartPixel + 240, y =self.YstartPixel + 160)


        def folderPath():
            image_folder_path = filedialog.askdirectory()
            self.entry_folderPath_text.set(image_folder_path)
            print(image_folder_path)




        # Find directory button
        self.folderPathButton = Button(self.master, text='Find', width=5, fg='black', command= folderPath)
        self.folderPathButton.place(x =self.XstartPixel + 440, y =self.YstartPixel + 125)





        # Gui Buttons
        self.BuildButton = Button(self.master, text='Build', width=10, bg='blue', fg='white', command= self.buildCommand)
        self.BuildButton.place(x =self.XstartPixel + 200, y =self.YstartPixel + 220)


        self.classifyButton = Button(self.master, text='Classify', width=10, bg='green', fg='white', command= self.classifyCommand)
        self.classifyButton.place(x =self.XstartPixel + 300, y =self.YstartPixel + 220)



        # ***   Status bar    ***

        self.statusLabel = Label(self.master, text="Status: Ready", width = 40, font = ("bold", 10))
        self.statusLabel.place( x = self.XstartPixel + 130, y = self.YstartPixel + 300)






    # ***   Updates the statusLabel   ***
    def updateStatus(self, newStatus):
        self.statusLabel.configure(text= "Status: " + newStatus )


    # Check if a value is int
    def isInt(self,value):
        try:
            int(value)
            return True
        except ValueError:
            return False



    def buildCommand(self):
        # self.updateStatus('Building...')

        toBuildFolderPath = self.entry_folderPath_text.get()
        if not os.path.exists(toBuildFolderPath):
            self.updateStatus('Folder path doesnt exists')
            return

        existingFileList = os.listdir(toBuildFolderPath)
        wantedFiles = ['Structure.txt','train.csv','test.csv']
        filteredFiles = [file for file in wantedFiles if file not in existingFileList]
        if len(filteredFiles) > 0:
            self.updateStatus('Files {} doesnt exists'.format(filteredFiles))
            return


        numOfBins = self.entry_bins_text.get()

        if not self.isInt(numOfBins):
            self.updateStatus('Bins must be a number!')
            return

        if numOfBins < 0:
            self.updateStatus('Bins must be a positive number!')
            return



        try:
            self.nb_user = NB_User(dir_path=toBuildFolderPath, bins=numOfBins)
            df_train = self.nb_user.getTrainData()
            self.nb_user.fit_model(df_train)


        except AssertionError as error:
            self.updateStatus(str(error))







    def classifyCommand(self):

        try:
            test_df = self.nb_user.getTestData()
            results = self.nb_user.predict(test_df)
            self.nb_user.writeResults(results)
        except AssertionError as error:
            self.updateStatus(str(error))








        results = None
        if results is None:
            self.updateStatus('Problem while Classifying')
            return


        self.updateStatus('Results were written to output.txt')


    def predictListener(self):
        pass








    @ staticmethod
    def listener(thread, action):
        thread.join()
        action()




    def enableButtons(self):
        self.classifyButton.configure(state = NORMAL)
        self.BuildButton.configure(state = NORMAL)



    def disableButtons(self):
        self.classifyButton.configure(state = DISABLED)
        self.BuildButton.configure(state = DISABLED)





def setWindowSizeAndPosition(root):

    w = 650  # width for the Tk root
    h = 430  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    return root

















