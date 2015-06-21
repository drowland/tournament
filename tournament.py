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


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count from players")
    count = cursor.fetchone()
    conn.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

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

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT p.id, p.name, count(m1.win_player_id) as wins,
                        count(m2.lose_player_id) as losses
                      FROM players p 
                        LEFT JOIN matches m1 ON p.id = m1.win_player_id
                        LEFT JOIN matches m2 on p.id = m2.lose_player_id
                      GROUP BY p.id, p.name
                      ORDER BY count(m1.win_player_id) DESC, count(m2.lose_player_id)''')
    results = cursor.fetchall()
    
    standings = []
    player_matches = 0
    for player in results:
        #sum wins and losses to get total matches
        player_matches = player[2] + player[3]
        standings.append((player[0], player[1], player[2], player_matches))
    return standings


def reportMatch(tourn_id, round_num, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      tourn_id: the id of the tournament being played
      round_num: the round or match number within a tournament
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO matches (tourn_id, round_num, win_player_id, lose_player_id) 
                      VALUES (%s, %s, %s, %s)''', 
                      (tourn_id, round_num, winner, loser))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # hard code to tourn_id = 1 for now until extended to support multiple tournaments
    tourn_id = 1

    # Get list of results from matches sorted by total points decending order
    # Left join from Players to Matches so if no matches then assignments can be made still
    # for first time
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count from matches where tourn_id = %s", (tourn_id,))
    count = cursor.fetchone()
    results = []
    if count[0] == 0:
        # no matches yet played for this tournament, therefore generate first round off
        # players table
        cursor.execute("SELECT id, name from players")
        players = cursor.fetchall()
        player_count = len(players)
        if player_count == 0:
            raise ValueError("No players defined therefore cannot initialise first round of matches")
        else:
            p = 0
            while p < player_count:
                player1 = players[p]
                player2 = None
                if (p+1) < player_count:
                    # We have another pair and not just a single player remaining
                    player2  = players[p+1]
                results.append((player1, player2))
                p += 2   # Need to increment by two as we are processing pairs
    else:
        # Need to get full list of previous matches and results as need to ensure we
        # don't schedule the same two teams again
        # Now pull in the current player standings so we have a results history
        standings = playerStandings()
        p = 0
        next_match = []
        #while p < len(standings):
        while True:
            # Need to check if more players and if current player has played next best 
            # player already
            if len(standings) > 1:
                # can current player play next player or have they already played?
                already_played = True
                i = 1   # opponent increment
                while already_played == True:
                    cursor.execute('''SELECT count(*) as count FROM matches WHERE
                                      (win_player_id = %s and lose_player_id = %s) or
                                      (lose_player_id = %s and win_player_id = %s)''',
                                      (standings[p][0], standings[i][0], standings[p][0], 
                                      standings[i][0]))
                    match_found = cursor.fetchone()
                    if match_found[0] == 0:
                        already_played = False
                        next_match = (standings[p][0], standings[p][1], standings[i][0], standings[i][1])
                        results.append(next_match)
                        # remove both players from standings list as they now have a match assigned
                        standings = deleteListItems(standings, (standings[p], standings[i]))
                    else:
                        # Teams already played so try next set of pairings
                        i += 1
            elif len(standings) == 1:
                # Odd number of players and on last player so gets a pass?
                results.append((standings[p][0], standings[p][1], None, None))
                break
            else:
                # no players left to process
                break
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
        del_items: List ok "players" that should be deleted from orig_list

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
    