-- Table definitions for the tournament project.

--CLEAN UP FROM LAST RUN, STARTING FRESH
drop table if exists tournaments cascade;
drop table if exists matches cascade;
drop table if exists players cascade;

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
	round			integer NOT NULL,
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
	round_num		integer NOT NULL,
	win_player_id	integer REFERENCES players (id),
	lose_player_id	integer REFERENCES players (id)
);


-- TEST DATA INSERTS (15 PLAYERS)
/*
insert into players (name) values ('David');
insert into players (name) values ('Gerri');
insert into players (name) values ('Ethan');
insert into players (name) values ('Jim');
insert into players (name) values ('Mike');
insert into players (name) values ('Sean');
insert into players (name) values ('Oisin');
insert into players (name) values ('Olga');
insert into players (name) values ('Linda');
insert into players (name) values ('Graham');
insert into players (name) values ('Dara');
insert into players (name) values ('Eoin');
insert into players (name) values ('Sue');
insert into players (name) values ('Robert');
insert into players (name) values ('Alyssa');
*/

-- TEST DATA INSERTS (2 TOURNAMENTS)
insert into tournaments (name) values ('Wentworth');
insert into tournaments (name) values ('Pebble Beach');

-- TEST DATA INSERTS (ROUND 1 FOR TOURNAMENT)
/*
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 1, 15);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 2, 14);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 3, 13);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 4, 12);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 5, 11);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 6, 10);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 7, 9);
insert into matches (tourn_id, round, player_1_id, player_2_id) values (1, 1, 8, null);
*/