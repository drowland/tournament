#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
import random

# set tournament ID to 1 for all test functions
tourn_id = 1

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers(tourn_id)
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers(tourn_id)
    c = countPlayers(tourn_id)
    if c == '0':
        raise TypeError(
            "countPlayers(tourn_id) should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers(tourn_id) returns zero."

def testRegisterTournament():
    deleteMatches()
    deletePlayers(tourn_id)
    registerPlayer("Paul Casey", tourn_id)
    registerPlayer("Ian Poulter", tourn_id)
    registerPlayer("Rory McIlory", tourn_id)
    registerPlayer("Dustin Johnson")
    registerPlayer("Jordan Spieth", tourn_id)
    c = countPlayers(tourn_id)
    if c != 4:
        raise ValueError(
            "After adding 5 players but registering 4, countPlayers(tourn_id) should be 4.")
    print "4. After registering 4 players for a specific tournament, countPlayers(tourn_id) returns 4."

def testRegisterCountDelete():
    deleteMatches()
    deletePlayers(tourn_id)
    registerPlayer("Markov Chaney", tourn_id)
    registerPlayer("Joe Malik", tourn_id)
    registerPlayer("Mao Tsu-hsi", tourn_id)
    registerPlayer("Atlanta Hope", tourn_id)
    c = countPlayers(tourn_id)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers(tourn_id)
    c = countPlayers(tourn_id)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers(tourn_id)
    registerPlayer("Melpomene Murray", tourn_id)
    registerPlayer("Randy Schwartz", tourn_id)
    standings = playerStandings(tourn_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers(tourn_id)
    registerPlayer("Bruno Walton", tourn_id)
    registerPlayer("Boots O'Neal", tourn_id)
    registerPlayer("Cathy Burton", tourn_id)
    registerPlayer("Diane Grant", tourn_id)
    standings = playerStandings(tourn_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tourn_id, id1, id2)
    reportMatch(tourn_id, id3, id4)
    standings = playerStandings(1)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testOddTeams():
    this_tourn_id = 2
    deleteMatches()
    deletePlayers()
    registerPlayer("Dustin Johnson", this_tourn_id)
    registerPlayer("Justin Rose", this_tourn_id)
    registerPlayer("Jason Day", this_tourn_id)
    registerPlayer("Adam Scott", this_tourn_id)
    registerPlayer("Rory McIlroy", this_tourn_id)
    registerPlayer("Ian Poulter", this_tourn_id)
    registerPlayer("Martin Kayner", this_tourn_id)
    registerPlayer("Phil Mickelson", this_tourn_id)
    registerPlayer("Sergio Garcia", this_tourn_id)
    standings = playerStandings(this_tourn_id)
    if len(standings) != 9:
        raise ValueError(
            "There should be 9 players registered for this tournament")

    for x in xrange(0,3):
        pairings = swissPairings(this_tourn_id)

        if len(pairings) !=5:
            raise ValueError(
                "There should be 5 pairings defined")
        
        
        for pair in pairings:
            # randomly choose a winner for each match
            first_team_wins = random.choice([True, False])
            if first_team_wins or pair[2]==None:
                reportMatch(this_tourn_id,pair[0],pair[2])
                print('Reporting: %s (W) | %s (L)' % (pair[1],pair[3]))
            else:
                reportMatch(this_tourn_id,pair[2],pair[0])
                print('Reporting: %s (W) | %s (L)' % (pair[3],pair[1]))

        standings = playerStandings(this_tourn_id)
        for player in standings:
            print('Player: %s (%s): %s wins | %s matches' 
                % (player[1], player[0], player[2], player[3]))
        x += 1

def testPairings():
    deleteMatches()
    deletePlayers(tourn_id)
    registerPlayer("Twilight Sparkle", tourn_id)
    registerPlayer("Fluttershy", tourn_id)
    registerPlayer("Applejack", tourn_id)
    registerPlayer("Pinkie Pie", tourn_id)
    standings = playerStandings(tourn_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tourn_id, id1, id2)
    reportMatch(tourn_id, id3, id4)
    pairings = swissPairings(tourn_id)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegisterTournament()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testOddTeams()
    print "Success!  All tests pass!"