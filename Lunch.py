from errbot import BotPlugin, botcmd
import random
from datetime import datetime, date


class Lunch(BotPlugin):
    """
    This is a plugin for Lunch Dates. The Idea is to communicate with (new) colleagues.
    For that you add yourself to the participants list for the day. At 11:30 PM Frankie creates random 
    groups(each group 4 Persons). There are two time-slots one at 12:00 and one at 12:20. See **!help lunch_add**
    for details.
    """
    def activate(self):
         super().activate() # activate plugin
         now = datetime.now() # get current time
         if now.minute < 30: # Hint: this will skip == 30
             count= 30 - now.minute # calculate how many minutes are left till 30
             self.start_poller((60 * count) - now.second, self.my_show,times=1) # start poller with (60s * (minutes till 30) - (current time seconds)) and execute only once 
             
         else:
            count= 60 - now.minute # calculate how many minutes are left till 60
            self.start_poller((60 * count) - now.second, self.my_show,times=1) # start poller with (60s * (minutes till 30) - (current time seconds)) and execute only once 
            
         self['participants'] = {} # create each time new dict, don't restore any names
         self['participants20'] = {} # create each time new dict, don't restore any names
         self['poll_started'] = {} # create each time new dict, don't restore 
         self['groups_len'] = {'group':0, 'group20':0} # create each time new dict. Set group participants to 0.


    def get_user_name(self,msgname):
        """
        Get the User name from the message sender id. This function is specific for Mattermost. 
        """
        splitname_rep = str(msgname).replace("/","@") # replace possible "/" with "@", so we can do only one split. 
        splitname = splitname_rep.split("@")[-1] # split and get the last element.
        return ''.join(splitname) # return as string
    
    
    def my_show(self):
        """
        Internal plugin command frequent update of time-slot members. Update is every 30 min
        if executed in a work day and between 9:00 AM and 11:00
        """

        poll_started = self['poll_started'] # copy dictionaries
        groups_len = self['groups_len']
        
        participants_group = self['participants']
        participants_group20 = self['participants20']

        if 'started' not in self['poll_started']: # check if new poll already started
            self.start_poller(60 * 30, self.my_show) # execute every 30 min.
            self.start_poller(60 * 30, self.my_lunch_start) # execute every 30 min.
            poll_started = {'started':1} # remember that poll has started 

        self['poll_started']=poll_started # save dictionary 

        now = datetime.now() # get current time

        if now.weekday() < 5 and now.hour >= 9 and ((now.hour < 11 and now.minute <=30) or (now.hour == 11 and now.minute == 0)):  # check is time is workday and between 9 and 11:00
            group_len = len(participants_group) # get latest number participants  
            group_len20 = len(participants_group20) # get latest number participants in the 12:20 group
            
            if groups_len ['group']  != group_len or groups_len ['group20']  != group_len20: #compare to old values. If new post participants numbers on channel
                self.send( self.build_identifier('~mittagessen'), "Number participants for Group 12:00 is "+str(len(participants_group)), )
                self.send( self.build_identifier('~mittagessen'), "Number participants for Group 12:**2**0 is "+str(len(participants_group20)), )
                groups_len ['group'] = group_len # save new numbers
                groups_len ['group20'] = group_len20 # save new numbers
        self['groups_len'] = groups_len # save dictionary 
    
    @botcmd(split_args_with=None)  # flags a Err command
    def lunch_add(self, msg, args):
        """
        Execute to add yourself to the lunch event for the day
        **!lunch add 20 CP** or **!lunch_add CP 20** adds you to the 12:20 group with desired place: CP
        **!lunch add 20** adds you to the 12:20 group, place wherever
        **!lunch add CP** adds you to the 12:**0**0 group with desired place CP
        **!lunch add** adds you randomly to one group
        """
        partisipant_name = self.get_user_name(msg.frm) # get participant id
        
        participants_group = self['participants']  # copy dictionaries
        participants_group20 = self['participants20']


        if partisipant_name in participants_group or partisipant_name in participants_group20 : # check if participant is already known
            yield partisipant_name+' is already in the List!'
        
        else:
            if not args: # if no args 
                random_add = random.randint(0, 100) # Choose random one integer between 0 and 100
                if random_add % 2  == 0: #if integer modulo 2 = 0 add participant to the 12:00 group, else to the 12:20 
                    participants_group [partisipant_name] = 'Wherever' # set wish Place to don't care 
                    yield 'Added @'+partisipant_name + " to Group 12:00"
                else:
                    participants_group20 [partisipant_name] = 'Wherever' # set wish Place to don't care 
                    yield 'Added @'+partisipant_name + " to Group 12:20"
            else: # if there are arguments
                command_args = args
                if "20" in command_args: # parse if "20" is there. 
                    if len(command_args) == 1: # is "20" the only argument?
                        participants_group20 [partisipant_name] = 'Wherever' # set wish Place to don't care 
                        yield 'Added @'+partisipant_name+", Desired place: Wherever, Time 12:20"
                    elif "20" != command_args[0]: # if there is more than one argument is it the first one? 
                        participants_group20 [partisipant_name] = str(command_args[0]) # set Desired place to arg. 1
                        yield 'Added @'+partisipant_name+", Time 12:20, Desired place: "+ str(command_args[0])
                    else: # set the second argument as Desired place 
                        participants_group20 [partisipant_name] = str(command_args[1])
                        yield 'Added @'+partisipant_name+", Time 12:20, Desired place: "+ str(command_args[1])
                else: # if "20" is not in the arguments
                    participants_group [partisipant_name] = str(command_args[0]) # set Desired place to arg. 0
                    yield 'Added @'+partisipant_name+", Time 12:00, Desired place: "+ str(command_args[0])

        self['participants'] = participants_group # save new dictionary
        self['participants20'] = participants_group20 # save new dictionary
        self['participants'] = participants_group # save new dictionary

        
    
    @botcmd  # flags a Err command
    def lunch_show(self, msg, args):
        """
        Show participants number at the moment
        """
        yield "Number participants for Group 12:00 is "+str(len(self['participants']))
        yield "Number participants for Group 12:20 is "+str(len(self['participants20']))

              
    @botcmd  # flags a Err command
    def lunch_remove(self, msg, args):
        """
        Remove participant from the list
        """
        
        participants_group = self['participants'] # copy dictionaries
        participants_group20 = self['participants20']  # copy dictionaries

        partisipant_name = self.get_user_name(msg.frm) # get participant id
        
        if partisipant_name in participants_group: # check if participant is in the 12:00 group
            del participants_group [partisipant_name] # delete participant from the group
            self['participants'] = participants_group # save new dictionary
            yield partisipant_name+' removed from the List!'
            
        elif partisipant_name in participants_group20: # check if participant is in the 12:20 group
            del participants_group20 [partisipant_name] # delete participant from the group
            self['participants20'] = participants_group20 # save new dictionary
            yield partisipant_name+' removed from the List'
        else: # participant is unknown 
            yield "Identity @"+ partisipant_name + " is unknown!"


    def my_lunch_start(self):
        """
        Internal plugin command for random group generation
        """
        group=1 # group counter in time-slot
        membersInGroup=4 # max. number participants in one group
        participants_group = self['participants'] # copy dictionaries
        participants_group20 = self['participants20'] # copy dictionaries
 
        now = datetime.now() # get current time

        if now.weekday() < 5 and now.hour == 11 and now.minute == 30: # check it is a workday and time is 11:30
            for participant in range(0,len(participants_group)): # loop trough participants in time slot 12:00
                if membersInGroup==4:
                    self.send( self.build_identifier('~mittagessen'), "**12:00 Group {} consists of:**".format(group), )
                    membersInGroup=0 # reset to 0
                    group+=1 # update group
                person, place = random.choice(list(participants_group.items())) # random select person and place
                self.send( self.build_identifier('~mittagessen'), '@'+person + " Desired place: " + place, ) # write to channel
                membersInGroup+=1 # update counter members
                del participants_group [person] # delete participant
                self['participants'] = participants_group # save new dictionary

            group=1 # group counter in time-slot
            membersInGroup=4 # max. number participants in one group
            for participant2 in range(0,len(participants_group20)): # loop trough participants in time slot 12:20
                if membersInGroup==4:
                    self.send( self.build_identifier('~mittagessen'), "**12:20 Group {} consists of:**".format(group), )
                    membersInGroup=0 # reset to 0
                    group+=1 # update group
                person, place = random.choice(list(participants_group20.items())) # random select person and place
                self.send( self.build_identifier('~mittagessen'), '@'+person + " Desired place: " + place, ) # write to channel
                membersInGroup+=1 # update counter members
                del participants_group20 [person] # delete participant
                self['participants20'] = participants_group20 # save new dictionary

       
