
import random
import sys
import UrlBloomFilter

class UrlBloomFilterTester:
    Bstart = 98
    Zend = 122
    
    def __init__(self):
        self.goodData = []
        self.goodDataLength = 0
        self.filter = UrlBloomFilter.UrlBloomFilter()
    
    def load(self, filename):
        with open(filename) as fd:
            x = fd.readline()
            line = x.replace("\n", "")
            while line:
                self.goodData.append(line) 
                x = fd.readline()
                line = x.replace("\n", "").replace("\r", "")
                
                
        self.goodDataLength = len(self.goodData)
        
        print("Tester: Read ", len(self.goodData), " good URLs") 
    
    def train(self):
        print("Training filter...")

        for url in self.goodData:
            self.filter.train(url)

    def create(self, j1):
        return "".join(map(lambda i: chr(random.randint(self.Bstart, self.Zend)), range(j1)))
    
    def createURL(self):
        return "".join([self.create(random.randint(8, 14)), "@", self.create(random.randint(9, 17)), ".", self.create(random.randint(3, 5)),  ".", self.create(2)])
    
    def check(self):
        url = ""
        ok = False
        falsePos = 0
        falseNeg = 0
        checkSize = 2 * len(self.goodData)

        print("Checking filter...")
        
        for i in range(1, checkSize):
            if i % 50000 == 0:
                print((i / checkSize * 100), "percent done")
                print("Classifications: ", i)
                print("False negative rate:", falseNeg / i)
                print("False positive rate:", falsePos / i)


            r = random.randint(0, 10)
            if(r == 7):
                idx = random.randint(0, self.goodDataLength - 1)
                url = self.goodData[idx]

                if not self.filter.classify(url):
                    falseNeg += 1
            else:
                url = self.createURL()

                if self.filter.classify(url):
                    falsePos += 1

        print("Total classifications: ", checkSize)
        print("False negative rate:", falseNeg / checkSize)
        print("False positive rate:", falsePos / checkSize)
        
        if falseNeg > 0:
            print("FAIL: some good strings were classified as bad")
        elif (falsePos / checkSize) > 0.05:
            print("FAIL: the rate of false positives is larger than 0.05:", (falsePos / checkSize))
        else:
            print("Correct")
            
tester = UrlBloomFilterTester()
tester.load(sys.argv[1])
tester.train()
tester.check()
