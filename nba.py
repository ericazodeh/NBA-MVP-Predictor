import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from Analytics import Player


#use this to find the mvp from multiple seasons
def getMultipleYears(list):
    for i in range(len(list)):
        get_NBA_stats(list[i])
#note: you can also use your OWN criteria of what an MVP should be by uncommenting the q1_var, q2_var,etc. variables in the get_NBA_stats function
#this function calculates the weight of your criteria
def convertResponse(res):
    if res < 0 or res > 10:
        print("Error: Number needs to be greater than 0 and less than 10. Restart program")
        return 0
    if res == 0:
        return 0
    elif res < 5:
        return res - 6.0
    elif res >= 5:
        return res - 4
#finds loss count of a team for a given year
def getLossCount(team,year):
    if team == 'TOT':
        team = 'BRK'
    url = 'https://www.basketball-reference.com/teams/{}/{}.html'.format(team,year)
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html, features="html.parser")
    #use REGEX to get losses
    record = (soup(text=re.compile('\n    \n      [0-9]')))
    if(len(record) == 0):
        return 10
    txt = record[0]

    x = re.findall("[0-9][0-9]*", txt)

    '''if year != 2021:
        x = re.findall("[0-9][0-9]", txt)
        #print(x)
    else:
       # x = re.findall("[0-9]", txt)
        #print(x)
        return 0
'''
    #when a team has less then 10 losses (the Warriors in 2016, Chicago Bulls in 1996, or the start of season) REGEX messes up
    if len(x) < 2:
        return 82 - int(x[0])
    return int(x[1])

#this function finds the ACTUAL MVP for that year to compare against program results
def statTest():
    url = "https://www.basketball-reference.com/awards/mvp.html"

    text = requests.get(url).text

    soup = BeautifulSoup(text,"html.parser")

    table = soup.find_all(class_="table_container")
    #print("Table print")
    #print(table)
    players= []
    for i in range(len(table)):

        player_ = []
        #print("Printing in table...")
        for td in table[i].find_all("td"):

           # print(td.text)
            player_.append(td.text)
            #print(player_)
        count = 0
        players.append(player_)
    #print(players)
    return players




