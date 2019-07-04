
class NaiveBayes(object):

    def __init__(self, structure):

        self.attributes_probs = {}
        self.class_probs = {}
        self.class_count = None
        self.cols_mp = {}
        self.class_ops = structure['class']
        for key, item in structure.items():
            self.cols_mp[key] = 2/len(item)



    def fit(self, data):
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
        predictions = {}
        for index, row in df_predict.iterrows():
            C_nominates = {}
            for target_c in self.class_ops:
                target_c_prob = self.class_probs[target_c]
                prob = 1
                for label, value in row.iteritems():
                    try:
                        prob *= self.attributes_probs[label][value, target_c]
                    except Exception as e:
                        prob *= (self.cols_mp[label] / self.class_count[target_c])

                C_nominates[target_c] = target_c_prob * prob
            predictions[index + 1] = max(C_nominates.keys(),key=C_nominates.get)
            # predictions[index] = max(C_nominates.keys(),key=C_nominates.get)

        return predictions



