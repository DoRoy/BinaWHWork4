
class NaiveBayes(object):
    """
    This class is an implementation to NaiveBayes
    It uses m-Estimate to handle missing values in training data.
    """

    def __init__(self, structure):
        """
        The structure dict for the model to build on.
        :param structure: dict of the data attributes.
        """
        self.attributes_probs = {}
        self.class_probs = {}
        self.class_count = None
        self.cols_mp = {}
        self.class_ops = structure['class']
        # Create the mp value for the attributes.
        for key, item in structure.items():
            self.cols_mp[key] = 2/len(item)



    def fit(self, data):
        """
        Builds the model by the given data.
        calculate the probabilities of every possible attribute.
        :param data: pd.DataFrame
        :return:
        """
        n = len(data)
        self.class_count = data.groupby('class').size() + 2
        self.class_probs = self.class_count / n

        for col in data.columns:
            if col == 'class':
                continue

            col_class_count = data.groupby([col, 'class']).size() + self.cols_mp[col]
            e_esti_col = col_class_count.div(self.class_count, axis=0, level='class')
            self.attributes_probs[col] = e_esti_col


    def predict(self, df_predict):
        """
        Predict the class for every record in df_predict
        :param df_predict: pd.DataFrame with records to predict
        :return: dict of row number to predicted value, starting from 1
        """
        predictions = {}
        # Iterate over each record
        for index, row in df_predict.iterrows():
            C_nominates = {}
            # Compute to every possible class the conditional probability the record belong to that class
            for target_c in self.class_ops:
                # class probability
                target_c_prob = self.class_probs[target_c]
                prob = 1
                # Compute the conditional probability of each attribute in the record
                for label, value in row.iteritems():
                    try:
                        prob *= self.attributes_probs[label][value, target_c]
                    except Exception as e:
                        prob *= (self.cols_mp[label] / self.class_count[target_c])

                C_nominates[target_c] = target_c_prob * prob
            # Take the class with max value (argmax on class)
            predictions[index + 1] = max(C_nominates.keys(),key=C_nominates.get)

        return predictions



