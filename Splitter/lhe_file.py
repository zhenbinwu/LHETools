#!/usr/bin/env python

import sys, string
from xml.dom import minidom, Node

class lhe_file(object):

    def __init__(self, filename, write=False):

        if write:
            self.lhe_file = open(filename, 'w')
        else:
            self.lhe_file = open(filename, 'r')

        self.header = self._get_header()
        self.init = self._get_init()
        self.n_events = self._count_events()
        
    def _get_header(self):

        self.lhe_file.seek(0) # roll back to the beginning
        self.lhe_file.next() # skip one line
        
        header = ''

        while True:
            line = self.lhe_file.next()
            header += line
            
            if line == '</header>\n':
                break

        doc = minidom.parseString(header)

	
        return doc.documentElement

    def _get_init(self):
        self._get_header() # takes us past the header 

        init = ''

        while True:
            line = self.lhe_file.next()
            init += line
            
            if line == '</init>\n':
                break


        doc = minidom.parseString(init)

        return doc.documentElement

    def _get_event(self, i):
        self._get_init() # takes us to the first event

        count = 0

        event = self._get_next_event()
        
        while count < i:
            event = self._get_next_event()
            count += 1

        return event

    def _get_next_event(self):

        event = ''
        
        while True:
            line = self.lhe_file.next()
            event+=line
                
            if line == "</event>\n":
                return event

    def _count_events(self):
        count = 0

        self._get_init() # get ready to read first event
        
        try:
            while True:
                self._get_next_event()
                count += 1
        except StopIteration:
            self._get_init() # roll back to first event
            return count

        self._get_init() # roll back to first event
        return count

    def next(self):
        return self._get_next_event()



class lhe_event(object):
    ''' Describes an event in LHE format '''
    

#    self.raw_event = str(raw_event)
#    self.element = minidom.parseString(self.raw_event)

        

    def get_n_particles(self):
        lines = self.raw_event.spltlines()
        first_line = lines[1]

        match = proc_matcher(first_line)

        return int(match(1))
            

    def __str__(self):
        #return self.element.toxml()
        return self.raw_event

    def __init__(self, raw_event):
        
        self.raw_event = str(raw_event)
        


if __name__=="__main__":

    import sys

    

    input_file = sys.argv[1]

    foo = lhe_file(input_file)

    print foo.header.toxml()
    print foo.init.toxml()
    print "file has %d events" % foo.n_events