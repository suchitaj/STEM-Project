__author__ = 'divya'

"""
Parser for GO Ontology obo file to query for
parents for any GO term
Reference: http://blog.nextgenetics.net/?e=6
"""
class go_obo_parser(object):

    def __init__(self):
        self.terms = {} #Dictionary to hold go ids


    def getTerm(self, stream):
        """
        Helper method in parsing GO obo file
        """
        block = []
        for line in stream:
            if line.strip() == "[Term]" or line.strip() == "[Typedef]":
                break
            else:
                if line.strip() != "":
                    block.append(line.strip())

        return block

    def parseTagValue(self, term):
        """
        Helper method in parsing GO obo file
        """
        data = {}
        for line in term:
            tag = line.split(': ',1)[0]
            value = line.split(': ',1)[1]
            #if not data.has_key(tag):
            if not tag in data:
                data[tag] = []

            data[tag].append(value)

        return data

    def parseOBO(self, inp_obo_file):
        """
        Method to parse a GO ontology obo file and create parent child relationships
        """

        oboFile = open(inp_obo_file,'r')

        #skip the file header lines
        self.getTerm(oboFile)

        #infinite loop to go through the obo file.
        #Breaks when the term returned is empty, indicating end of file
        while 1:
          #get the term using the two parsing functions
          term = self.parseTagValue(self.getTerm(oboFile))
          if len(term) != 0:
            termID = term['id'][0]
            #print(str(termID))

            #only add to the structure if the term has a is_a tag
            #the is_a value contain GOID and term definition
            #we only want the GOID
            if 'is_a' in term:
              termParents = [p.split()[0] for p in term['is_a']]

              if not termID in self.terms:
                #each goid will have two arrays of parents and children
                self.terms[termID] = {'p':[],'c':[]}

              #append parents of the current term
              self.terms[termID]['p'] = termParents

              #for every parent term, add this current term as children
              for termParent in termParents:
                if not termParent in self.terms:
                  self.terms[termParent] = {'p':[],'c':[]}
                self.terms[termParent]['c'].append(termID)

            if 'relationship' in term:
                termParents = [p.split()[1] for p in term['relationship']]
                if not termID in self.terms:
                    #each goid will have two arrays of parents and children
                    #self.terms[termID] = {'p':[],'c':[]}
                    self.terms[termID] = {'p':[],'c':[]}

                #for every parent term, add this current term as children
                for termParent in termParents:
                    #print(str(termParent))

                    if not termParent in self.terms:
                        self.terms[termParent] = {'p':[],'c':[]}
                    self.terms[termParent]['c'].append(termID)

                    #append parents of the current term
                    self.terms[termID]['p'].append(termParent)

          else:
            break


    def get_immediate_parent(self, go_term):
        """
        Method to get immediate parent of a GO term
        """
        parent = self.terms[go_term]['p']

    def get_immediate_child(self, go_term):
        """
        Method to get immediate children of a Go term
        """
        children = self.terms[go_term]['c']

    def getDescendents(self, goid):
        """
        Method to get all descendents of a GO terms in the GO ontology graph
        """
        recursiveArray = [goid]
        if goid in self.terms:
            children = self.terms[goid]['c']
            if len(children) > 0:
                for child in children:
                    recursiveArray.extend(self.getDescendents(child))

        return set(recursiveArray)

    def getAncestors(self, goid):
        """
        Method to get all ancestors of a GO term in the GO ontology graph
        """
        recursiveArray = [goid]
        if goid in self.terms:
            parents = self.terms[goid]['p']
            if len(parents) > 0:
                for parent in parents:
                    recursiveArray.extend(self.getAncestors(parent))

        return set(recursiveArray)

if __name__ == "__main__":
    print("Reading and parsing the obo file.")
    inp_obo_file = "./go.obo"
    gp = go_obo_parser()
    gp.parseOBO(inp_obo_file)
    print("Parsing complete.")

    #Get all anscestors of a GO Term
    parents = gp.getAncestors('GO:2001282')
    print("Parents of GO:2001282")
    for parent in parents:
        print(str(parent))