# individual-deliverables-benturnerrocks

This repository is made to store individual deliverables for CS257 (software design).

The **individual-deliverables-benturnerrocks** folder contains aspects of the project before SQL integration solely written by me. This includes:
  - a flask app *FlaskLab* using dummy data
  - a front-end *HTML and CSS Lab* focusing not on the data but instead on learning the aesthetics of the UI
  - a front-end *favoriteBookWebsite* using fabricated book data
  - testing files for Flask App and command-line interface using the "unittest" library
  - txt files produced or used by the files
  - a *merge_data.py* that joins all streaming service files into a combined file that includes a new variable indicating their original streaming service
  - a *makePopularList.py* that creates *popularTitles.txt*, which keeps track of popular titles based on their search count using our site
  - a CLI *main.py* using only Netflix titles that contain our "Parser" class for parsing the CLI arguments and data-driven functions foundational to our app. These include a "findMatchingMovies" search function, a "getPopularMovies" that uses helper functions, a "getRandomMovie" random movie generator based on criteria, and a "getMovie" search that increases popularity count.
  - a *main_updated.py* using all streaming service data that simplifies *main.py* by creating a "Movie" class to keep track of movie characteristics. This version also includes docstrings as well as the ability to display the usage text to get a better understanding of the CLI.
