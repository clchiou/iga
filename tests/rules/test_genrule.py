import unittest

from iga.rules.genrule import tokenize


class TestGenrule(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(
            [('LITERAL', '')],
            list(tokenize('')),
        )
        self.assertEqual(
            [
                ('LITERAL', ' '),
                ('LITERAL', '$'),
                ('LITERAL', ' '),
            ],
            list(tokenize(' $$ ')),
        )
        self.assertEqual(
            [
                ('LITERAL', ' '),
                ('SUBSTITUTION', ''),
                ('LITERAL', 'bb'),
                ('SUBSTITUTION', 'a'),
                ('LITERAL', ' '),
            ],
            list(tokenize(' $()bb$(a) ')),
        )
        self.assertEqual(
            [
                ('SUBSTITUTION', 'abc def'),
                ('SUBSTITUTION', 'location //a/b/c'),
                ('SUBSTITUTION', 'ghi'),
            ],
            list(tokenize('$(abc def)$(location //a/b/c)$(ghi)')),
        )


if __name__ == '__main__':
    unittest.main()
