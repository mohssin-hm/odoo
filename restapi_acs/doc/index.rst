.. Odoo REST API: Version 1.0 documentation master file, created by
   sphinx-quickstart on Wed Jul  5 08:51:16 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Odoo REST API: Version 1.0 documentation
========================================

Our Odoo REST API Reference houses a lot of information, but doesn't always tell you how you should use it.

If you want to built apps and other integrations for the Odoo, this tutorial will walk you through what is required to authenticate and make basic API calls.

Get the module
==============

The module **restapi_acs** is available on **Odoo App Store**, Here are links for:
    
    * `Version 13.0 (Community) <https://www.odoo.com/apps/modules/13.0/restapi_acs/>`_
    * `Version 14.0 (Community) <https://www.odoo.com/apps/modules/13.0/restapi_acs/>`_

Installation
============

Install **restapi_acs** module by following below steps:

1. Unzip **restapi_acs** module to **custom addons** directory
2. Restart odoo server
3. Activate **Developer Mode** from the **Settings** menu
4. Navigate to the **Apps** menu
5. Click on **Update Apps List** menu in left side bar
6. Once apps list is updated, click on **Apps** menu from left / top side bar
7. Search module **restapi_acs**
8. Click on **Install** button.


Getting Started
===============

.. toctree::
   :maxdepth: 2

   connection/connection
   calling_methods/calling_methods
   workflow_manipulations/workflow_manipulations
   report_printing/report_printing
   inspection_and_introspection/inspection_and_introspection
