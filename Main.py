from Classifier.NB_User import NB_User


class MainClass:

     def GUIRun(self):
         import GuiMainView

         print("***   Main Start   ***")
         root = GuiMainView.Tk()
         root = GuiMainView.setWindowSizeAndPosition(root)
         root.title("Naive Bayes Classifier")

         guiFrame = GuiMainView.NaiveBayesGui(root)
         guiFrame.mainloop()







def main():
    # Helper class to control the Gui
    mainClass = MainClass()
    # Run the Gui
    mainClass.GUIRun()



if __name__ == '__main__':
    main()

