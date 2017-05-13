:tocdepth: 1

.. sectnum::

.. _overview:

########
Overview
########

DRAFT

Still to be done:
 - fill out more text
 - internal links
 - synchronize with previous LDM-148
 - synchronize with OpsCon documents
 - finish tracing to requirements


The LSST Data Management System (DMS) is a set of services employing a variety of software components running on computational and networking infrastructure that combine to deliver science data products to the observatory's users and support observatory operations.
The DMS is constructed by the DM subsystem in the NSF MREFC project; in the Operations era, it is operated by a combination of the LSST Data Facility, Science Operations, and Observatory Operations departments.

The data products to be delivered are defined and described in the Data Products Definition Document (LSE-163).
These are divided into three major categories or "Levels".
Level 1 data products are generated on a nightly or daily cadence and comprise raw, calibrated, and difference images as well as alerts of transient, moving, and variable objects detected from the images, published within 60 seconds, and recorded in searchable catalogs.
Level 2 data products are generated on an annual cadence and represent a complete reprocessing of the set of images taken to date to generate astronomical catalogs containing measurements and characterization of tens of billions of stars and galaxies with high and uniform astrometric and photometric accuracy.
Level 3 data products are generated, created, or imported by science users.
They derive value from their close association with or derivation from other LSST data products.
Science data products are delivered through Data Access Centers (DACs), plus streams of near-realtime alerts and telescope pointing predictions.
Each LSST data product has associated metadata providing provenance and quality metricsand tracing it to relevant calibration information in the archive.
The DACs are composed of modest but significant computational, storage, networking, and other resources intended for use as a flexible, multi-tenant environment for professional astronomers with LSST data rights to retrieve, manipulate, and annotate LSST data products in order to perform scientific discovery and inquiry.

The services that make up the DMS are in turn made up of software and underlying service components, instantiated in a particular configuration in a particular computing environment to perform a particular function.
Some software components are specific to a service; others are general-purpose and reused across multiple services.
Many services have only one instance in the production system; others have several, and all have additional instances in the development and integration environments for testing purposes.

The DMS services can be considered to consist of three tiers of components.
The top tier is science "applications" software that generates data products.
This software is used to build "payloads" that perform particular data analysis and product generation tasks.
It is also used by science users and staff to analyze the data products.
The detailed design of the components in this tier is given in Data Management Science Pipelines Design, LDM-151.
The middle tier is "middleware" software components and services that execute the science application payloads and isolate them from their environment, including changes to underlying technologies.
These components also provide data access for science users and staff.
The detailed design of the components in this tier is given in Data Management Middleware Design, LDM-152.
The bottom tier is "infrastructure": hardware, networking, and low-level software and services that provide a computing environment.
The detailed design of components in this tier is given in Data Management Infrastructure Design, LDM-129.

The DMS computing environments reside in four main physical locations: the Summit Site including the main Observatory and Auxiliary Telescope buildings on Cerro Pachon, Chile; the Base Facility data center located at the Base Site in La Serena, Chile; the Archive Facility data center at the National Center for Supercomputing Applications (NCSA) in Urbana, Illinois, USA; and the Satellite Computing Facility at CC-IN2P3 in Lyon, France.
These are linked by high-speed networks to allow rapid data movement.
The Base and Archive Facilities include production computational environments (the Base Center and Archive Center, respectively) and also the US and Chilean Data Access Centers.

The DMS service instances can be broken down into four main functional domains: a Level 1, near-realtime domain (L1) closely linked to the rest of the Observatory; a Level 2 domain (L2) organized around the annual Data Release Production; a Data Access Center domain (DAC) with associated science user support components; and an analysis and developer support domain (ADS) encompassing environments that operations staff use for science verification, software development, system integration, and system testing.
In addition, an underlying infrastructure domain (Infra) hosts services supporting all of the other domains, including a common Data Backbone that provides data transport and archiving that is the primary connection between all of the domains.
These domains are distinguished by having different users, operations timescales, interfaces, and often components.

