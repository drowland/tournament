README for tournament_db

This is my submission for Project 2 of the FSWD Nanodegree @ Udacity

Contents
========

tournament.sql
- Postgres DB initiatization script to set up table structure and minimum reference data

tournament.py
- Main project code that implements the various functions to support a swiss style tournament

tournament_test_py
- Test cases that runs through the various features of tournament.py

README.md
- This file

Usage
=====

You will require a postgres database called 'tournment' before starting out.  With this database selected, run the tournament.sql file by invoking from the psql prompt as follows:

\i tournament.sql

Next you need to make sure you have the python / postgre library installed.  This is psycopg2.

Place the tournament.py and tournament_test.pg in the same location and run the test suite as follows:

python tournament_test.py

Notes
=====

All of the advanced options have been imlemented except for the following:

"When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against."

I hope you like what you see :)