Installation
============

Using pip
---------

Install from PyPI using:

.. code-block:: bash

   pip install pyTGA

Using uv
--------

`uv <https://docs.astral.sh/uv/>`_ is a fast Python package manager. Install pyTGA using:

.. code-block:: bash

   uv add pyTGA

Or in a virtual environment:

.. code-block:: bash

   uv venv
   uv pip install pyTGA

Development Installation
------------------------

If you want to install the development version:

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/MyonicS/pyTGA

2. Install in development mode with dev dependencies:

.. code-block:: bash

   cd pyTGA
   pip install -e .[dev]

Or using uv:

.. code-block:: bash

   cd pyTGA
   uv pip install -e .[dev]