The services that make up the DMS include (with the domains they are in noted):
 - Archiving services for the Camera and Auxiliary Telescope (L1)
 - Catch-up Archiving service (L1)
 - Engineering and Facility Database (EFD) Transformation service (L1)
 - Prompt Processing service (L1)
 - Observatory Control System (OCS) Driven Batch Processing service (L1)
 - Offline Processing service (L1)
 - Telemetry Gateway service (L1)
 - Alert Broker Feed service (L1)
 - Alert Mini-Broker service (L1)
 - Level 1 Quality Control (QC) service (L1)
 - Data Backbone service (Infra)
 - Batch Processing service (Infra)
 - Flexibly-Provisioned Compute Resources (Infra)
 - Other Infrastructure Services (Infra)
 - Calibration Products Production Execution service (L2)
 - Data Release Production Execution service (L2)
 - Level 2 Quality Control (QC) service (L2)
 - Bulk Data Distribution service (DAC)
 - Data Access Web services (DAC)
 - Science Platform service (Science Verification, Commissioning, and DAC
   instances) (ADS, DAC)
 - Developer services (ADS)
 - Integration and testing services (ADS)

The relationships between these services, their functional domains, and their science application "payloads" can be visualized in this diagram:

.. figure:: /_static/DMS_Architecture.png

    Data Management System Architecture

The science application software for the Alert Production, daytime processing, Data Release Production, and calibration processing is built out of a set of frameworks that accept plugins.
In turn, those frameworks build on middleware that provides portability and scalability.

Key applications software components include:
 - Astronomy framework (``afw``)
 - Measurement framework (``meas_base``)
 - Common measurement algorithms (``meas_algorithms``, ``meas_*``)
 - Astronomical image processing algorithms (``ip_*``)
 - Camera-specific customizations (``obs_*``)
 - Many science algorithms implemented using these components

.. figure:: /_static/DM_Application_Software_Arch.png

    Data Management Science Pipelines Software "Stack"


Key middleware components include:
 - Data access client (Data Butler) (``daf_persistence``)
 - Task framework (``pex_*``, ``pipe_base``, ``ctrl_pool``)
 - Workflow and orchestration for production control (``ctrl_*``)

Infrastructure components include:
 - Parallel distributed database (``qserv``)
 - Other databases (typically relational)
 - Filesystems
 - Authentication and authorization (identity management)
 - Provisioning and resource management
 - Monitoring

.. figure:: /_static/DM_Middleware_and_Infrastructure.png

    Data Management Middleware and Infrastructure



.. _domains:

#######
Domains
#######


.. _level-1-domain:

Level 1 Domain
==============

This domain is responsible for all near-realtime operations closely tied with Observatory operations.
Its primary goals are to archive data from the Observatory, process it into Level 1 science data products, and publish them to the DACs, alert subscribers, and back to the OCS.
It contains a large number of services because of the requirements for interaction with other Observatory systems and for output of Alerts directly to end users.

The Archiving, Catch-up Archiving, and EFD Tranformation services capture raw data and metadata and convey them to the Data Backbone for permanent archiving.
The Prompt Processing, OCS Driven Batch Processing, and Offline Processing services support execution of science payloads in three different modes, depending on control and latency requirements.
The Level 1 Quality Control Service monitors the science data products, including alerts, notifying operators if any anomalies are found.
The Telemetry Gateway, Alert Broker Feed, and Alert Mini-Broker services provide selected outputs to the OCS, community alert brokers, and LSST data rights holders, respectively.

The services in this domain need to run rapidly and reliably at times and with latencies that are not amenable to a human-in-the-loop design.
Instead, they are designed to execute autonomously, often under the control of the OCS, with human oversight, monitoring, and control only at the highest level.

.. _level-1-domain-services:

Service Descriptions
--------------------

Detailed concepts of operations for each service can be found in "Concept of Operations for the LSST Production Services" (LDM-230).


.. _archiving:

Archiving services for the Camera and Auxiliary Telescope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These capture raw images taken by the main Camera, including the wavefront sensors and the guide sensors when so configured, and the auxiliary telescope spectrograph, retrieving them from their respective Camera Data Acquisition system instances.
They also capture specific sets of metadata associated with the images, including telemetry values and event timings, from the OCS publish/subscribe middleware and/or from the EFD.
The image pixels and metadata are then permanently archived in the Data Backbone.

Requirements satisfied: DMS-REQ-0018, DMS-REQ-0068, DMS-REQ-0020, DMS-REQ-0265,
DMS-REQ-0309

Requirements partially satisfied: DMS-REQ-0004, DMS-REQ-0284, DMS-REQ-0318,
DMS-REQ-0315

.. _catch-up-archiving:

