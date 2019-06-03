# DjangoBaseDev
Basic Django Dev environment for the creation of apps and general testing.

This is designed to be a base site with all the pieces needed to allow for the test and dev of django apps.

Ideally the apps will each inhabit their own branch and the 'master' branch will just have the base project.

## Dependencies
This assumes using [Pycharm](https://www.jetbrains.com/pycharm/download/) as the IDE
### Install Python 3.7.3
[Python](https://www.python.org/downloads/release/python-373/)
###Install GeckoDriver
[GeckoDriver](https://github.com/mozilla/geckodriver/releases)
[Adding to PATH](https://www.softwaretestinghelp.com/geckodriver-selenium-tutorial/)
###settings_secret.py
Copy settings_secret.py into folder with settings.py
### Virtual Environment
[Setup Instructions](https://www.jetbrains.com/help/pycharm-edu/creating-virtual-environment.html)
###Requirements
Run the following command in the terminal with the virtual environment activated.

`pip install -r requirements.txt`

###Django Setup
In order for the tests to run Django needs to have the migrations for the database prepared

(virtual environment)> `python manage.py makemigrations`

###PyCharm Run Configurations
This section is for setting up run configurations for the IDE

#### Testing w/pytest & Coverage

[pytest Docs](https://docs.pytest.org/en/latest/)

[coverage Docs](https://coverage.readthedocs.io/en/v4.5.x/)

[PyCharm Run Configurations](https://www.jetbrains.com/help/pycharm/creating-and-editing-run-debug-configurations.html)
* Script: `[virtual enveroment]/pytest.py`
* Parameters: `--cov-report term-missing --cov-report html --cov -ra --tb=native`
* Working Directory: `[base poject]`

These parameters will provide:
 * short one line summery of each failed test in the terminal
 * table displaying files tests where run on with number of statements, Coverage of tests and any lines of code missed by the tests
 * short traceback of each failure and exception
 * html based report in htmlcov/ for an interactive report