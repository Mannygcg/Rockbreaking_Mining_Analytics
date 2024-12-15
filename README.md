---
title: Rockbreaking Analytics
marimo-version: 0.9.16
width: medium
---

# Rockbreaking Analytics

For many mining sites, it is sometimes necessary to have a process called 'rockbreaking'. This process is used to break material that is fed to a unit operation but deemed oversized or blocking the entry of material - this is most commonly performed prior the material being transported on a unit operations such as conveyor belts.

Rockbreaking is necessary to prevent any blockages and damages to the equipment upstream, however performing rockbreaking  requires for the rates to stop which consequently negatively impacts production.

On this script, we will use randomly generated data that simulates the times a processing plant uses their rockbreakers.

## Data context

The material will be sourced from different zones (Zone1, Zone2, Zone3...), each zone has a 'Rocky Ratio' (a value determined during the mining exploration), which measures how rocky the material is - thus how likely for a material to require rock breaking.

The material will be loaded to different trucks which will then tip the material to the nearest crushing area ('A' or 'B'). The material will go through a grizzly screen and then through a crusher. Each crushing area has two rockbreakers - one at the grizzly and another at the crusher.

# Important information about the data used
The data used in this exercise was randomly generated and does not represent any real data from any company or individual. It was created solely for illustrative and educational purposes.

# Repository content

## A_DATA.csv and B_DATA.csv
Both of these datasets share the same columns but their data represents material fed from different zones and fed to different unit operations (A and B). The columns present on this data are:

* TIP_DATETIME: time in which a truck dumped material to the grizzly.
* ORIGIN: zone from which the material was extracted.
* MASS: tonnes of material on the truck
* TRUCK_ID: unique truck identifier.
* ROCKY_RATIO: calculated likeliness for a material to be rocky - 1 being rocky and 5 being not rocky. Rockier material tends to generate more rockbreaking events.

## RB_DATA.csv

* AREA: indicates in which crusher (A or B) the rockbreaking event occurred.
* LOCATION: indicates at which section of primary crusher (Grizzly or Crusher) the rockbreaking event occurred.
* EVENT_START: time in which the event started.
* EVENT_END: time in which the event finished.
* LENGTH: duration of the event (seconds) that afffected performance.

## RockBreaking_Analytics.py
Python file edited using marimo.

## RB_Report.html
HTML file with all of the report information including coding within the python file.

## RB_Report_Excluding_Code.html
HTML file with all of the relevant report information (Graphs and tables) exluding python coding.