Catch-up Archiving service
^^^^^^^^^^^^^^^^^^^^^^^^^^

This archives into the Data Backbone any raw images that were missed by the primary archiving services due to network or other outage.
It retrieves information -- the same sets as specified for the primary archiving services -- from the EFD to generate metadata.
The image pixels and metadata are then permanently archived in the Data Backbone.

Requirements partially satisfied: DMS-REQ-0004, DMS-REQ-0284, DMS-REQ-0318,
DMS-REQ-0165, DMS-REQ-0315

.. _efd-transform:

Engineering and Facility Database Transformation service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This extracts all information (including telemetry, events, configurations, and commands) from the EFD and its large file annex, transforms it into a form more suitable for querying by image timestamp, and loads it into a "Transformed EFD" database available in the Data Backbone.

Requirements satisfied: DMS-REQ-0102

Requirements partially satisfied: DMS-REQ-0315

.. _prompt-processing:

Prompt Processing service
^^^^^^^^^^^^^^^^^^^^^^^^^

This captures crosstalk-corrected images from the main Camera Data Acquisition system and selected metadata from the OCS and/or EFD and executes the Alert Production science payload on them, generating Level 1 data products that are stored in the Data Backbone.
The Alert Production payload then distributes Alerts to the Alert Broker Feed service and the Alert Mini-Broker service.

The Prompt Processing service has calibration (including Collimated Beam Projector images), science, and deep drilling modes.
In calibration mode, it executes a Calibration QC payload that provides rapid feedback of raw calibration image quality.
In normal science mode, two consecutive exposures are grouped and processed as a single visit; definitions of exposure groupings to be processed as visits in other modes are TBD.
The service is required to deliver Alerts within 60 seconds of the final camera readout of a standard science visit with 98% reliability.

There is no Prompt Processing service for the auxiliary telescope spectrograph.

Requirements satisfied: DMS-REQ-0022, DMS-REQ-0069

.. _ocs-driven-batch:

OCS Driven Batch Processing service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This executes science payloads in response to commands from the Observatory Control System.
It is used for modest-latency analysis of images during Commissioning and for processing daily calibration images in normal observing operations.
Images and metadata are taken from the Data Backbone, and results are provided back to the Data Backbone; there is no direct connection from this service to the Camera Data Acquisition system.
This obviously bounds the minimum latency by the latency of the Archiving Service.
A summary status for the processing performed is returned to the OCS for each command, following the normal OCS commanding protocol.

Requirements satisfied: DMS-REQ-0131

Requirements partially satisfied: DMS-REQ-0130

.. _offline-processing:

Offline Processing service
^^^^^^^^^^^^^^^^^^^^^^^^^^

This executes science payloads to ensure that all Level 1 data products are generated within 24 hours.
In particular, this service executes the daytime Moving Object processing payload.
It also may execute a variant of the Alert Production payload if the Prompt Processing service encounters difficulties.
Images and metadata are taken from the Data Backbone, and results are provided back to the Data Backbone.

Requirements satisfied: [...]

.. _level-1-qc:

Level 1 Quality Control service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This collects information on Level 1 science and calibration payload execution, post-processes the science data products from the Data Backbone to generate additional measurements, and monitors the measurement values against defined thresholds, providing an automated quality control capability for potentially detecting issues with the environment, telescope, camera, data acquisition, or data processing.
Alarms stemming from threshold crossings are delivered to Observatory operators and to DPP Production Scientists for verification, analysis, and resolution.

Requirements satisfied: DMS-REQ-0097, DMS-REQ-0099, DMS-REQ-0101, DMS-REQ-0096,
DMS-REQ-0098, DMS-REQ-0100

.. _telemetry-gateway:

Telemetry Gateway service
^^^^^^^^^^^^^^^^^^^^^^^^^

This obtains information from Prompt and Offline Processing of images and the Level 1 Quality Control service, including quality metrics, and transmits them to the OCS as specified in the Data Management-OCS Software Communication Interface (LSE-72).
Note that further information on the status and performance of DMS services will also be available to Observatory operators through remote displays originated from the DPP processing centers.

Requirements satisfied: [...]

.. _alert-broker-feed:

Alert Broker Feed service
^^^^^^^^^^^^^^^^^^^^^^^^^

This obtains Alerts generated by the Alert Production science payload and distributes them to community alert brokers and to the Alert Mini-Broker service.

