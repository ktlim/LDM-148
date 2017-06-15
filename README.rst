#######
LDM-148
#######

=============================
Data Management System Design
=============================

This is a working repository for *LDM-148: Data Management System Design*.

* Read the living document on the web: http://ldm-148.lsst.io 

Building the PDF locally
========================

The document is built using LaTeX, and relies upon the `lsst-texmf <https://lsst-texmf.lsst.io/>`_ and `images <https://github.com/lsst-dm/images>`_ repositories.
It includes the necessary versions of these as git submodules.
To build from scratch::

  $ git clone https://github.com/lsst/LDM-148
  $ cd LDM-148
  $ git submodule init
  $ git submodule update
  $ make
