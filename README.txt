
Soma-workflow
=============


Main Features
-------------

  **Unified interface to multiple computing resources:** 
    Submission of jobs or workflows with an unique interface to various 
    parallel resources: multiple core machines or clusters which can be 
    managed by various systems (such as Grid Engine, Condor, Torque/PBS, LSF..)

  **Workflow management:**
    Soma-workflow provides the possibility to submit a set of tasks (called jobs) 
    with execution dependencies without dealing with individual task submission.

  **Python API and Graphical User Interface:**
    The Python API was designed to be easily used by non expert user, but also
    complete to meet external software needs: submission, control and monitoring 
    of jobs and workflows. The GUI provides an easy and quick way of monitoring 
    workflows on various computing resources. The workflows can also be 
    submitted and controlled using the GUI.

  **Quick start on multiple core machines:**
    Soma-workflow is directly operational on any multiple core machine. 
    
  **Transparent remote access to computing resources:** 
    When the computing resource is remote, Soma-workflow can be used as a   
    client-server application. The communication with a remote computing 
    resource is done transparently for the user through a ssh port forwarding 
    tunnel. The client/server architecture enables the user to close the client 
    application at any time. The workflows and jobs execution are not stopped. 
    The user can open a client at any time to check the status of his 
    work.

  **File transfer and file path mapping tools:** 
    If the user's machine and the remote computing resource do not have a shared 
    file system, Soma-workflow provides tools to handle file transfers and/or 
    path name matchings.

Documentation
-------------

Visit Soma-workflow_ main page!

An extensive documentation_ is available, with ready to use examples_.

.. _Soma-workflow: http://www.brainvisa.info/soma-workflow
.. _examples: http://www.brainvisa.info/doc/soma-workflow-2.1/sphinx/examples.html
.. _documentation: http://www.brainvisa.info/doc/soma-workflow-2.1/sphinx/index.html


Installation
------------

For a quick start/test on a multiple core machine::

  $ easy_install "soma-workflow"

To enable plotting in the GUI, it may be useful to install matplotlib::

  $ easy_install "soma-workflow[plotting]"

To install the client interface to a remote computing resource::

  $ easy_install "soma-workflow[client]"

To install the client application with plotting enabled::

  $ easy_install "soma-workflow[client,plotting]"

For easy testing, the access to the local machine via Soma-workflow is always
enabled, no matter the installation chosen.

