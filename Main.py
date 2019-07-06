from Classifier.NB_User import NB_User


class MainClass:


     def GUIRun(self):
         import GuiMainView

         print("***   Main Start   ***")
         root = GuiMainView.Tk()
         root = GuiMainView.setWindowSizeAndPosition(root)
         root.title("Naive Bayes Classifier")

         guiFrame = GuiMainView.FlowerGui(root)
         guiFrame.mainloop()







def main():
    mainClass = MainClass()
    mainClass.GUIRun()
    # nb_user = NB_User(dir_path='', bins=4)
    # nb_user.run()


def build(path, bins):
    nb_user = NB_User(dir_path=path, bins=bins)
    df_train = nb_user.getTrainData()
    nb_user.fit_model(df_train)
    return nb_user

def classify(nb_user):
    test_df = nb_user.getTestData()
    results = nb_user.predict(test_df)
    nb_user.writeResults(results)


if __name__ == '__main__':
    main()

