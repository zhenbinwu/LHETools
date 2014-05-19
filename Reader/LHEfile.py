import ROOT as rt

class LHEfile():
    
    def __init__(self, fileINname):
        self.eventList = []
        self.fileINname = fileINname
        self.MaxEv = -99
        self.fileIN = 0

    def setMax(self, maxVal):
        self.Max = maxVal
        
    def readEvents(self):
        if ".gz" in self.fileINname:
            import gzip
            self.fileIN = gzip.open(self.fileINname, 'r')
        else:
            self.fileIN = open(self.fileINname)
        newEVENT = False
        oneEvent = []
        for line in self.fileIN:
            if newEVENT: oneEvent.append(line)
            if line.find("</event>") != -1:
                # the event block ends
                newEVENT = False
                self.eventList.append(oneEvent)
                oneEvent = []
                if len(self.eventList) >= self.Max and self.Max>0: break
            if line.find("<event>") != -1:
                # the event block starts
                newEVENT = True
                oneEvent.append(line)
        self.fileIN.close()
        return self.eventList
