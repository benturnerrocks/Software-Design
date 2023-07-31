import unittest
import main
import flask_individual

app = flask_individual.app

class TestHome(unittest.TestCase):
    #test the home page
    def test_route(self):
        self.app = app.test_client()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(str.encode("Hello, this is the homepage. To generate a random movie, enter the url extension: /getRandomMovie/<categories>/<criteria> where categories is the categories we are filtering the data by (i.e. genre, title, director, etc) and criteria is what we specify those categories are. Multiple distinct categories or criteria should be separated by an underscore (_) and should follow the usage guidlines specified in /usage ex: /getRandomMovie/-ca/Klara Castanho or /getRandomMovie/-ca_-ti/Klara Castanho_Jaws"),response.data,"Not correct home page.")

class TestRandom(unittest.TestCase):
    #test the getRandomMovie function
    def test_Klara(self):
        #test a specific case (Klara) which should always give the same movie
        self.app = app.test_client()
        response = self.app.get('/getRandomMovie/-ca/Klara Castanho', follow_redirects=True)
        self.assertEqual(str.encode(str(['s14', 'Movie', 'Confessions of an Invisible Girl', 'Bruno Garotti', 'Klara Castanho, Lucca Picon, Júlia Gomes, Marcus Bessa, Kiria Malheiros, Fernanda Concon, Gabriel Lima, Caio Cabral, Leonardo Cidade, Jade Cardozo', '', 'September 22, 2021', '2021', 'TV-PG', '91 min', 'Children & Family Movies, Comedies', "When the clever but socially-awkward Tetê joins a new school, she'll do anything to fit in. But the queen bee among her classmates has other ideas."])), response.data,"Klara Castanho example does not work.")
    
    def test_Random(self):
        #test the randomness of the generic getRandomMovie function
        self.app = app.test_client()
        response1 = self.app.get('/getRandomMovie/', follow_redirects=True)
        response2 = self.app.get('/getRandomMovie/', follow_redirects=True)
        self.assertNotEqual(response1.data, response2.data,"Base getRandomMovie does not return a random function. (unless by some crazy odds)")

class TestUsage(unittest.TestCase):
    #test that the usage statement is produced when asked
    def test_Usage(self):
        self.app = app.test_client()
        response = self.app.get('/usage', follow_redirects=True)
        self.assertIn(str.encode("USAGE"),response.data)

if __name__ == '__main__':
    unittest.main()