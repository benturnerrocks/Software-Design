import os.path
import unittest
import main
import psycopg2
import psqlConfig as config

rawData = main.DataSource()
allmovies = rawData.getAllMovies()
 
class TestRandom(unittest.TestCase):
    """ A test class for the function getRandomMovie"""

    def test_basicRandom(self):
        """checks if getRandomMovie with no arguments returns the information of a movie that is actually in the dataset"""
        self.assertIn(main.getRandomMovie(main.Parser([])), allmovies, "Output is not a valid show/movie in dataset.")

    def test_optionsRandom(self):
        """checks if getRandomMovie filtered by multiple criteria returns the information of a movie that are actually in the dataset"""
        self.assertIn(main.getRandomMovie(main.Parser(["-ty", "Movie", "-di", "Spielberg"])), allmovies, "Output is not a valid documentary movie in dataset.")
    
    def test_edgeRandom(self):
        """checks if getRandomMovie with specific filtering returns the information of the only movie that works "Confessions of an Invisible Girl"""
        self.assertListEqual(main.getRandomMovie(main.Parser(["-ty", "Movie","-di", "Bruno Garotti", "-ca", "Klara Castanho", "-y", "2021"])), main.getMovie(main.Parser(["-ti","Confessions of an Invisible Girl"])), "Output is not a valid documentary movie in dataset.")
    
    def test_Randomness(self):
        """checks if getRandomMovie without arguments is actually random (gives a new movie each time"""
        self.assertNotEqual(main.getRandomMovie(main.Parser([])), main.getRandomMovie(main.Parser([])), "Output is not random (or the odds are for ever in your favor)")

class TestGettingPopularMovies(unittest.TestCase):
    def test_popularTitlestxtExists(self):
        """Checks if popularTitles.txt is already made"""
        popularTitlesTextExists = os.path.exists('popularTitles.txt')
        self.assertTrue(popularTitlesTextExists, "The text file popularTitles.txt does not exist")

    def test_popularTitlesFunction(self):
        """Checks if getPopularTitles returns the correct list of movies
        entire popular movies list cannot be tested because it is extremely variable
        the popular movie tested here may need to be changed, especially if it is no longer popular"""
        popularMovie = 'Jaws'
        self.assertIn(popularMovie, main.getPopularMovies())

    

class TestGETMOVIE(unittest.TestCase):
    """A test class for the function getMovie"""

    def testReturnValue(self):
        """checks that getMovie actually returns a list"""
        parsedArgs = main.Parser([])
        parsedArgs.title = ["Je Suis Karl"]
        result = main.getMovie(parsedArgs)
        self.assertIsInstance(result, list, "Function does not return a list of datapoints")

    def testMovieContents(self):
        """checks that getMovie actually returns the information of a particular movie"""
        parsedArgs = main.Parser([])
        parsedArgs.title = ["Sankofa"]
        result = main.getMovie(parsedArgs)
        cursor = rawData.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE title = 'Sankofa'")
        databaseInfo = list(cursor.fetchall()[0])
        self.assertEqual(result, databaseInfo, "Function return value does not represent correct dataset entries")

    def testNoisyData(self):
        """checks that getMovie actually returns the information of a particular movie given input with weird space"""
        parsedArgs = main.Parser([])
        parsedArgs.title = ["Seabiscuit "]
        result = main.getMovie(parsedArgs)
        cursor = rawData.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE title = 'Seabiscuit'")
        databaseSeabiscuit = list(cursor.fetchall()[0])
        self.assertEqual(result, databaseSeabiscuit, "Function does not correct for spaces at end of text")

class TestPROCESSING(unittest.TestCase):
    """A test class for the data"""
    def testDataset(self):
        cursor = rawData.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM movies")
        databaseCount = list(cursor.fetchall()[0])[0]
        self.assertEqual(databaseCount, 22998, "Dataset not fully processed")
         
class testPARSER(unittest.TestCase):
    """A test class for the Parser class"""

    def testParseArgs(self):
        testString = ["-cast", "Ryan", "Gosling", "-year", "1969", "1984"]
        result = main.Parser(testString)
        self.assertEqual(result.getCast(), ["Ryan", "Gosling"], "Doesn't parse cast search terms")
        self.assertEqual(result.getYear(), ["1969", "1984"], "Doesn't parse year search terms")

class testFINDMATCHINGMOVIES(unittest.TestCase):
    """A test class for the function findMatchingMovies"""

    def testSearchOneTerm(self):
        """checks that findMatchingMovies actually returns movies with titles containing the word 'Bangkok'"""
        parsedArgs = main.Parser([])
        parsedArgs.title = ["Bangkok"]
        result = main.findMatchingMovies(parsedArgs)
        for movie in result:
            self.assertIn("Bangkok", movie, "Returns movie which don't match the criterion")

    def testParseAndSearch(self):
        """checks that findMatchingMovies actually returns movies with titles containing the work 'Bangkok', 
        after first parsing the search term through our parser."""

        parsedArgs = main.Parser(["-title", "Bangkok"])
        result = main.findMatchingMovies(parsedArgs)
        for movie in result:
            self.assertIn("Bangkok", movie, "Returns movies which don't match the criterion")    

    def testSearchEachCriterion(self):
        """Search for Pulp Fiction using every available search category, and return only the movie Pulp Fiction"""

        parsedArgs = main.Parser(["-type", "movie", "-title", "pulp fiction", "-director", "quentin tarantino", 
        "-cast", "uma thurman", "-country", "united states", "-year", "1994", "-rating", "R",
        "-genre", "cult movies", "-description", "burger-loving hit man", "-service", "netflix"])
        result = main.findMatchingMovies(parsedArgs)
        self.assertEqual(1, len(result), "Doesn't return exactly one movie")
        errorMessage = "Returns " + result[0] + " instead of Pulp Fiction"
        self.assertEqual("Pulp Fiction", result[0], errorMessage )

    def testInvalidSearch(self):
        """Check that a search for a movie which doesn't exist returns no movies"""

        parsedArgs = main.Parser(["-title", "Pulpless Fiction"])
        result = main.findMatchingMovies(parsedArgs)
        self.assertEqual([], result, "Returns a movie that doesn't exist!")


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")
