# team-project-team-e-1
The team repository for Andreas, Ben, Christian, and Mitchell

The **team-project-team-e-1** folder contains the full project in collaboration with Andreas Miller, Mitchell Anderson, and Christian Peerzada. This includes:
  - a folder of pdfs *Non-Code* detailing the project proposal, data collection, and team contract for our project.
  - a *datasource.py* that uses PSQL database queries to pull select data from our table
  - a *main.py* that is the CLI adapted to use PSQL using functions from *datasource.py*
  - an initial Flask app *teamFlaskApp.py* that integrates our primary project functions into the Flask environment
  - our developed Flask app *teamFlaskFrontEnd.py* that includes a more complete UX
  - testing files <ins>*test_flaskapp.py*</ins> for preliminary testing of the Flask app functionality and *tests_final.py* which has more rigorous testing of the core search functionality. Both use the Python unit testing framework "unittest".

*Note:* *teamFlaskFrontEnd.py* is the main file for our Flask app.

To get the database in PSQL use the query:
\copy movies FROM 'Data/movie_database.csv' DELIMITER ',' CSV
