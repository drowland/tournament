#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers(tourn_id=None):
    """Remove all the player records from the database.
    Args:
        tourn_id: (optional) tournament ID to remove resistration records at same time
        as deleting players
    """
    deleteRegistrations(tourn_id)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def deleteRegistrations(tourn_id=None):
    """Remove all the registration records from the database.
    Args:
        tourn_id: (optional) tournament ID to remove registrations from a specific tournament
        omitting tourn_id will remove all registrations
    """
    conn = connect()
    cursor = conn.cursor()
    if tourn_id==None:
        cursor.execute("DELETE FROM registration")
    else:
        cursor.execute("DELETE FROM registration WHERE tourn_id = %s", (tourn_id,))
    conn.commit()
    conn.close()

def countPlayers(tourn_id):
    """Returns the number of players currently registered for a specific tournament

    Args:
        tourn_id: tournament identifier for list of registered players
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count from registration WHERE tourn_id = %s", (tourn_id,))
    count = cursor.fetchone()
    conn.close()
    return count[0]

def registerPlayer(name, tourn_id=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      tourn_id: (optional) tournament idetifier that will register a player into a specific
                tournament at the same time as adding to the database
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s) RETURNING id", (name,))
    conn.commit()
    player_id = cursor.fetchone()[0]
    conn.close()

    # Now register the player to a specific tournament if a tourn_id was passed in
    if tourn_id != None:
        # Need to register for the tournament as well
        registerTournament(tourn_id, player_id)
    

def registerTournament(tourn_id, player_id):
    """Registers a player into a specific tournment.

    Args:
        tourn_id:  the ID of the tournment that the player is to be registered for
        player_id: the ID of the player that is being registered into the tournemnt
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO registration (tourn_id, player_id) 
                        VALUES (%s, %s)""", (tourn_id, player_id))
    conn.commit()
    conn.close()

def playerStandings(tourn_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tourn_id: tournament ID to pull list of standings for
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the number of points the player has won
        match_count: the number of matches the player has played
    """

    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT u.id, u.name, COALESCE(sum(u.points),0) as points, COALESCE(sum(u.match_count),0) as match_count FROM
                (select r.player_id as id, p.name, count(m.id) as match_count, sum(m.player_1_points) as points 
                    from registration r
                    LEFT JOIN players p ON r.player_id = p.id
                    LEFT JOIN matches m ON p.id =  m.player_1_id
                    WHERE r.tourn_id = %s
                    GROUP BY r.player_id, p.name
                UNION ALL
                select r.player_id as id, p.name, count(m.id) as match_count, sum(m.player_2_points) as points 
                    from registration r
                    LEFT JOIN players p ON r.player_id = p.id
                    LEFT JOIN matches m ON p.id =  m.player_2_id
                    WHERE r.tourn_id = %s
                    GROUP BY r.player_id, p.name) as u
                GROUP BY u.id, u.name
                ORDER BY sum(u.points) DESC''', (tourn_id, tourn_id))
    results = cursor.fetchall()
    return results


def reportMatch(tourn_id, player1, player2, player1_points, player2_points):
    """Records the outcome of a single match between two players.

    Args:
      tourn_id: the id of the tournament being played
      player1:          the player id of the first player
      player2:          the player id of the second player
      player1_points:   first player points (Win=2 | Draw=1 | Lose=0)
      player2_points:   second player points (Win=2 | Draw=1 | Lose=0)
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO matches (tourn_id, player_1_id, player_2_id, player_1_points, player_2_points) 
                      VALUES (%s, %s, %s, %s, %s)''', 
                      (tourn_id, player1, player2, player1_points, player2_points))
    conn.commit()
    conn.close()
 
def swissPairings(tourn_id):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    Args:
        tourn_id: tournament identifier for pairings to be returned
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # Get list of results from matches sorted by total points decending order
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count from matches where tourn_id = %s", (tourn_id,))
    count = cursor.fetchone()
    results = []
    if count[0] == 0:
        # no matches yet played for this tournament, therefore generate first round off
        # registration table
        cursor.execute("""SELECT r.player_id as id, p.name FROM registration r, players p 
                          WHERE r.player_id = p.id and r.tourn_id = %s""", (tourn_id,))
        players = cursor.fetchall()
        player_count = len(players)
        if player_count == 0:
            raise ValueError("No players registered therefore cannot initialise first round of matches")
        else:
            p = 0
            while p < player_count:
                player1 = players[p]
                player2 = (None, None)
                if (p+1) < player_count:
                    # We have another pair and not just a single player remaining
                    player2  = players[p+1]
                results.append((player1[0], player1[1], player2[0], player2[1]))
                p += 2   # Need to increment by two as we are processing pairs
    else:
        # Need to get full list of previous matches and results as need to ensure we
        # don't schedule the same two teams again
        # Now pull in the current player standings so we have a results history
        standings = playerStandings(tourn_id)

        next_match = []
        # identify whether we have odd/even number of teams as requires special logic for odd
        # don't care for initial pairings as first set of pairings are somewhat random so just 
        # let the last player take a bye
        if (len(standings) % 2 != 0):
            # we have an odd number of players.  find players that have already had a bye
            # in this tournament
            cursor.execute("""select player_1_id as player_id from matches 
                                where player_2_id is null and tourn_id = %s
                              union 
                              select player_2_id as player_id from matches
                                where player_1_id is null and tourn_id = %s""", (tourn_id, tourn_id))
            bye_players = cursor.fetchall()

            # give the best positioned player a buy in the next round
            for pos in standings:
                existing_bye = False
                for bye in bye_players:
                    if pos[0] == bye[0]:
                        existing_bye = True
                if existing_bye == False:
                    next_match = (pos[0], pos[1], None, None)
                    results.append(next_match)
                    standings = deleteListItems(standings, (pos,))
                    break
        
        # attempt to pair up matches
        break_out = False
        while len(standings) > 1 and break_out == False:
            player_increment = 1
            already_played = True

            while already_played and player_increment < len(standings):
                p1 = standings[0][0]    # player id of first remaining position in standings
                p2 = standings[player_increment][0]    # player id of second remaining position in standings

                # check to see if these players have already played
                cursor.execute('''SELECT count(*) as count FROM matches WHERE
                                      (player_1_id = %s and player_2_id = %s) or
                                      (player_2_id = %s and player_1_id = %s)''',
                                      (p1, p2, p1, p2))
                match_found = cursor.fetchone()

                if match_found[0] == 0:
                    # teams have not played so schedule match
                    already_played = False
                    next_match = (standings[0][0], standings[0][1], standings[player_increment][0], standings[player_increment][1])
                    results.append(next_match)
                    standings = deleteListItems(standings, (standings[0], standings[player_increment]))
                else:
                    if len(standings) == 2:
                        # only 2 players left and they have already played.  Need to break out
                        break_out = True
                        break
                    else:
                        player_increment += 1

    conn.close()

    return results

def deleteListItems(orig_list, del_items):
    """ Returns a list of player standings minus the players that need to be deleted

    During the Swiss Pairing routine playerd are matched against their adjacent players as
    per the standings.  In order to process all pairings and to cope with situations where
    players may have already played each other, the matched players are removed from the
    standings collection once paired up.  As you cannot delete multiple items from a list that 
    are not adjacent to one another, this function takes care of things by retruning a new list
    excluding the players that should be deleted

    Args:
        orig_list: The original list of all players from which you want certain players removed
        del_items: List of "players" that should be deleted from orig_list

    Returns:
        List of player standings minus the players that have been deleted
    """
    res = []
    for i in orig_list:
        if i in del_items:
            pass
        else:
            res.append(i)
    return res
    