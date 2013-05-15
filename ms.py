#!/usr/bin/python

###############################################
# Howard Grimberg/ Aditya Balasubrmanian
# EECS 678 - Intro. To Operating Systems
# Spring 2013 
# Project 3
#
#   Copyright 2013 Howard Grimberg and Aditya Balasubrmanian
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################

from os import listdir, fork, execl
from optparse import OptionParser
from time import sleep
from sys import exit


#Class to contain all information for a given process.
#Contains a PID on which everything is based on.


class Process:
	#Set everything to 0 in constructor
    def __init__(self, pid):
        self.pid = int(pid)
        self.rss = 0
        self.uss = 0
        self.shr = 0
        self.pss = 0
        self.swap = 0
        self.cmd = ''
        self.read();
        return
    #Method to read
    def read(self):
        
		#Using the pid of the object, find its command line representation.
		#Must be sure to have pid(shouldnt be 0)
        cmd_read = open('/proc/' + str(self.pid) + '/cmdline')
        self.cmd = cmd_read.read()
        
		#Open file to read smaps
        mem_read = open('/proc/' + str(self.pid) + '/smaps')
        
		#For each line in the file
        for line in mem_read:
			#Split on the :
			#Format is {Field}:{Value}\n
            line_parse = line.split(':')
			
			#Check if its a value we are looking for
            if(line_parse[0] == 'Rss'):
				#Sum of resident memory
                self.rss = self.rss + int(line_parse[1].strip().strip("kB"))
            elif(line_parse[0] == 'Pss'):
				#Proportional set size memory.
                self.pss = self.pss + int(line_parse[1].strip().strip("kB"))
            elif(line_parse[0] == 'Swap'):
				#Sum of swapped out memory for this process
                self.swap = self.swap + int(line_parse[1].strip().strip("kB"))
            elif(line_parse[0] == 'Shared_Dirty' or line_parse[0] == 'Shared_Clean'):
				#Sum of shared memory for this process
                self.shr = self.shr + int(line_parse[1].strip().strip("kB"))
            elif(line_parse[0] == 'Private_Dirty' or line_parse[0] == 'Private_Clean'):
				#Sum all private memory for this process
                self.uss = self.uss + int(line_parse[1].strip().strip("kB"))
        
        return    

#Class defining processlist
#Contains an associative array mapping
#PIDs to their respective process object
class ProcessList:
    def __init__(self):
        self.processes = {}
        self.updateAll()
        return
    
	#Tells each Process object to read and update itself from procfs
    def updateAll(self):
        pids = self.__getProcessNumbers()
        self.processes.clear()
        for elem in pids:
            self.processes[elem] = Process(elem)
        return
    
	#Get PIDs by scanning /proc for valid numbers
	#Returns a list of PIDs
    def __getProcessNumbers(self):
        proc_fs = listdir('/proc')
        pids = []
        for elem in proc_fs:
            if elem.isdigit():
                pids.append(elem)      
        return pids
      

	  
#Method to get total of memory usage
def showCumulativeTotals(processlist):    
# Get all processes
    meminfo = open('/proc/meminfo', 'r')
	#Similar process to what we did above for reading info.
	#for a single process, only using a differnet file
    for line in meminfo:
        parsed = line.split(':')
        if parsed[0] == 'MemTotal':
            total_mem = parsed[1].strip().strip("kB")
        elif parsed[0] == 'MemFree':
            mem_free = parsed[1].strip().strip("kB")
    shr_sum = 0
    priv_sum = 0
	
	#Sum all shared(dirty or clean) and private(dirty or clean) 
	#Memory for all processes  by chewing on the processllist
    for elem in processlist.values():
        shr_sum = shr_sum + elem.shr
        priv_sum = priv_sum + elem.uss
    mem_in_use = 0
	
	#Calculate memory in use by taking the difference of the total and free memory
    mem_in_use = int(total_mem) - int(mem_free) 
    
	#Format and print a nice table
    base_format = '{0:10}  {1:10}kB'
    print 'Total Usage'
    print base_format.format("Total", total_mem)
   
    print base_format.format("In Use", str(mem_in_use))
    print base_format.format("Free", mem_free)
    print base_format.format("Shared", str(shr_sum)) 
    print base_format.format("Nonshared", str(priv_sum))    
    
    
    return


    

def main(*args, **kwargs):

	#Stuff to handle arguments
	#DEPRECATED IN PYTHON 2.7
    parser = OptionParser()
    parser.add_option("-s", "--sort", dest="sort", default="rss-",
                  help="Column and direction to sort table", type="string")
    
   
    
    
    (options, args) = parser.parse_args()
  
    #Determine the sort order
    if(options.sort.find("-") == -1):
        descending = False
    else:
        descending = True
	#Build are of our information
    plist = ProcessList()    
	
	#Figure our what column to sort on by stripping
	#the existent - character
    to_sort = options.sort.strip('-')
	
	#Figure out what column to sort on and do sort, returning a tuple
    if(to_sort == 'rss'):
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].rss, reverse=descending)
    elif(to_sort == 'shr'):
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].shr, reverse=descending)
    elif(to_sort == 'swap'):  
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].swap, reverse=descending)
    elif(to_sort == 'pid'):  
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].pid, reverse=descending)
    elif(to_sort == 'uss'):
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].uss, reverse=descending)
    elif(to_sort == 'pss'):
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].pss, reverse=descending)
    elif(to_sort == 'cmd'):   
        plist_tuple_sorted = sorted(plist.processes.items(), key=lambda val: val[1].cmd, reverse=descending)
    else:
        print '*** ERROR:Invalid Column Name'
        return
		
	#Show cumulative totals
    showCumulativeTotals(plist.processes)
	
	#Set table formating
    base_format = "{0:10} {1:10} {2:10} {3:10} {4:10} {5:10} {6:32}"
	
	#Print Table Header
    header = base_format.format("PID", "USS", "PSS", "SWAP", "RES", "SHR", "CMD")
    print header;
 
	#Print each value in process list
    for pcess in plist_tuple_sorted:
        line = base_format.format(pcess[0], pcess[1].uss, pcess[1].pss, pcess[1].swap, pcess[1].rss, pcess[1].shr, pcess[1].cmd)
        print line

        
    return

 
#Dont mind me, I just like to think I have a main function. 
main()     
        
        
