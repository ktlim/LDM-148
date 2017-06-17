.. image:: https://img.shields.io/badge/ldm--148-lsst.io-brightgreen.svg
   :target: https://ldm-148.lsst.io
.. image:: https://travis-ci.org/lsst/LDM-148.svg
   :target: https://travis-ci.org/lsst/LDM-148

#######
LDM-148
#######

=============================
Data Management System Design
=============================

This is a working repository for *LDM-148: Data Management System Design*.

Links
=====

* Live drafts: http://ldm-148.lsst.io/v
* GitHub: https://github.com/lsst/LDM-148
* DocuShare: https://ls.st/LDM-148*

Building the PDF locally
========================

The document is built using LaTeX, and relies upon the `lsst-texmf <https://lsst-texmf.lsst.io/>`_ and `images <https://github.com/lsst-dm/images>`_ repositories.
It includes the necessary versions of these as git submodules.
To build from scratch::

  git clone https://github.com/lsst/LDM-148
  cd LDM-148
  git submodule init
  git submodule update
  make
