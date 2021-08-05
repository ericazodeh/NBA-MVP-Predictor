

'''Player class:
Contains all required stats for a given NBA player for a given NBA season
'''
class Player():
    def __init__(self,name='',fg=0.0,three_point=0.0,reb=0.0,ast = 0.0,steal_blocks=0.0,turnover=0.0,pts=0.0,score = 0.0, games = 0.0, threes_attempted = 0.0, losses = 41,team=''):
        self.name = name

        #While data scraping, if any invalid input is found then replace the stat field with a 0
        if fg != '':
            self.fg = float(fg)
        else:
            self.fg = 0.0

        if three_point != '':
            self.three_point = float(three_point)
        else:
            self.three_point = 0.0

        if reb != '':
            self.reb = float(reb)
        else:
            self.reb = 0.0

        if ast != '':
            self.ast = float(ast)
        else:
            self.ast = 0.0

        if steal_blocks != '':
            self.steal_blocks = float(steal_blocks)
        else:
            self.steal_blocks = 0.0

        if turnover != '':
            self.turnover = float(turnover)
        else:
            self.turnover = 0.0

        if pts != '':
            self.pts = float(pts)
        else:
            self.pts = 0.0

        if score != '':
            self.score = float(score)
        else:
            self.score = 0.0

        if games != '':
            self.games = float(games)
        else:
            self.games = 0.0

        if threes_attempted != '':
            self.threes_attempted = float(threes_attempted)
        else:
            self.threes_attempted = 0.0
        #give a player a 41-41 record if an invalid loss stat is found
        if losses != '':
            self.losses = int(losses)
        else:
            self.losses = 41
        #sometimes traded players have multiple entries, so classify them the same
        if team != '':
            self.team = str(team)
        else:
            self.team = 'TOT'


    def test(self):
        string = self.name + "("+ self.team + ")"+",  "+ str(self.pts) + "pts ("+str(round(self.pts*0.75,2)) + "), "+str(self.reb) + " rebounds "+ "("+str(round(self.reb * 1.6,2)) + ")," + str(self.ast) + " asts"+ "("+str(round(self.ast * 1.5,2)) + ")"+", and a defensive score of " + str(round(self.steal_blocks,2)) + "("+str(round(self.steal_blocks * 1.2,2)) + ")"+", eFg of "+str(self.fg) + "("+str(round(5.42 *(self.fg / 0.529),2)) + ")"+" and TS% of "+ str(self.three_point)+ "("+ str(round(5.42 *(self.three_point / 0.524),2))+") with " +str(self.losses)+ " losses("+ str(round(self.losses*-0.3,2)) +") - " + str(self.score) + " points"
        return string
    def debug(self):
        pass
    #returns loss count for a player
    def getLost(self):
        return str(self.losses)
    #compares players by their calculated
    def __lt__(self, other):
        return self.score < other.score

    '''
    This function calculates a player's score after giving multiplier's to a player's
    individual stats based on user input
    '''
    def computeScore(self,q1,q2,q3,q4,q5,q6,q7,q8, losses = 0):
        total = 0.0
        eFg = q1*(5.42 *(self.fg / 0.529))
        three_pct = q2 * (5.42 *(self.three_point / 0.524))
        reb = q3 * self.reb *1.064
        ast = q4 * self.ast * 1.22
        defense =  q5 * self.steal_blocks * 1.2
        tov = q6 * self.turnover * -2.0
        pts = q7 * 0.75 * self.pts
        games = q8 * 5.42 *(self.games / 82.0)
        lossDeductions = float(-0.3 *(losses))

        total += eFg + three_pct + reb + ast + defense + tov + pts + games + lossDeductions
        #if you missed a large amount of games, you get a 5-point score penalty
        if self.games < 65:
            self.score -= 5

        self.score = total




