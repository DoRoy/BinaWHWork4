from Classifier import IO, Preprocess, NaiveBayes
from Classifier.NaiveBayes import NaiveBayes


class NB_User:
    """
    A class to help working with the NaiveBase class
    summarize the functionality to simple functions to work with.
    """

    def __init__(self, dir_path, bins):
        """
        Constructor, building the NaiveBase class by the structure in dir_path and uses #bins to discrete
        :param dir_path:
        :param bins:
        """
        self.dir_path = dir_path
        self.bins = bins
        structure_text = IO.readTXT(dir_path + 'Structure.txt')
        self.categorical_cols, self.numerical_cols = Preprocess.get_numeric_categorical_lists(structure_text)
        self.structure = Preprocess.createStructureDic(self.categorical_cols, self.numerical_cols, bins)
        self.nb_model = NaiveBayes(self.structure)


    def getTrainData(self):
        """
        Wrap the getAndProcessData function to easy use with train.csv
        :return: pd.DataFrame of the train data
        """
        return self.getAndProcessData('train.csv')

    def getTestData(self):
        """
        Wrap the getAndProcessData function to easy use with test.csv
        :return: pd.DataFrame of the test data
        """
        return self.getAndProcessData('test.csv')

    def getAndProcessData(self, file_name):
        """
        Read the csv in file_name and preform mode on missing categorical attributes
        and mean on missing numerical attributes, then preform discretion
        In case the csv is empty throws AssertionError
        :param file_name: file name to read
        :return: pd.DataFrame of the csv after fillna and discretion
        """
        df = IO.readCSV(self.dir_path + file_name)
        assert len(df) != 0, '{} Dataset is empty'.format(file_name)
        Preprocess.completeMissingVals(df, self.numerical_cols)
        Preprocess.discrete_numeric(df, self.numerical_cols, self.bins)
        return df


    def fit_model(self, train_df):
        """
        Preform fit on the model
        :param train_df: pd.DataFrame corresponding to the structure
        :return:
        """
        self.nb_model.fit(train_df)


    def predict(self, test_df):
        """
        predict using the naivebayes on df_test
        :param test_df: pd.DataFrame
        :return: (dict:results, float: accuracy)
        """
        results = self.nb_model.predict(test_df.drop(columns=['class']))
        # results_df = pd.DataFrame.from_dict(results, orient='index')
        compared_results = list(map(lambda x, y: 0 if x == y else 1, results.values(), test_df['class']))
        compared_results_tuple = list(zip(results.values(), test_df['class']))
        error = float(sum(compared_results)) / len(compared_results)
        acc = 1 - error
        # print('Accuracy = {}, Error = {}'.format(acc, error))

        return results, acc


    def writeResults(self, result):
        """
        Write the results to output.txt in the given folder
        :param result: dict of results returned from predict
        :return:
        """
        # python 3.0+
        results_str = '\n'.join("{} {}".format(key, val) for (key, val) in result.items())

        # python 3.0-
        # '\n'.join("%s %r" % (key,val) for (key,val) in result.iteritems())
        # print(results_str)
        IO.writeResults(self.dir_path + 'output.txt', results_str)


    def run(self):
        """
        Runs the whole process
        :return:
        """
        # Build
        train_df = self.getTrainData()
        self.fit_model(train_df)

        # Classify
        test_df = self.getTestData()
        results, acc = self.predict(test_df)
        self.writeResults(results)