Requirements satisfied: [...]

.. _alert-mini-broker:

Alert Mini-Broker service
^^^^^^^^^^^^^^^^^^^^^^^^^

This obtains an alert feed from the Alert Broker Feed service and allows individual LSST data rights holders to execute limited filters against it, producing filtered feeds that are then distributed to the individuals.

Requirements satisfied: [...]


.. _level-1-interfaces:

Interfaces
----------

OCS to various Level 1 Domain services, including Telemetry Gateway to OCS: these interface through the SAL library provided by the OCS subsystem.

Camera DAQ to Archiver, Catch-Up Archiver, Prompt Processing: these interface through the custom library provided by the Camera DAQ.

Prompt Processing and Offline Processing to Telemetry Gateway: these interface via an internal-to-DM messaging protocol.

Prompt Processing (and Offline Processing?) to Alert Broker Feed and Alert Mini-Broker: these interface through a reliable transport system.

EFD to EFD Transformer: this interface is via connection (mechanism TBD) to the MySQL databases that make up the EFD as well as file transfer from the EFD's Large File Annex.

Prompt Processing to Offline Processing: in the event that Prompt Processing runs over its allotted time window, processing can be cancelled and the failure recorded, after which Offline Processing will redo the processing at a later time.
Note that it may be possible, if computational resources can be provisioned flexibly enough, for the Prompt Processing to just continue to run with additional resources provisioned to handle future processing.
In that case, there would effectively be an infinite time window.

Archiver, Catch-Up Archiver, Prompt Processing to Data Backbone: files are copied to Data Backbone storage via a file transfer mechanism, and their information and metadata are registered with Data Backbone management dataabases.
Catalog database entries are ingested into databases resident within the Data Backbone via bulk load or INSERT statements.

Offline Processing and OCS Driven Batch Processing to Data Backbone: payloads use the Data Butler as a client to access files and catalog databases within the Data Backbone.
If necessary, a workflow system may be interposed that could stage data from the Data Backbone to local storage prior to access by the Data Butler, but this overhead is less desirable in the Level 1 Domain.

EFD Transformer to Data Backbone: Transformed EFD entries are inserted into the database resident within the Data Backbone.

Offline Processing and OCS Driven Batch to Batch Processing: batch jobs are submitted via normal queuing mechanisms with varying priorities.
If necessary, a workflow system might be interposed.


.. _level-2-domain:

Level 2 Domain
==============

This domain is responsible for all longer-period data processing operations, including the largest and most complex payloads supported by the DMS: the annual Data Release Production (DRP) and periodic Calibration Products Productions (CPPs).
Note that CPPs will execute even while the annual DRP is executing, hence the need for a separate service.
The Level 2 Quality Control Service monitors the science data products, notifying operators if any anomalies are found.

The services in this domain need to run efficiently and reliably over long periods of time, spanning weeks or months.
They need to execute millions or billions of tasks when their input data is available while tracking the status of each and preserving its output.
They are designed to execute autonomously with human oversight, monitoring, and control primarily at the highest level, although provisions are made for manual intervention if absolutely necessary.

This domain does not have direct users (besides the operators of its services); the services within it obtain inputs from the Data Backbone and place their outputs into the Data Backbone.


.. _level-2-services:

Service Descriptions
--------------------

.. _cpp-execution:

Calibration Products Production Execution service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This executes various CPP science payloads at various intervals to generate Master Calibration Images and populate the Calibration Database with information derived from analysis of raw calibration images from the Data Backbone and information in the Transformed EFD.
This includes the computation of crosstalk correction matrices.
Although not a calibration product, the templates used by Alert Production are also generated by this service, based on raw science images from the Data Backbone.
Additional information such as external catalogs may also be taken from the Data Backbone.
Computations occur using the Flexibly-Provisioned Compute Resources.
The intervals at which this service executes will depend on the stability of Observatory systems, but are expected to include at least monthly and annual executions.
The annual execution is a prerequisite for the subsequent execution of the Data Release Production.
The service involves human scientist/operator input to determine initial configurations of the payload, to monitor and analyze the results, and possibly to provide additional configuration information during execution.

Requirements satisfied: [...]

.. _drp-execution:

