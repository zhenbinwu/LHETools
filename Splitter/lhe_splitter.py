#!/usr/bin/env python

import sys, string, itertools, sre, gzip

#from segment_list import segment_list
from lhe_file import lhe_file 
from sets import Set


class event_getter(object):

    def __init__(self,lhe_file_list):

        
        self._lhe_file_list = []

        for i in Set(lhe_file_list): # remove duplicates
            self._lhe_file_list.append(lhe_file(i))

        self.n_events = 0
        self.reset()

    def reset(self):
        self.input_files = itertools.chain(self._lhe_file_list)
        self._current_file = self.input_files.next()
        self.n_events = self._count()
        
    def get_next_event(self):

        try:
            event = self._current_file.next()
        except StopIteration:
            self._current_file = self.input_files.next()
            event = self._current_file.next()
        return event

    def get_current_header(self):
        return self._current_file.header.toxml()
    def get_current_init(self):
        return self._current_file.init.toxml()

    def _count(self):
        n_total = 0

        try:
            while True:
                n_total += self._current_file.n_events
                self._current_file = self.input_files.next()
        except StopIteration:
            self.input_files = itertools.chain(self._lhe_file_list)
            self._current_file = self.input_files.next()
            
        return n_total

    

def split_lhe_file(segments, input_file_list, outname):

    #dsid = matcher.group(1)
    
    #segmentList = segment_list(segments)
    
    getter = event_getter(input_file_list) 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Events per file ~~~~~
    n_events_needed = int(segments)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Total events  ~~~~~
    n_events_total = getter.n_events

    print "%d events required per file" % n_events_needed

    print "%d events in these files:" % n_events_total

    for i in input_file_list:
        print ('\t %s' % i)
    

    if  n_events_total < n_events_needed:
        n_events_needed = n_events_total
        #print "not enough events! exiting!"
        #sys.exit(-1)


    for segment in range(n_events_total/ n_events_needed):


        segment_number = segment
        n_events = n_events_needed
        
        header = getter.get_current_header()
        init = getter.get_current_init()

        outfile_name = "%s_%d.lhe" % (outname, segment_number)
        
        outfile = open( outfile_name, 'w')

        outfile.write('<LesHouchesEvents version="1.0">\n')

        outfile.write(header)
        outfile.write('\n')
        outfile.write(init)
        outfile.write('\n')
        
        for i in range(n_events):
            event = getter.get_next_event()
            outfile.write(event)
            
        outfile.write('</LesHouchesEvents>\n')
        outfile.close()
        


def main():
    args = sys.argv[1:]
    segments = args[0]
    outname = args[1]
    lhe_files = args[2:]
    
    split_lhe_file(segments, lhe_files, outname)

if __name__ == '__main__':
    main()
