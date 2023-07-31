import os.path
import unittest
import main


data = main.initializeData()
rawData = [movie.getMovieInfo() for movie in data]
 
class TestRandom(unittest.TestCase):
    """ A test class for the function getRandomMovie"""

    def test_basicRandom(self):
        """checks if getRandomMovie with no arguments returns the information of a movie that is actually in the dataset"""
        self.assertIn(main.getRandomMovie(main.Parser([])), rawData, "Ouput is not a valid show/movie in dataset.")

    def test_optionsRandom(self):
        """checks if getRandomMovie filtered by multiple criteria returns the information of a movie that are actually in the dataset"""
        self.assertIn(main.getRandomMovie(main.Parser(["-ti", "Movie", "-di", "Spielberg"])), rawData, "Ouput is not a valid documentary movie in dataset.")
    
    def test_edgeRandom(self):
        """checks if getRandomMovie with specific filtering returns the information of the only movie that works "Confessions of an Invisible Girl"""
        self.assertIn(main.getRandomMovie(main.Parser(["-ty", "Movie","-di", "Bruno Garotti", "-ca", "Klara Castanho", "-y", "2021"])), rawData, "Ouput is not a valid documentary movie in dataset.")
    
    def test_Randomness(self):
        """checks if getRandomMovie without arguments is actually random (gives a new movie each time"""
        self.assertNotEqual(main.getRandomMovie(main.Parser([])), main.getRandomMovie(main.Parser([])), "Ouput is not random (or the odds are for ever in your favor)")
    
class TestGettingPopularMovies(unittest.TestCase):
    def test_popularTitlestxtExists(self):
        """Checks if popularTitles.txt is already made"""
        popularTitlesTextExists = os.path.exists('popularTitles.txt')
        self.assertTrue(popularTitlesTextExists, "The text file popularTitles.txt does not exist")

    def test_popularTitlesFunction(self):
        """Checks if getPopularTitles returns the correct list of movies"""
        #entire popular movies list cannot be tested because it is extremely variable
        #the popular movie tested here may need to be changed, especially if it is no longer popular
        popularMovie = 'Sankofa'
        self.assertIn(popularMovie, main.getPopularMovies())

    def test_sortingAlgorithmHelper(self):
        """checks if the bubble sort algorithm works correctly on the list it's given"""
        testList = [['MovieTitle1',1], ["MovieTitle2",4], ["MovieTitle3",3], ["MovieTitle4",5], ["MovieTitle5",2]]
        sortedtestList = [["MovieTitle1",1], ["MovieTitle5",2], ["MovieTitle3",3], ["MovieTitle2",4], ["MovieTitle4",5]]
        self.assertEqual(main.bubble_sort(testList), sortedtestList, "Sorting algorithm does not return sorted list")
    
    def test_movieListUpdateHelper(self):
        """Checks if the list of popular movies is updated when a more popular movie is found."""
        currentMovie = ["Movie", "newTitle", 11]
        movieList = [["MovieTitle1",1], ["MovieTitle5",2], ["MovieTitle3",3], ["MovieTitle2",4], ["MovieTitle4",5], ["MovieTitle7",6], ["MovieTitle8",7], ["MovieTitle10",8], ["MovieTitle6",9], ["MovieTitle9",10]]
        self.assertIn(["newTitle", 11], main.updatePopularMoviesList(movieList, currentMovie), "updatePopularMoviesList function does not replace less popular movie in list with more popular movie when list is full")

class TestGETMOVIE(unittest.TestCase):
    """A test class for the function getMovie"""

    def testReturnValue(self):
        """checks that getMovie actually returns a list"""
        result = main.getMovie("Je Suis Karl")
        self.assertIsInstance(result, list, "Function does not return a list of datapoints")

    def testMovieContents(self):
        """checks that getMovie actually returns the information of a particular movie"""
        result = main.getMovie("Sankofa")
        self.assertEqual(result, data[7].getMovieInfo(), "Function return value does not represent correct dataset entries")

    def testNoisyData(self):
        """checks that getMovie actually returns the information of a particular movie given input with weird space"""
        result = main.getMovie("Seabiscuit ")
        self.assertEqual(result, data[349].getMovieInfo(), "Function does not correct for spaces at end of text")

class TestPROCESSING(unittest.TestCase):
    """A test class for the data"""
    def testDataset(self):
        self.assertEqual(len(data), 8807, "Dataset not fully processed")

        
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
        """checks that findMatchingMovies actually returns the movie Bangkok given a search criteria"""
        parsedArgs = main.Parser([])
        parsedArgs.title = ["Bangkok"]
        result = main.findMatchingMovies(parsedArgs)
        for movie in result:
            self.assertIn("Bangkok", movie, "Returns movie which don't match the criterion")

    def testParseAndSearch(self):
        """checks that findMatchingMovies actually returns the movie Bangkok given a search criteria put into parser"""
        parsedArgs = main.Parser(["-title", "Bangkok"])
        result = main.findMatchingMovies(parsedArgs)
        for movie in result:
            self.assertIn("Bangkok", movie, "Returns movie which don't match the criterion")

if __name__ == '__main__':
    unittest.main()
    print("Everything passed")