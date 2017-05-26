.. much more subtle headings between TOC headers
.. raw:: html

  <style>
    div.body h2 {
      background: inherit;
      border: none;
      font-size: 110%;
    }
  </style>

Introduction
============

.. image:: logo-128.png
  :class: float-right

This document describes the schema for Common Package Specification files. A Common Package Specification file (hereafter "CPS") is a mechanism for describing how users may consume a package. "User" here refers to another package, not an end user. CPS deals with *building* software, not *installing* software.

CPS is based on `JSON`_. A CPS file is a valid JSON object.

The official version of the specification is maintained at https://github.com/mwoehlke/cps.

Contents
========

General Information
'''''''''''''''''''

.. toctree::
   :maxdepth: 2

   overview
   history
   development

Core Specification
''''''''''''''''''

.. toctree::
   :maxdepth: 2

   schema
   features
   components
   configurations
   searching

Appendices
''''''''''

.. toctree::
   :maxdepth: 2

   schema-supplement
   recommendations
   sample

* :ref:`search`

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. _JSON: http://www.json.org/

.. kate: hl reStructuredText
