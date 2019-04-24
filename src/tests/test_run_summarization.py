import unittest
from src.run_summarization import make_soup, load_documents_for_topics, get_output_filename
from src.helpers.class_document import Document


class IOTests(unittest.TestCase):
    """
    Tests for file IO operations
    """

    def test_get_documents_for_topics(self):
        topic_soup = make_soup('test_data/test_topics.xml')
        topics = load_documents_for_topics(topic_soup)
        expected_topics = {'PUP1A': [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002'),
                                     Document('TST20190201.0001'), Document('TST20190201.0002')],
                           'WAR2A': [Document('TST_ENG_20190301.0001'), Document('TST_ENG_20190301.0002'),
                                     Document('TST20190401.0001'), Document('TST20190401.0002')]}
        self.assertCountEqual(topics, expected_topics)

    def test_get_output_filename(self):
        topic_id = 'PUP1A'
        output_file = get_output_filename(topic_id, 'test')

        self.assertEqual(output_file, '../outputs/D2/PUP1-A.M.100.A.test')


if __name__ == '__main__':
    unittest.main()
