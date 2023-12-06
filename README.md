# Software Design
This repository contains project work for our Flask project on streaming services in CS257 (Software Design) at Carleton College. We focused on using Agile development methodologies and Git version control through GitHub.

The **individual-deliverables-benturnerrocks** folder contains the CLI delivered by just me without PSQL. It includes some code by teammates but my key contributions include the random function, the search functionalities, the parser, and the testing. I created and prioritized the switch to OOP using a Movie class. This includes:
  - a preliminary flask app *FlaskLab* using dummy data
  - experimental front-ends *HTML and CSS Lab* and *favoriteBookWebsite* using fabricated data
  - testing files using the Unittest library
  - a CLI *main.py* and *main_updated.py* that includes the main core functionalities of our app

The **team-project-team-e-1** folder contains the full project in collaboration with Andreas Miller, Mitchell Anderson, and Christian Peerzada. This includes:
  - a folder of pdfs *Non-Code* detailing the project proposal, data collection, and team contract for our project.
  - a *datasource.py* that uses PSQL database queries to pull select data from our table
  - a *main.py* that is the CLI adapted to use PSQL using functions from *datasource.py*
  - an initial Flask app *teamFlaskApp.py* that integrates our primary project functions into the Flask environment
  - our developed Flask app *teamFlaskFrontEnd.py* that includes a more complete UX
  - testing files *test_flaskapp.py* for preliminary testing of the Flask app functionality and *tests_final.py* which has more rigorous testing of the core search functionality. Both use the Python unit testing framework "unittest".

The final product is a locally hosted webpage created using Python (Flask), HTML, CSS, SQL, and some JavaScript. The purpose of the page is to help users parse a movie database across multiple streaming services to either find a particular movie or gain information on what type of movie they might enjoy based on certain criteria. Although more work could have been done to achieve the full potential of this project, we were constrained by time and scope. If I had more time, I would have improved the data using new data or web-scraping, improved both the creativity and breadth of the front and back end, as well as expanded to allow more diverse functionalities associated with movies. For instance, I would love to include a machine-learning aspect of the webpage that can give tailored suggestions based on search and watch history.
