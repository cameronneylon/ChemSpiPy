import urllib
import xml.etree.ElementTree as ET
import unittest


class ChemSpiderId(str):
    """A class for holding ChemSpider IDs and enabling searches based on them.

    """

    def __init__(self,csid):
        """Initialize the ChemSpiderId object with a value.

        """

        self.id = ""

        if type(csid) == str and csid.isdigit() == True:
            self.id = csid
            
        elif type(csid) == int:
            self.id = str(csid)

        else:
            raise TypeError('ChemSpiderId needs to be intialised with an int or a str')

    def __string__(self):
        return self.id

    def imageurl(self):
        """ Return the URL of a png image for a specific Chemspider ID.

        some random text
        """

        assert self != '', 'ChemSpiderId not initialised with value'

        baseurl = 'http://www.chemspider.com/'
        url = baseurl + 'ImagesHandler.ashx?id=%s' % self
        return url


def simplesearch(query):
    """Returns ChemSpiderId string from a simple search for query.

    some random text
    """

    assert type(query) == str, 'query not a string object'

    baseurl = 'http://www.chemspider.com/'
    token  = '3a19d00d-874f-4879-adc0-3013dbecbbc9'

    # Construct a search URL and poll Chemspider for the XML result
    searchurl = baseurl + 'Search.asmx/SimpleSearch?query=' + query + '&token=' + token

    response = urllib.urlopen(searchurl)

    tree = ET.parse(response) #parse the CS XML response
    elem = tree.getroot()
    csid_tags = elem.getiterator('{http://www.chemspider.com/}int')

    csidlist = []
    for tags in csid_tags:
      csidlist.append(tags.text)
    
    returned_id = ChemSpiderId(csidlist[0])

    return returned_id

########################################
#
# Unit tests
#
########################################

class TestChemSpiPy(unittest.TestCase):

    def setUp(self):
        self.testint = 236
        self.teststring = '236'
        self.testquery = 'benzene'
        self.testimageurl = 'http://www.chemspider.com/ImagesHandler.ashx?id=236'

    def testchemspiderid(self):
        self.assertRaises(TypeError, ChemSpiderId, 1.2)
        self.assertEqual(ChemSpiderId(self.teststring), self.teststring)
        self.assertEqual(ChemSpiderId(self.testint), self.teststring)
        self.assertEqual(ChemSpiderId(self.teststring).imageurl(), self.testimageurl)

    def testsimplesearch(self):
        self.assertEqual(simplesearch(self.testquery), self.teststring)


if __name__ == '__main__':
    unittest.main()
