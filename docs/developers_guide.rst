Developer's Guide
=================

Source Code Directories
+++++++++++++++++++++++

All runtime code, unless otherwise required by Django, is stored in a specific folder:
- Python code is stored in

.. code-block:: shell-session

   base_dir/cccenter/python/
   
- HTML template code is stored in

.. code-block:: shell-session

   base_dir/cccenter/templates/cccenter/
   
- Javascript code is stored in

.. code-block:: shell-session

   base_dir/cccenter/static/cccenter/
   
- CSS code is stored in

.. code-block:: shell-session

   base_dir/cccenter/static/css/
   
Image files available as static assets are stored in

.. code-block:: shell-session

   base_dir/cccenter/static/images/
   
Test Code
+++++++++

Test code falls into one of five categories:

- Unit tests stored in

.. code-block:: shell-session

   base_dir/cccenter/testing/unit_tests/
   
- Integration tests stored in

.. code-block:: shell-session

   base_dir/cccenter/testing/integration_tests/
   
- Acceptance tests stored in

.. code-block:: shell-session

   base_dir/cccenter/testing/acceptance_tests/
   
- HTML verification files stored in

.. code-block:: shell-session

   base_dir/cccenter/testing/html_validation/

This folder is empty until validation tests are run.

Running the Test Code
+++++++++++++++++++++

To run the unit and integration tests, enter:

.. code-block:: shell-session

   python3 manage.py test
   
while in the base_dir.

To run the HTML validation tests, enter:

.. code-block:: shell-session

   ./validate
   
while in the base_dir.

-- Space reserved for acceptance tests

To find the pylint score for the website, run:

.. code-block:: shell-session

   pylint cccenter/
   
while in the base_dir. The file pylintrc contains the settings that govern the generated report.
