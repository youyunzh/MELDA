from src.base_files.base_content_selector import BaseContentSelector
from src.helpers.class_document import Document
from src.helpers.class_sentence import Sentence
from mead.mead_summary_generator import MeadSummaryGenerator
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
import numpy as np
from scipy.sparse import dok_matrix

class MeadContentSelector(BaseContentSelector):
    """
    Select content using MEAD scores
    """

    def get_sentence_position(self, sentence, n, c_max=1):
        """
        Get the position score for this sentence
        :param: sentence, c_max (optional)
        :return: float
        """
        i = sentence.position
        # original equation adds 1 to the numerator but our sentence numbering
        # is zero-based so +1 isn't necessary
        p_score = ((n - i) / n) * c_max

        return p_score

    def get_first_sentence_overlap(self, sentence):
        pass

    def get_cluster_centroid(self, documents, idf_array, threshold=-1):
        """
        The centroid for the cluster is the vector for
        the pseudo-document for the cluster, cf. MEAD paper
        :param: documents, idf_array, threshold (optional)
        :return: numpy array
        """
        word_sentence_matrix = Vectors().get_topic_matrix(documents).toarray()
        total_words_in_cluster = word_sentence_matrix.sum(0)

        # The original MEAD implementation used: matrix for num DOCUMENTS in topic X num words in corpus
        # But "document" is a flexible term -- see Gina's response in Canvas discussion...
        # so using sentences as a proxy for documents for now
        sentences_per_word = np.count_nonzero(word_sentence_matrix, axis=0)
        average_count = np.divide(total_words_in_cluster, sentences_per_word)

        if len(average_count) != len(idf_array):
            raise Exception("Cluster centroid arrays must be the same length")

        centroid_cluster = np.multiply(average_count, idf_array)
        if threshold == -1:
            self.__calculate_threshold(centroid_cluster)
        centroid_cluster[centroid_cluster < threshold] = 0 # set all centroid word values below threshold to zero

        return centroid_cluster

    def __calculate_threshold(self, centroid_cluster):
        """
        Calculate threshold for centroid value if not given
        This is just a trial value, it can be modified as needed/appropriate
        :param: centroid_cluster
        :return: float
        """
        cluster_max = centroid_cluster.max()
        cluster_mean = centroid_cluster.mean()
        return (cluster_max + cluster_mean) / 2

    def get_centroid_score(self, sentence, centroid):
        """
        Get the centroid score for this sentence
        :param: sentence, centroid
        :return: float
        """
        centroid_score = 0

        for word in sentence:
            word_idx = WordMap.id_of(word)
            centroid_score += centroid[word_idx]

        return centroid_score

    def apply_redundancy_score(self):
        pass

    def get_score(self, sentence, centroid, n, w_c=1, w_p=1, w_f=1):
        """
        Get the MEAD score for this sentence
        :param sentence:
        """

        # get each parameter for the score
        c_score = self.get_centroid_score(sentence, centroid)
        p_score = self.get_sentence_position(sentence, n)
        f_score = self.get_first_sentence_overlap(sentence)

        # add up the scores adjusted with optional score weights (default weights of 1)
        score = (w_c * c_score) + (w_p * p_score) + (w_f * f_score)

        sentence.set_mead_score(score)  # assign score value to Sentence object

    def select_content(self, documents, idf_array): # todo: pass the idf_array into select content in run_summarization
        """
        Select the salient content for the summary
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """
        selected_content = []
        centroid = self.get_cluster_centroid(documents, idf_array)
        for doc in documents:
            n = len(documents)
            for s in doc.sens:
                self.get_score(s, centroid, n)
                selected_content.append(s)

        return selected_content