# -*- coding: utf-8 -*-
'''
Entelect StarterBot for Python3
'''
import time

startTime = time.time()

import json
import os
from time import sleep
import random


    
    
class StarterBot:
    
    def __init__(self,state_location):
        '''
        Initialize Bot.
        Load all game state information.
        '''
        try:
            self.game_state = self.loadState(state_location)
        except IOError:
            print("Cannot load Game State")
            
        self.full_map = self.game_state['gameMap']
        self.rows = self.game_state['gameDetails']['mapHeight']
        self.columns = self.game_state['gameDetails']['mapWidth']
        self.command = ''
        
        self.player_buildings = self.getPlayerBuildings()
        self.opponent_buildings = self.getOpponentBuildings()
        self.projectiles = self.getProjectiles()
        
        self.player_info = self.getPlayerInfo('A')
        self.opponent_info = self.getPlayerInfo('B')
        
        self.round = self.game_state['gameDetails']['round']
        
        self.buildings_stats = {"ATTACK":{"health": self.game_state['gameDetails']['buildingsStats']['ATTACK']['health'],
                                 "constructionTime": self.game_state['gameDetails']['buildingsStats']['ATTACK']['constructionTime'],
                                 "price": self.game_state['gameDetails']['buildingsStats']['ATTACK']['price'],
                                 "weaponDamage": self.game_state['gameDetails']['buildingsStats']['ATTACK']['weaponDamage'],
                                 "weaponSpeed": self.game_state['gameDetails']['buildingsStats']['ATTACK']['weaponSpeed'],
                                 "weaponCooldownPeriod": self.game_state['gameDetails']['buildingsStats']['ATTACK']['weaponCooldownPeriod'],
                                 "energyGeneratedPerTurn": self.game_state['gameDetails']['buildingsStats']['ATTACK']['energyGeneratedPerTurn'],
                                 "destroyMultiplier": self.game_state['gameDetails']['buildingsStats']['ATTACK']['destroyMultiplier'],
                                 "constructionScore": self.game_state['gameDetails']['buildingsStats']['ATTACK']['constructionScore']},
                       "DEFENSE":{"health": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['health'],
                                 "constructionTime": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['constructionTime'],
                                 "price": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['price'],
                                 "weaponDamage": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['weaponDamage'],
                                 "weaponSpeed": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['weaponSpeed'],
                                 "weaponCooldownPeriod": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['weaponCooldownPeriod'],
                                 "energyGeneratedPerTurn": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['energyGeneratedPerTurn'],
                                 "destroyMultiplier": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['destroyMultiplier'],
                                 "constructionScore": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['constructionScore']},
                       "ENERGY":{"health": self.game_state['gameDetails']['buildingsStats']['ENERGY']['health'],
                                 "constructionTime": self.game_state['gameDetails']['buildingsStats']['ENERGY']['constructionTime'],
                                 "price": self.game_state['gameDetails']['buildingsStats']['ENERGY']['price'],
                                 "weaponDamage": self.game_state['gameDetails']['buildingsStats']['ENERGY']['weaponDamage'],
                                 "weaponSpeed": self.game_state['gameDetails']['buildingsStats']['ENERGY']['weaponSpeed'],
                                 "weaponCooldownPeriod": self.game_state['gameDetails']['buildingsStats']['ENERGY']['weaponCooldownPeriod'],
                                 "energyGeneratedPerTurn": self.game_state['gameDetails']['buildingsStats']['ENERGY']['energyGeneratedPerTurn'],
                                 "destroyMultiplier": self.game_state['gameDetails']['buildingsStats']['ENERGY']['destroyMultiplier'],
                                 "constructionScore": self.game_state['gameDetails']['buildingsStats']['ENERGY']['constructionScore']}}
        return None
    def getFirstDefensePosition(self,lane):
        '''
        Returns index of first defense building
        '''
        for i in range(len(lane)):
            if lane[i] == 0 :
                return i 
    def checkIfOccupied(self,row):
        if (self.full_map[row][0]['buildings'][0]['buildingType'] == 'ENERGY'):
            return True
        else:
            return False
    def loadState(self,state_location):
        '''
        Gets the current Game State json file.
        '''
        return json.load(open(state_location,'r'))

    def getPlayerInfo(self,playerType):
        '''
        Gets the player information of specified player type
        '''
        for i in range(len(self.game_state['players'])):
            if self.game_state['players'][i]['playerType'] == playerType:
                return self.game_state['players'][i]
            else:
                continue        
        return None
    
    def getOpponentBuildings(self):
        '''
        Looks for all buildings, regardless if completed or not.
        0 - Nothing
        1 - Attack Unit
        2 - Defense Unit
        3 - Energy Unit
        '''
        opponent_buildings = []
        
        for row in range(0,self.rows):
            buildings = []
            for col in range(int(self.columns/2),self.columns):
                if (len(self.full_map[row][col]['buildings']) == 0):
                    buildings.append(0)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ATTACK'):
                    buildings.append(1)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'DEFENSE'):
                    buildings.append(2)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ENERGY'):
                    buildings.append(3)
                else:
                    buildings.append(0)
                
            opponent_buildings.append(buildings)
            
        return opponent_buildings
    
    def getPlayerBuildings(self):
        '''
        Looks for all buildings, regardless if completed or not.
        0 - Nothing
        1 - Attack Unit
        2 - Defense Unit
        3 - Energy Unit
        '''
        player_buildings = []
        
        for row in range(0,self.rows):
            buildings = []
            for col in range(0,int(self.columns/2)):
                if (len(self.full_map[row][col]['buildings']) == 0):
                    buildings.append(0)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ATTACK'):
                    buildings.append(1)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'DEFENSE'):
                    buildings.append(2)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ENERGY'):
                    buildings.append(3)
                else:
                    buildings.append(0)
                
            player_buildings.append(buildings)
            
        return player_buildings
    
    def getProjectiles(self):
        '''
        Find all projectiles on the map.
        0 - Nothing there
        1 - Projectile belongs to player
        2 - Projectile belongs to opponent
        '''
        projectiles = []
        
        for row in range(0,self.rows):
            temp = []
            for col in range(0,self.columns):
                if (len(self.full_map[row][col]['missiles']) == 0):
                    temp.append(0)
                elif (self.full_map[row][col]['missiles'][0]['playerType'] == 'A'):
                    temp.append(1)
                elif (self.full_map[row][col]['missiles'][0]['playerType'] == 'B'):
                    temp.append(2)
                
            projectiles.append(temp)
            
        return projectiles

    def checkDefense(self, lane_number):

        '''
        Checks a lane.
        Returns True if lane contains defense unit.
        '''
        
        lane = list(self.opponent_buildings[lane_number])
        if (lane.count(2) > 0):
            return True
        else:
            return False

    def checkEnergy(self, lane_number):
        '''
            Check if there is any energy stations on the lane
        '''
        lane = list(self.opponent_buildings[lane_number])
        if (lane.count(3) > 0):
            return True
        else:
            return False

    def checkMyEnergy(self, lane_number):
        '''
            Check if there is any energy stations on the lane (self)
        '''
        lane = list(self.player_buildings[lane_number])
        if (lane.count(3) > 0):
            return True
        else:
            return False
           
    def checkMyDefense(self, lane_number):

        '''
        Checks a lane.
        Returns True if lane contains defense unit.
        '''
        
        lane = list(self.player_buildings[lane_number])
        if (lane.count(2) > 0):
            return True
        else:
            return False
    
    def checkAttack(self, lane_number):
        '''
        Checks a lane.
        Returns True if lane contains attack unit.
        '''
        lane = list(self.opponent_buildings[lane_number])
        if (lane.count(1) > 0):
            return True
        else:
            return False

    def checkMyAttack(self, lane_number):
        '''
        Checks a lane.
        Returns True if lane contains attack unit.
        '''
        lane = list(self.player_buildings[lane_number])
        if (lane.count(1) > 0):
            return True
        else:
            return False
    
    def getUnOccupied(self,lane):
        '''
        Returns index of all unoccupied cells in a lane
        '''
        indexes = []
        for i in range(len(lane)):
            if lane[i] == 0 :
                indexes.append(i)
        
        return indexes
                
    def generateAction(self):
        '''
        Place your bot logic here !
        
        - If there is an opponent attack unit on a row, and you have enough energy for a defense
             Build a defense at a random unoccupied location on that row if it is undefended.
        - Else If you have enough energy for the most expensive building 
             Build a random building type at a random unoccupied location
        - Else: 
             Save energy until you have enough for the most expensive building
             
        Building Types :
            0 : Defense Building
            1 : Attack Building
            2 : Energy Building
        '''        
        x,y,building = 0,0,0
        #check all lanes for an attack unit
        lanes = []
        
        for i in range(self.rows):
            if len(self.getUnOccupied(self.player_buildings[i])) == 0:
                #cannot place anything in a lane with no available cells.
                continue
            elif ( self.checkAttack(i) and (self.player_info['energy'] >= self.buildings_stats['DEFENSE']['price']) and (self.checkMyDefense(i)) == False):
                #place defense unit if there is an attack building and you can afford a defense building
                lanes.append(i)

        #lanes variable will now contain information about all lanes which have attacking units
        #A count of 0 would mean all lanes are not under attack
        
      
        if len(lanes) > 0 and self.player_info['energy'] >= max(self.buildings_stats['ATTACK']['price'], self.buildings_stats['DEFENSE']['price']):
            for row in range(0,self.rows):
                '''plant defense if under attack'''
                if   (self.checkAttack(row)    == True and self.checkMyDefense(row) == False) and (self.getUnOccupied(lanes).__contains__(row) == False):
                    y = row
                    x = 3
                    building = 0
                elif (self.checkMyAttack(row)  == False and self.checkMyDefense(row) == True)  and (self.getUnOccupied(lanes).__contains__(row) == False):
                    '''plant attack behind defense'''
                    y = row
                    x = 1
                    building = 1
                elif (self.checkMyDefense(row) == False)  and self.getUnOccupied(self.player_buildings[row]).__contains__(row) == False:
                    y = row
                    x = 4
                    building = 0
        elif self.player_info['energy'] >= max(self.buildings_stats['DEFENSE']['price'],self.buildings_stats['ATTACK']['price'])  :
            for row in range(0,self.rows):
                if self.player_info['energy'] >= self.buildings_stats['ATTACK']['price'] and self.getPlayerBuildings().count(1) <  3  and (self.getUnOccupied(lanes).__contains__(row) == False):
                        if (self.checkMyAttack(row) == False)  :
                            y = row
                            x = 2
                            building = 1
        elif  self.player_info['energy'] >= self.buildings_stats['ENERGY']['price'] :
            for row in range(0,self.rows):
                '''plant energy if not enough energy''' 
                if (self.checkMyEnergy(row) == False )  and (self.getUnOccupied(lanes).__contains__(row) == False):
                        y = row 
                        x = 0
                        building = 2  
                elif(self.checkMyEnergy(row) == False )  and (self.getUnOccupied(lanes).__contains__(row) == False) :
                        y = row 
                        x = 0
                        building = 2  

        else :
            self.logAction('round : ' + str(self.round) + '    '+ str(x)  + ',' + str(y) + 'Do Nothing')
            self.writeDoNothing()
            return None


        if(x < 7) and (y < self.columns) and (building  < 3):
            self.writeCommand(x,y,building)
            self.logAction('round : ' + str(self.round) + '    '+ str(x)  + ',' + str(y) + 'building : ' + str(building)  )
            return x,y,building
        else:
            self.logAction('round : ' + str(self.round) + '    '+ str(x)  + ',' + str(y) + 'Do Nothing')
            self.writeDoNothing()
            return None

    def writeCommand(self,x,y,building):
        '''
        command in form : x,y,building_type
        '''
        outfl = open('command.txt','w')
        outfl.write(','.join([str(x),str(y),str(building)]))
        outfl.close()
        return None

    def logAction(self,message):
        '''
        logs data onto a text file 
        '''
        outf2 = open('action_log.txt','a')
        outf2.write(message + '\n')
        outf2.close()
        return None

    def getLanes(self):
        
        lanes = []

        for i in range(self.rows):
            if len(self.getUnOccupied(self.player_buildings[i])) == 0:
                #cannot place anything in a lane with no available cells.
                continue
            elif ( self.checkAttack(i) and (self.player_info['energy'] >= self.buildings_stats['DEFENSE']['price']) and (self.checkMyDefense(i)) == False):
                #place defense unit if there is an attack building and you can afford a defense building
                lanes.append(i)

        return lanes
    def writeDoNothing(self):
        '''
        command in form : x,y,building_type
        '''
        outfl = open('command.txt','w')
        outfl.write("")
        outfl.close()
        return None

if __name__ == '__main__':
    s = StarterBot('state.json')
    s.generateAction()

    

    