Data Release Production Execution service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This executes the DRP science payload annually to generate all Level 2 data products after the annual CPP is executed.
A small-scale (about 10% of the sky) mini-production is executed first to ensure readiness, followed by the full production.
Raw science images are taken from the Data Backbone along with Master Calibration Images and information from the Transformed EFD.
Additional information such as external catalogs may also be taken from the Data Backbone.
Outputs are loaded into the Data Backbone and the Data Access Center Domain services.
Computations occur on the Flexibly-Provisioned Compute Resources, including compute and storage resources located at the Satellite Center at CC-IN2P3 in Lyon, France.
The service involves human scientist/operator/programmer input to determine initial configurations of the payload, to monitor and analyze results, and, when absolutely necessary, to make "hot fixes" during execution that maintain adequate consistency of the resulting data products.

Requirements satisfied: [...]

.. _level-2-qc:

Level 2 Quality Control service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This collects information on Level 2 science payload execution, post-processes the science data products from the Data Backbone to generate additional measurements, and monitors the measurement values against defined thresholds, providing an automated quality control capability for potentially detecting issues with the data processing but also the environment, telescope, camera, or data acquisition.
Alarms stemming from threshold crossings are delivered to DPP Production Scientists for verification, analysis, and resolution.


.. _level-2-interfaces:

Interfaces
----------

Calibration Products Production Execution and Data Release Production Execution to Data Backbone: for large-scale productions, a workflow system is expected to stage files fom the Data Backbone to local storage for access by the science payloads via the Data Butler.

Calibration Products Production Execution and Data Release Production Execution to Batch Processing: the workflow system controls and submits batch jobs to the Batch Processing service.


.. _dac-domain:

Data Access Center Domain
=========================

This domain is responsible for all science-user-facing services, primarily the instances of the LSST Science Platform (LSP) in the US and Chilean DAC environments.
The LSP is the preferred analytic interface to LSST data products in the DAC.
It provides computation and data access on both interactive and asynchronous timescales.
The domain also includes a service for distributing bulk data on daily and annual (Data Release) timescales to partner institutions, collaborations, and LSST Education and Public Outreach (EPO).

The services in this domain must support multiple users simultaneously and securely.
The LSP must be responsive to science user needs; updates are likely to occur at a different cadence from the other domains as a result.
The LSP must operate reliably enough that scientific work is not impeded.


.. _dac-services:

Service Descriptions
--------------------

.. _bulk-data-distribution:

Bulk Data Distribution service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This service is used to transmit Level 1 and Level 2 data products to partners such as LSST Education and Public Outreach, the UK LSST project, and the Dark Energy Science Collaboration.
It extracts data products from the Data Backbone and transmits them over high bandwidth connections to designated, pre-subscribed partners.

Requirements satisfied: [...]

.. _data-access-web:

Data Access Web services
^^^^^^^^^^^^^^^^^^^^^^^^

These provide language-independent, VO-compliant access to images, catalogs, and metadata.

Requirements satisfied: [...]

.. _science-platform-dac:

Science Platform service for science users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This provides an exploratory analysis environment for science users, including a spectrum of interfaces ranging from pre-determined ("portal-like") to fully flexible ("notebook-like") incorporating rendering of images, catalogs, and plots and providing for execution of LSST-provided and custom algorithms.

Requirements satisfied: [...]

.. _dac-interfaces:

Interfaces
----------

[...]


.. _ads-domain:

Analysis and Developer Support Domain
=====================================

This domain encompasses environments for analysts, developers, and integration and test.
Its users are the Observatory staff as they analyze raw data and processed data products to characterize them, develop new algorithms and systems, and test new versions of components and services before deployment.


.. _ads-services:

Service Descriptions
--------------------

.. _science-platform-qa:

Science Platform for QA
^^^^^^^^^^^^^^^^^^^^^^^

An instance of the Science Platform customized to allow access to unreleased and intermediate data products from the Alert, Calibration Products, and Data Release Productions.
Optimized for usage by scientists within the LSST Operations team.

Requirements satisfied: [...]

.. _science-platform-commissioning:

Science Platform for Commissioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An instance of the Science Platform for QA running on the Commissioning Cluster at the Base Center (but also with access to the Batch Processing service and the Flexibly Provisioned Compute Resources at the Archive) and accessing a Base endpoint for the Data Backbone.
Note that it is not expected that the Commissioning Cluster would have direct access to the Camera DAQ.

Requirements satisfied: [...]

.. _developer-services:

Developer services
^^^^^^^^^^^^^^^^^^

