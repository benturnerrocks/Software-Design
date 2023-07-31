import os.path
import unittest
import main


data = main.initializeData()
#if there are issues with data then that is because this file was kept up to standard with the old main.py code
#as specified in the revisions page, the only part I was revising is the documentation and so if the code doesnt work 
# it is because somehow the wrong main.py is being used

#if issues occur, i tried to create a main.py that has the code that works for these tests
 
class TestRandom(unittest.TestCase):
    """ A test class for the function getRandomMovie: THIS IS MEANT FOR OLD main.py file"""

    def test_basicRandom(self):
        """checks if getRandomMovie with no arguments returns the information of a movie that is actually in the dataset"""
        self.assertIn(main.getRandomMovie(main.Parser([])), data, "Ouput is not a valid show/movie in dataset.")

    def test_optionsRandom(self):
        """checks if getRandomMovie filtered by multiple criteria returns the information of a movie that are actually in the dataset"""
        self.assertIn(main.getRandomMovie(main.Parser(["-ti", "Movie", "-di", "Spielberg"])), data, "Ouput is not a valid documentary movie in dataset.")
    
    def test_edgeRandom(self):
        """checks if getRandomMovie with specific filtering returns the information of the only movie that works "Confessions of an Invisible Girl"""
        self.assertIn(main.getRandomMovie(main.Parser(["-ty", "Movie","-di", "Bruno Garotti", "-ca", "Klara Castanho", "-y", "2021"])), data, "Ouput is not a valid documentary movie in dataset.")
    
    def test_Randomness(self):
        """checks if getRandomMovie without arguments is actually random (gives a new movie each time"""
        self.assertNotEqual(main.getRandomMovie(main.Parser([])), main.getRandomMovie(main.Parser([])), "Ouput is not random (or the odds are for ever in your favor)")


if __name__ == '__main__':
    unittest.main()
