import nltk
from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters, hrf_experiment_output_path
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from nltk import ne_chunk
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
nltk.download('stopwords')

class TextProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        default_keys = {'apply_on'}
        super().__init__()
        parameters = process_parameters(parameters, default_keys)
        self.apply_on = parameters['apply_on']
        del parameters['apply_on']
        self.parameters = parameters
        self.stop_words = set(stopwords.words('english'))
        self.tfidf = TfidfVectorizer()
        self.text_processing_output_path = hrf_experiment_output_path().joinpath("preprocessing/text/")

    def pre_processing(self, data, **kwargs):
        """

        @param data:
        @return:
        """
        text_tasks = {
            "remove_stop_words": self.remove_stop_words(data),
            "pos_tagging": self.pos_tagging(data),
            "tf_idf": self.tf_idf(data),
            "stemming": self.stemming(data),
            "lemmatization": self.lemmatization(data)
        }
        parameters_keys = self.parameters.values()
        print('parameters keys: ', parameters_keys)

        new_dataset = None
        for key in parameters_keys:
            result = text_tasks[key]
            print(result)




    def remove_stop_words(self, data):
        filtered_sentence = []
        column_to_apply = self.apply_on
        feature = data[column_to_apply]
        for word in feature:
            print("Word: ", word)
            if word not in self.stop_words:
                filtered_sentence.append(word)


        return filtered_sentence
    def word_tokenizer(self, data):
        column_to_apply = self.apply_on
        feature = data[column_to_apply]
        words_array = []
        for row in feature:
            tokenized_row = word_tokenize(row)
            words_array.append(tokenized_row)

        words_serie = pd.Series(words_array)
        name_new_feature = column_to_apply + "word_tokens"
        data[name_new_feature] = words_serie
        return data

    def sentence_tokenizer(self, data):
        column_to_apply = self.apply_on
        feature = data[column_to_apply]
        words_array = []
        for row in feature:
            tokenized_row = sent_tokenize(row)
            words_array.append(tokenized_row)

        words_serie = pd.Series(words_array)
        name_new_feature = column_to_apply + "_sent_tokens"
        data[name_new_feature] = words_serie
        return data

    def remove_duplicated_words(self, data):
        pass

    def pos_tagging(self, data):
        column_to_apply = self.apply_on
        column_to_apply = column_to_apply + "_tokenized"
        feature = data[column_to_apply]
        pos_tagging_result = nltk.pos_tag(feature.values)
        return pos_tagging_result
    def named_entity_recognition(self):
        pass

    def tf_idf(self, data):
        column_to_apply = self.apply_on
        column_to_indexing = "title"
        feature_to_indexing = data[column_to_indexing]
        feature = data[column_to_apply]
        feature_matrix = self.tfidf.fit_transform(data)


        similarity_matrix = linear_kernel(feature_matrix, feature_matrix)

        #Mapping pode ir para a parte do algoritmo
        mapping = pd.Series(data.index, index=feature_to_indexing)

        similarity_matrix.to_csv(self.text_processing_output_path)


    def stemming(self, data):
        pass

    def lemmatization(self, data):

        lemmatizer = None


    def frequency(self, data):
        column_to_apply = self.apply_on
        feature = data[column_to_apply]
        freq_dist = FreqDist(feature.values)
        return freq_dist