Software version control service, build and unit test service, ticket tracking service, documentation services, etc.

Requirements satisfied: [...]

Integration and testing services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integration environments representing various deployment environments, deployment services, test datasets, test execution services, metric measurement and tracking services, etc.

Requirements satisfied: [...]

.. _ads-interfaces:

Interfaces
----------

[...]


.. _infrastructure-domain:

Infrastructure Domain
=====================

This domain encompasses the underlying services and systems that form the computing environments in which the other domains are deployed and operate.
It interfaces with the other domains but has no direct users.


.. _infrastructure-services:

Service Descriptions
--------------------

.. _data-backbone:

Data Backbone service
^^^^^^^^^^^^^^^^^^^^^

This service provides policy-based replication of files and databases across multiple physical locations, including the Summit, Base, Archive, and Satellite Processing Centers.
It provides a registration mechanism for new datasets and database entries and a retrieval mechanism compatible with the Data Butler.

Requirements satisfied: [...]

.. _batch-processing:

Batch Processing service
^^^^^^^^^^^^^^^^^^^^^^^^

This service provides execution of batch jobs with a variety of priorities from a variety of users in a variety of environments (e.g. OS and software configurations)  on the underlying Flexibly-Provisioned Compute Resources.
It is expected to use containerization to handle the variety of environments.

Requirements satisfied: [...]

.. _compute-resources:

Flexibly-Provisioned Compute Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This service provides compute, local-to-node storage, and local-to-LAN storage resources for all processing, including Prompt Processing, Batch Processing, and the Science Platforms.

Some compute resources are reserved for particular uses, but others can be flexibly provisioned, up to a certain maximum quota, if needed to deal with surges in processing.

Priority order:
 - Prompt processing
 - Offline processing
 - OCS-controlled batch processing
 - Data Access Center processing
 - Calibration Products Production
 - Data Release Production

Requirements satisfied: [...]

.. _infrastructure-other:

Other Infrastructure Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These services include databases (including the Qserv distributed database), filesystems, provisioning systems, authentication systems, resource management systems, monitoring systems, and system management.


.. _infrastructure-interfaces:

Interfaces
----------

[...]


.. _software-components:

###################
Software Components
###################

.. _science-payloads:

Science Payloads
================

Described in DM Applications Design Document (LDM-151).
Payloads are built from application software components.

.. _alert-production-payload:

Alert Production science payload
--------------------------------

Executes under control of the Prompt Processing service on the Flexibly-Provisioned Compute Resources.
Uses crosstalk-corrected science images and associated metadata delivered by the Prompt Processing service, Master Calibration Images, Template Images, Level 1 Database, and Calibration Database information from the Data Backbone.
Generates all Level 1 science data products including Alerts (with the exception of Solar System object orbits) and loads them into the Data Backbone and Level 1 Database.
Transmits Alerts to Alert Broker Feed service and Alert Mini-Broker service.
Generates image quality feedback to the OCS and observers via the Telemetry Gateway.

Requirements satisfied: DMS-REQ-0072, DMS-REQ-0029, DMS-REQ-0030, DMS-REQ-0070,
DMS-REQ-0010, DMS-REQ-0074, DMS-REQ-0266, DMS-REQ-0269, DMS-REQ-0270,
DMS-REQ-0271, DMS-REQ-0272, DMS-REQ-0273, DMS-REQ-0317, DMS-REQ-0274,
DMS-REQ-0285

Requirements partially satisfied: DMS-REQ-0002

.. _daymops-payload:

Daytime MOPS payload
--------------------

Executes under control of the Offline Processing service after a night's observations are complete.
Uses Level 1 Database entries.
Generates entries in the MOPS Database and the Level 1 Database, including Solar System object records, measurements, and orbits.

Requirements satisfied: DMS-REQ-0286, DMS-REQ-0287, DMS-REQ-0288, DMS-REQ-0089

.. _calibration-qc-payload:

Calibration QC payload
----------------------

Executes under control of the Prompt Processing service.
Uses crosstalk-corrected science images and associated metadata delivered by the Prompt Processing service, Master Calibration Images, and Calibration Database information from the Data Backbone.
Generates image quality feedback to the OCS and observers via the Telemetry Gateway.

Requirements satisfied: [...]

.. _daily-cpp-payload:

Daily calibration products update payload
-----------------------------------------

