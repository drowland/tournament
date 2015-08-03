README for tournament_db

This is my submission for Project 2 of the FSWD Nanodegree @ Udacity

Contents
========

tournament.sql
- Postgres DB initiatization script to set up db abd table structure and minimum reference data.

IMPORTANT NOTE: you may have issues with this script when it attempts to drop the database if this is not your first time running the script as there may be existing connections to the database.  If this does happen, you can comment out the section that drops and creates the database and uncomment the section that drops the individual tables.  Unfortunately there is no easy way to force kill the existing connections that would then allow the drop/create database commands.

tournament.py
- Main project code that implements the various functions to support a swiss style tournament

tournament_test_py
- Test cases that runs through the various features of tournament.py

README.md
- This file

Usage
=====

You will require a postgres database called 'tournment' before starting out.  The tournament.sql script will take care of this for you.  All you need to do is establish a psql connection to a postgres server and then runn the following command:

\i tournament.sql

Next you need to make sure you have the python / postgre library installed.  This is psycopg2.

Place the tournament.py and tournament_test.py in the same location and run the test suite as follows:

python tournament_test.py

Notes
=====

All of the advanced options have been imlemented except for the following:

"When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against."

I hope you like what you see :)