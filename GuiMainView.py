
# Imports
from Classifier.NB_User import NB_User
from tkinter import *
from tkinter import filedialog
import os


# Gui class
class NaiveBayesGui(Frame):

    def __init__(self,master):
        self.master = master
        Frame.__init__(self, master)
        self.grid()

        self.nb_user = None

        # Start position in window
        self.XstartPixel = 40
        self.YstartPixel = 80

        # Title
        label_0 = Label(self.master, text="Naive Bayes Classifier", width=20, font=("bold", 30))
        label_0.place( x = self.XstartPixel + 80, y = self.YstartPixel + 0)

        # Directory input
        label_folderPath = Label(self.master, text="Directory Path", width=10, font=("bold", 10))
        label_folderPath.place( x = self.XstartPixel + 130, y = self.YstartPixel + 130)
        self.entry_folderPath_text = StringVar()
        self.entry_folderPath_text.trace("w", self.inputField_changed)

        self.entry_folderPath = Entry(self.master, textvariable=self.entry_folderPath_text, width=30)
        self.entry_folderPath.place(x =self.XstartPixel + 240, y =self.YstartPixel + 130)

        # Bins input
        label_bins = Label(self.master, text="Discretization Bins", width=15, font=("bold", 10))
        label_bins.place( x = self.XstartPixel + 100,  y = self.YstartPixel + 160)
        self.entry_bins_text = StringVar()
        self.entry_bins_text.trace("w", self.inputField_changed)

        self.entry_bins = Entry(self.master, textvariable=self.entry_bins_text, width=10)
        self.entry_bins.place(x =self.XstartPixel + 240, y =self.YstartPixel + 160)


        # Input valid flags
        self.folderFlag = False
        self.binsFlag = True


        # File dialog
        def folderPath():

            folder_path = filedialog.askdirectory() + '/'
            self.entry_folderPath_text.set(folder_path)

            self.prepareBuild()



        # Find directory button
        self.folderPathButton = Button(self.master, text='Find', width=5, fg='black', command= folderPath)
        self.folderPathButton.place(x =self.XstartPixel + 440, y =self.YstartPixel + 125)



        # Gui Buttons
        self.BuildButton = Button(self.master, text='Build', width=10, bg='blue', fg='white', command= self.buildCommand)
        self.BuildButton.place(x =self.XstartPixel + 200, y =self.YstartPixel + 220)
        self.BuildButton.configure(state=DISABLED)

        self.classifyButton = Button(self.master, text='Classify', width=10, bg='blue', fg='white', command= self.classifyCommand)
        self.classifyButton.place(x =self.XstartPixel + 300, y =self.YstartPixel + 220)
        self.classifyButton.configure(state=DISABLED)



        # ***   Status bar    ***
        self.statusLabel = Label(self.master, text="Status: Welcome", width = 50, font = ("bold", 8))
        self.statusLabel.place( x = self.XstartPixel + 130, y = self.YstartPixel + 300)


    # Called every time an input field is changed
    def inputField_changed(self, *args):
        self.prepareBuild()




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



    def prepareBuild(self):

        self.classifyButton.configure(state=DISABLED)

        # /***  Check if bins input is valid    ***/
        numOfBins = self.entry_bins_text.get()
        if not self.isInt(numOfBins):
            self.updateStatus('Bins must be an int!')
            self.BuildButton.configure(state=DISABLED)
            self.binsFlag = False
            return

        numOfBins = int(numOfBins)
        if numOfBins < 0:
            self.updateStatus('Bins must be a positive integer!')
            self.BuildButton.configure(state=DISABLED)
            self.binsFlag = False
            return

        self.binsFlag = True


        # /***  Check folderPath    ***/

        # Check if folder exists
        toBuildFolderPath = self.entry_folderPath_text.get()
        if not os.path.exists(toBuildFolderPath):
            self.updateStatus('Folder path doesnt exists')
            self.BuildButton.configure(state=DISABLED)
            self.folderFlag = False
            return

        # Check if ['Structure.txt','train.csv','test.csv'] are all in the folder.
        existingFileList = os.listdir(toBuildFolderPath)
        wantedFiles = ['Structure.txt', 'train.csv', 'test.csv']
        filteredFiles = [file for file in wantedFiles if file not in existingFileList]
        if len(filteredFiles) > 0:
            self.updateStatus('Files %s doesnt exists' % filteredFiles)
            self.BuildButton.configure(state=DISABLED)
            self.folderFlag = False
            return

        self.folderFlag = True




        # /***  Bins and folderPath are valid    ***/

        toBuildFolderPath = self.entry_folderPath_text.get()

        # Do build
        try:
            numOfBins = int(self.entry_bins_text.get())
            self.nb_user = NB_User(dir_path=toBuildFolderPath, bins=numOfBins)
            self.nb_user.getTrainData()

            # Train file is not empty
            self.updateStatus("Ready")
            self.BuildButton.configure(state=NORMAL)

        # If some error received while building
        except AssertionError as error:
            self.BuildButton.configure(state=DISABLED)
            self.updateStatus(str(error))



    # Build - on button click
    def buildCommand(self):

        # Do build
        try:

            df_train = self.nb_user.getTrainData()
            self.nb_user.fit_model(df_train)

            # If no error occurred
            self.updateStatus('Build successfully!')
            self.classifyButton.configure(state=NORMAL)

        # If some error received while building
        except AssertionError as error:
            self.updateStatus(str(error))






    # Classify - on button click
    def classifyCommand(self):

        # Do Classify
        try:
            test_df = self.nb_user.getTestData()
            results, acc = self.nb_user.predict(test_df)
            self.nb_user.writeResults(results)
            self.updateStatus('Results were written to output.txt - Accuracy = %.3f' % (acc))

        # If some error received while classifying
        except AssertionError as error:
            self.updateStatus(str(error))




# Set the window in the middle of the screen
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

















