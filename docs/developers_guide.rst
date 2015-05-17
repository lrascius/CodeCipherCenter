Developer's Guide
=================

Source Code Directories
+++++++++++++++++++++++

All runtime code, unless otherwise required by Django, is stored in a specific folder:

- Python code is stored in

.. code-block:: console

   base_dir/cccenter/python/
   
- HTML template code is stored in

.. code-block:: console

   base_dir/cccenter/templates/cccenter/
   
- Javascript code is stored in

.. code-block:: console

   base_dir/cccenter/static/cccenter/
   
- CSS code is stored in

.. code-block:: console

   base_dir/cccenter/static/css/
   
Image files available as static assets are stored in

.. code-block:: console

   base_dir/cccenter/static/images/
   
Test Code
+++++++++

Test code falls into one of five categories:

- Unit tests stored in

.. code-block:: console

   base_dir/cccenter/testing/unit_tests/
   
- Integration tests stored in

.. code-block:: console

   base_dir/cccenter/testing/integration_tests/
   
- Acceptance tests stored in

.. code-block:: console

   base_dir/cccenter/testing/acceptance_tests/
   
- HTML verification files stored in

.. code-block:: console

   base_dir/cccenter/testing/html_validation/

This folder is empty until the integration tests are run.

Running the Test Code
+++++++++++++++++++++

To run the unit tests, enter:

.. code-block:: console

   ./unit_tests
   
while in the base_dir.

To run the integration tests, enter:

.. code-block:: console

   ./integration_tests
   
while in the base_dir.

To run the HTML validation tests, enter:

.. code-block:: console

   ./validate
   
while in the base_dir.

To run the acceptance test, open Firefox, then open Selenium (make sure it's installed first, see installation guide).
Once Selenium is open, click on File > Open... and navigate to

.. code-block:: console

   base_dir/cccenter/testing/acceptance_tests/test_case.html
   
Once the tests are loaded, click on "Play entire test suite". The acceptance tests will then run.

To find the pylint score for the website, run:

.. code-block:: console

   pylint cccenter/
   
while in the base_dir. The file pylintrc contains the settings that govern the generated report.