Executes under control of the OCS-controlled batch service so that its execution can be synchronized with the observing schedule.
Uses raw calibration images and information from the Transformed EFD to generate a subset of Master Calibration Images and Calibration Database entries in the Data Backbone.

Requirements satisfied: [...]

.. _intermediate-cpp-payload:

Intermediate-period calibration products production payloads
------------------------------------------------------------

Execute under control of the CPP Execution service at nominally monthly intervals but perhaps as frequently as weekly or as infrequently as quarterly, depending on the stability of Observatory systems and their calibrations.
Uses raw calibration images and information from the Transformed EFD to generate a subset of Master Calibration Images and Calibration Database entries in the Data Backbone.

.. _template-generation-payload:

Template generation payload
---------------------------

Executes under control of the CPP Execution service if necessary to generate templates for Alert Production in between annual Data Release Productions.
Uses raw science images to generate the templates, placing them in the Data Backbone.

.. _annual-cpp-payload:

Annual calibration products production payload
----------------------------------------------

Executes under control of the CPP Execution service at annual intervals prior to the start of the Data Release Production.
Uses raw calibration images, information from the Transformed EFD, information from the Auxiliary Telescope Spectrograph, and external catalogs to generate Master Calibration Images and Calibration Database entries in the Data Backbone.

.. _drp-payload:

Data Release Production payload
-------------------------------

Executes under control of the DRP Execution service at annual intervals, first running a "mini-DRP" over a small portion of the sky, followed by the full DRP over the entire sky.
Produces science data products in the Data Backbone.


.. _suit:

SUIT
====

The Science User Interface and Tools provide visualization, plotting, catalog rendering, browsing, and searching elements that can be assembled into predetermined "portals" but can also be used flexibly within dynamic "notebook" environments.


.. _middleware:

Middleware
==========

.. _middleware-data-butler:

Data Butler access client
-------------------------

The Data Butler provides an access abstraction for all science payloads that enables their underlying data sources and destinations to be configured at runtime with a variety of back-ends ranging from local disk to network locations and a variety of serializations ranging from YAML and FITS files (potentially with the addition of HDF5 or ASDF) to database tables.

.. _middleware-qserv:

Parallel distributed database (Qserv)
-------------------------------------

Underlying the catalog data access web service is a parallel distributed database required to handle the petabyte-scale, tens-of-trillions-of-rows catalogs produced by LSST.

.. _middleware-task-framework:

Task framework
--------------

The Task Framework is a Python class library that provides a structure (standardized class entry points and conventions) to organize low-level algorithms into potentially-reusable algorithmic components (Tasks; e.g. dark frame subtraction, object detection, object measurement), and to organize tasks into basic pipelines (SuperTasks; e.g., process a single visit, build a coadd, difference a visit).
The algorithmic code is written into (Super)Tasks by overriding classes and providing implementation for standard entry points.
The Task Framework allows the pipelines to be constructed and run at the level of a single node or a group of tightly-synchronized nodes.
It allows for sub-node parallelization: trivial parallelization of Task execution, as well as providing (in the future) parallelization primitives for development of multi-core Tasks and synchronized multi-node Tasks.

The Task Framework serves as an interface layer between orchestration and the algorithmic code.
It exposes a standard interface to "activators" (command-line runners as well as the orchestration layer and QA systems), which use it to execute the code wrapped in tasks.
The Task Framework does not concern itself with fault-tolerant massively parallel execution of the pipelines over multiple (thousands) of nodes nor any staging of data that might be required; this is the concern of the orchestration middleware.

The Task Framework exposes to the orchestration system needs and capabilities of the underlying algorithmic code (i.e., the number of cores needed, expected memory-per-core, expected need for data).
It may also receive from the orchestration layer the information on how to optimally run the particular task (i.e., which level of intra-node parallelization is be desired).

It also includes a configuration API and a logging API.


.. _change-record:

#############
Change Record
#############

+-------------+------------+----------------------------------+-----------------+
| **Version** | **Date**   | **Description**                  | **Owner**       |
+=============+============+==================================+=================+
| 0.1         | 2017-02-17 | Initial draft.                   | Kian-Tat Lim    |
+-------------+------------+----------------------------------+-----------------+
| 0.2         | 2017-03-03 | Incorporated feedback.           | Kian-Tat Lim    |
+-------------+------------+----------------------------------+-----------------+
