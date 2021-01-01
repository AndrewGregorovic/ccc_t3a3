# T3A3

## About

For this assessment I have chosen to implement an Album/Track ratings system in Spotify. This is achieved primarily through the addition of a track_ratings table to the existing database. This is created as a separate table so that it allows users to rate tracks without needing to save them to their personal Spotify library. This ratings system is initially very simple to make implementation easier. It basically just provides a way for users to assign a 1-5 rating for individual tracks and then allows them to update and remove any existing ratings they have made. In regards to album ratings, those are not set by users, instead the rating for an album is calculated as the average rating of the album's tracks ignoring any tracks without ratings as it seems more appropriate to not have unrated tracks skew the average.

## Simplifications

As the main purpose of this project is to implement a working feature, a number of simplifications to the database have been made so that the focus is on the feature rather than trying to recreating Spotify's whole database.

Along with only including the database tables necessary to create this extension, the relationship between tables has also been simplified to one-to-one relationships such as between artists and tracks. The attributes for the models used to create this extension have also been simplified, such as all the primary key ids being integers rather than a uuid.

## Table of Contents
- [Installation](#installation)
- [Data Integrity/Validation](#data-integrity-validation)
- [User Interface](#user-interface)
- [Professional Report: Privacy and Security](#professional-report-privacy-and-security)
- [Professional Report: Developer Obligations](#professional-report-developer-obligations)

## Installation

1. Clone the repository, `git clone https://github.com/AndrewGregorovic/ccc_t3a3.git`
2. Navigate to the app directory, `cd <path/to/directory>/ccc_t3a3`
3. Install a virtual environment, `python3 -m venv venv`
    > Install the venv module if you are missing it, `pip3 install venv`
4. Activate the environment, `source venv/bin/activate`
5. Install dependencies, `pip install -r requirements.txt`
6. Run the app, `python src/main.py`

## Data Integrity/Validation

Data integrity and validation is achieved in this extension through the use of constraints and unit testing.

Both the models and schemas used in this application have constraints built in to validate the data being entered into the database is correct and which therefore maintains the integrity of the database by ensuring that there are no missing fields or incorrect data types in records that have been saved to the database. The model constraints include data type constraints, null constraints, primary/foreign key constraints and length constraints for strings. Certain model attributes also have set defaults to prevent errors for fields that are not nullable and it makes sense to have a default. Schemas use multiple validation methods to validate input/output from the database such as data type validation, range validation for integers and length validation for strings as well as equal or oneof validation for appropriate string inputs. The schemas also ensure that when accepting user input, all required fields are provided so that no incomplete records are given to the database.

As the front end for this application is very limited with the project focus being more on the back end, unit testing is also conducted on all the api endpoints that do not return a html page. In these unit tests the full set of model attributes that is returned from the api request is tested to validate the data that is retrieved from the database.

## User Interface



## Professional Report: Privacy and Security



## Professional Report: Developer Obligations

