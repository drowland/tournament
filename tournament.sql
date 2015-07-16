-- Table definitions for the tournament project.

--CLEAN UP FROM LAST RUN, STARTING FRESH
--drop table if exists registration cascade;
drop table if exists tournaments cascade;
drop table if exists matches cascade;
drop table if exists players cascade;
drop table if exists registration cascade;

-- START OF CREATION SECTION
-- PLAYERS
create table players (
	id		serial PRIMARY KEY,
	name	text NOT NULL
);

-- TOURNAMENTS (enabling support for multiple active tournaments)
create table tournaments (
	id		serial PRIMARY KEY,
	name	text NOT NULL,
	created	timestamp DEFAULT now()
);

-- Players registered for a specific tournament
create table registration (
	tourn_id	integer NOT NULL,
	player_id 	integer NOT NULL,
	PRIMARY KEY	(tourn_id, player_id)	
);

-- MATCHES AND RESULTS TABLE
/*
-- Advanced version to support draws
create table matches (
	id				serial PRIMARY KEY,
	tourn_id		integer REFERENCES tournaments (id),
	player_1_id		integer,
	player_2_id		integer,
	player_1_points	real,	-- W=1 | D=0.5 | L=0
	player_2_points	real	-- W=1 | D=0.5 | L=0
);
*/

-- MATCHES records results from a match between 2 players for a given tournament
create table matches (
	id				serial PRIMARY KEY,
	tourn_id		integer REFERENCES tournaments (id),
	win_player_id	integer REFERENCES players (id),
	lose_player_id	integer REFERENCES players (id)
);

-- TEST DATA INSERTS (2 TOURNAMENTS)
insert into tournaments (name) values ('Wentworth');
insert into tournaments (name) values ('Pebble Beach');