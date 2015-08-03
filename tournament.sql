-- Creating the database itself
/* NOTE: you might have issues dropping the database due to existing connection
         if this is not the first time creating the database.  If so comment out this section and
         uncomment the section below which drops individual tables
*/

-- *** YOU WOULD START COMMENT OUT HERE ***
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
-- *** YOU WOULD END COMMENT OUT HERE ***

-- use the tournament database
\c tournament

--CLEAN UP FROM LAST RUN, STARTING FRESH
/* THIS SECTION ONLY NEEDED IF NOT DROPPING DATABASE EACH TIME */
-- YOU WOULD START UN-COMMENT HERE ***
/*
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS registration CASCADE;
*/
-- *** YOU WOULD END UN-COMMENT HERE

-- START OF CREATION SECTION
-- PLAYERS
CREATE TABLE players (
	id		SERIAL PRIMARY KEY,
	name	TEXT NOT NULL
);

-- TOURNAMENTS (enabling support for multiple active tournaments)
CREATE TABLE tournaments (
	id		SERIAL PRIMARY KEY,
	name	TEXT NOT NULL,
	created	TIMESTAMP DEFAULT now()
);

-- Players registered for a specific tournament
CREATE TABLE registration (
	tourn_id	INTEGER NOT NULL,
	player_id 	INTEGER NOT NULL,
	PRIMARY KEY	(tourn_id, player_id)	
);

-- MATCHES AND RESULTS TABLE
-- Advanced version to support draws
CREATE TABLE matches (
	id				SERIAL PRIMARY KEY,
	tourn_id		INTEGER REFERENCES tournaments (id),
	player_1_id		INTEGER REFERENCES players (id),
	player_2_id		INTEGER REFERENCES players (id),
	player_1_points	INTEGER,	-- Win=2 | Draw=1 | Lose=0
	player_2_points	INTEGER		-- Win=2 | Draw=1 | Lose=0
);

-- TEST DATA INSERTS (2 TOURNAMENTS)
INSERT INTO tournaments (name) VALUES ('Wentworth');
INSERT INTO tournaments (name) VALUES ('Pebble Beach');