'''Main function
1. BasketballReferencce.com holds tables each year of every NBA players stats for that given year
2. Get that page and Web Scrape the table
3. Load each players data from a row into the Player class created in Analytics.py
4. Compute each players score based off an accumalation of points, rebounds, assists, wins, defense, shooting %, e.t.c.
5. Sort players from the highest scoring to the lowest scoring
6. Display the top 10 leading players

'''
def get_NBA_stats(yr):

    statTest()
    #year=input("Which NBA season are you interested in?: ")
    #year = 2006
    year = yr
    #player=input("For which player do you want to get stats?: ")
    player = "LeBron James"
    #print("Answer these questions on a scale of 1 to 10. Please answer with a 0 if you do not feel the statistic should be included!")
   # q1_var = float(input("Importance of a player's efficiency in shooting the ball: "))
    q1_var = convertResponse(5)
    q1 = 1 + 2*q1_var / 100.0 if (q1_var != 0) else 0.0
   # q2_var = float(input("Importance of a player's efficiency in scoring: "))
    q2_var = convertResponse(5)
    q2 = 1 + 2*q2_var / 100.0 if (q2_var != 0) else 0.0
    #q3_var = float(input("Importance of a player's rebounds: "))
    q3_var = convertResponse(5)
    q3 = 1 + 2*q3_var / 100.0 if (q3_var != 0) else 0.0
    #q4_var = float(input("Importance of a player's assists: "))
    q4_var = convertResponse(5)
    q4 = 1 + 3*q4_var / 100.0 if (q4_var != 0) else 0.0
   # q5_var = float(input("Importance of a player's defense: "))
    q5_var = convertResponse(5)
    q5 = 1 + 3*q5_var / 100.0 if (q5_var != 0) else 0.0
   # q6_var = float(input("Importance of a player's ability to limit turnovers: "))
    q6_var = convertResponse(5)
    q6 = 1 + 3*q6_var / 100.0 if (q6_var != 0) else 0.0
    #q7_var = float(input("Importance of a player's scoring ability: "))
    q7_var = convertResponse(5)
    q7 = 1 + 15*q7_var / 100.0 if (q7_var != 0) else 0.0
    #q8_var = float(input("Importance of a player's durability (i.e. ability to play every possible game without getting injured/sitting out: "))
    q8_var = convertResponse(5)
    q8 = 1 + 3*q8_var / 100.0 if (q8_var != 0) else 0.0

    url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(year)
    url1 = 'https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'.format(year)

    r = requests.get(url)
    r1 = requests.get(url1)

    r_html = r.text
    r_html1 = r1.text


    soup = BeautifulSoup(r_html, 'html.parser')
    soup1 = BeautifulSoup(r_html1,'html.parser')

    table = soup.find_all(class_="full_table")
    table1 = soup1.find_all(class_ = "full_table")

    """ Extracting List of column names"""
    head = soup.find(class_="thead")
    head1 = soup1.find(class_ = "thead")
    column_names_raw = [head.text for item in head][0]

    column_names_raw1 = [head1.text for item1 in head1][0]
    column_names_polished = column_names_raw.replace("\n", ",").split(",")[2:-1]
    column_names_polished1 = column_names_raw1.replace("\n", ",").split(",")[2:-1]
    column_names_polished.append('TS%')

    '''for i in range(len(column_names_polished1)):
       print(column_names_polished[i] + ' '+ str(i))
    print("--------------------------------------------------")
    for i in range(len(column_names_polished1)):
       print(column_names_polished1[i] + ' '+ str(i))'''
    """Extracting full list of player_data"""
    players = []
    nba_list = []

    for i in range(len(table)):

        player_ = []
        for td in table[i].find_all("td"):

            player_.append(td.text)

        count = 0
        for td1 in table1[i].find_all("td"):
            if count != 7:
                count += 1
                continue
            else:
                player_.append(td1.text)
                break

        players.append(player_)


        df = pd.DataFrame(players, columns=column_names_polished).set_index("Player")
        # cleaning the player's name from occasional special characters
        df.index = df.index.str.replace('*', '')

    for i in range(len(players)):
        p = players[i]

        if float(p[28]) < 13.7:
            continue
        person = Player(p[0],p[16],p[29],p[22],p[23],float(p[24]) + float(p[25]),p[26],p[28],0.0,p[4],p[11],0,p[3])
        name = p[0]
        fg = p[16]
        three_point = p[29]
        reb = p[22]
        ast = p[23]

        tov = p[26]
        pts = p[28]
        score = 0.0
        games = p[4]
        threeAttempts = p[11]
        losses = 0
       # p[3]
        #print("losses " + person.getLost())

        person.computeScore(q1,q2,q3,q4,q5,q6,q7,q8)
        nba_list.append(person)

    nba_list.sort()
    topTwentyCandidates = nba_list[(len(nba_list)-10):len(nba_list)]

    ''' for player in topTwentyCandidates:
        if yr != 1976:
            if player.losses > 36:
                topTwentyCandidates.remove(player)
        else:
            if player.losses > 42:
                topTwentyCandidates.remove(player)'''




    for i in range(len(topTwentyCandidates)):
        topTwentyCandidates[i].losses = getLossCount(topTwentyCandidates[i].team,yr)
        #print(topTwentyCandidates[i].losses)
        topTwentyCandidates[i].computeScore(q1,q2,q3,q4,q5,q6,q7,q8,topTwentyCandidates[i].losses)



    topTwentyCandidates.sort()

    print("Top 10 Calculated MVP Candidates")
    print(str(int(year) - 1) + "-" + str(int(year)))
    #print(len(topTwentyCandidates))
    for i in range(len(topTwentyCandidates)-1,len(topTwentyCandidates)-11, -1):
        print(str(10-i) +". " +topTwentyCandidates[i].test())

    #print(statTest()[0][1+((2020-yr)*17)])
    total = 0
    secondPlace = 0
    mvp = statTest()[0][1+((2020-yr)*17)]

    '''if str(mvp) in str(topTwentyCandidates[9].name) or str(topTwentyCandidates[9].name) in str(mvp):
        print("yes")
        total +=1
        secondPlace += 1

    elif str(mvp) in str(topTwentyCandidates[8].name) or str(topTwentyCandidates[8].name) in str(mvp):
        print("2nd")
        secondPlace += 1

    else:
        print("no")
        print(mvp)'''

    '''li = []
    li.append(total)
    li.append(secondPlace)'''

    return

    '''if __name__ == "__main__":
        get_NBA_stats()'''


#sum1 = 0
#sum2 = 0
'''for i in range(2021,1974,-1):
  var = get_NBA_stats(i)
  sum1 += var[0]
  sum2 += var[1]'''

#print(getLossCount('MIN',2005))
#p.debug()
#print(sum1/46.0)
#print(sum2/46.0)



year= int(input("Which year would you like the program to predict the MVP (1974-2021): "))
get_NBA_stats(year)



