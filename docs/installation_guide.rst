Installation Guide
==================

Before beginning, make sure you have Python3 installed.

1. First, download the repository and place it in its own folder.
2. Next, if you don't have it installed, install virtualenv with:

.. code-block:: shell-session
   
   sudo pip install virtualenv
   
3. In the directory above the repository, enter:

.. code-block:: shell-session

   virtualenv venv -p python3

This will create a Python3 virtual environment.

4. To activate the virtual environment, enter:

.. code-block:: shell-session

   source venv/bin/activate
   
You can leave the virtual environment at any time with:

.. code-block:: shell-session

   deactivate
   
5. Next, move down into the folder with the repo's files in it and enter:

.. code-block:: shell-session

   pip install -r requirements.txt
   
to install all of the necessary Python packages.  If necessary, run:

.. code-block:: shell-session

   sudo pip install -r requirements.txt
   
6. To set up the (development) database, enter:

.. code-block:: shell-session

   python3 manage.py makemigrations
   python3 manage.py migrate
   
7. If you want to create a superuser account for yourself in the database, enter:

.. code-block:: shell-session

   python3 manage.py createsuperuser
   
8. To run the website on localhost, at any time enter:

.. code-block:: shell-session

   python3 manage.py runserver
   
9. To set up Selenium for acceptance testing, go to http://docs.seleniumhq.org/download/
   and download Selenium IDE 2.9.0 for Firefox.
   
That's all!  You're ready to go.
