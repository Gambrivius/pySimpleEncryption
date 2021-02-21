'''
Author: Christopher Laponsie
Python Version: 3.7.5
Description:
    This program defines a base class PRNG (Psuedo Random Number Generator) and derives two classes from it:
        MiddleSquarePRNG: An implementation of the middle square algorithm invented by John von Neumann
        lcgPRNG: An implementation of the linear congruental generator with same parameters as ANSI C.

    The two functions provided take either PRNG class as a parameter and output some test information:
        cypherTest(prng, key)
            Parameters:
                prng is an instace of either PRNG class
                key is the value to set the PRNG seed to initially
            Results:
                Performs bitwise XOR on a predefined string with a stream of random values from the PRNG
                Prints the encrypted text
                Resets the seet
                Reperforms the bitwise XOR operation on the cipher text
                Prints the decrypted string.
                Intentionally decrypts the cipher text with the wrong key (key+1)
                Prints the incorrectly decrypted string.
        diceTest(prng)
            Parameters:
                prng is an instace of either PRNG class
            Results:
                Generates 100 random dice rolls by taking normalized output of PRNG function as n:
                    n * 5 + 1 (generates a number between 1 and 6)
                Outputs mean and stdev of sample size.

                For truly random results, the average should be 6/2+0.5 (min roll is 1, max roll is 6, so middle is 6/2 + 1/2)
                Both functions return pretty random results.
                (1 + 2 + 3 + 4 +5 + 6)/6 = 21/6 = 3.5
                

                Further research could include looking at the period of each function.     
'''

class PRNG:
    def __init__ (self):
        self.seed = 0
    def setSeed(self, s):
        self.seed = s
    def getSeed (self):
        return self.seed
    def getRawPRNG(self):
        # to be defined by derived class
        pass
    
    def getNormalizedPRNG(self):
        # normalizes the output to a value between 0 and 1
        # this way it can be scaled to any value
        pass
    def toNormalizedByte(self):
        # takes the normalized ooutput and scales it to a byte

        # to be defined by derived class
        return int(self.getNormalizedPRNG() * 255)

class MiddleSquarePRNG (PRNG):
    '''
    Simple implementation of Middle Square PRNG algorithm

    Resource: https://search-proquest-com.proxy.davenport.edu/docview/2391258883?accountid=40195&pq-origsite=summon    
        Ali-Pacha, H., Hadj-Said, N., Ali-Pacha, A., Mohamad, A. M., & Mamat, M. (2019). Cryptographic adaptation of the middle square generator.
                International Journal of Electrical and Computer Engineering, 9(6), 5615-5627. doi:http://dx.doi.org.proxy.davenport.edu/10.11591/ijece.v9i6.pp5615-5627
    '''
    def __init__ (self):
        self.seed = 0
        self.setDigits(5)
        
    def setSeed(self, s):
        self.seed = s
    def setDigits(self, d):
        self.digits = d
        self.maxValue = int('9' * d)
    def getRawPRNG(self):
        # outputs a pseudo random number using the mdidle square method
        
        # create a string from the square the current seed
        strSquare = str(self.seed ** 2)
        # the string must be atleast self.digits long
        # fill with 0s if necessary
        strSquare = strSquare.zfill(self.digits)
        # get the length of the string
        # necessary to extract the middle
        width = len(strSquare)
        #print (width)
        leftPos = int((width-self.digits)/2)
        #print (leftPos)
        middleSquare = int(strSquare[leftPos:leftPos+self.digits])
        #print(strSquare)
        #print(middleSquare)
        self.setSeed (middleSquare)
        return (middleSquare)
    def getNormalizedPRNG(self):
        # normalizes the output to a value between 0 and 1
        # this way it can be scaled to any value later
        # ie: if you wanted to simulate the roll of the a 6 sided dice
        #       you could take this value, multiply it by 5 and add one
        return (self.getRawPRNG() / self.maxValue)

class lcgPRNG (PRNG):
    '''
    Resource: https://aaronschlegel.me/linear-congruential-generator-r.html
        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.). Aberdeen, MD. Army Research Lab.
    '''
    def __init__ (self):
        self.seed = 123456
        '''
        Selecting paramaters for the LCG can be tricky and involve a bit of math.
        We are using the same as the ANSI C implementation. (Saucier, 2000)
        '''
        self.a = 1103515245
        self.m = 2**32
        self.c = 12345
    def getRawPRNG(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed
    def getNormalizedPRNG(self):
        return (self.getRawPRNG() / self.m)

def cypherTest(prng, key):
    # a simple stream cypher using XOR and a pseudo random number generator

    prng.setSeed ( key )
    print ("Key: %s" % key)
    message = "Hello world!  Cyphering is fun."
    def xorString(msg):
        resultantString = ""
        for pos in range(len(msg)):
            char = msg[pos:pos+1]
            a =  ord(char) # convert the character into ascii value
            encrypted_char = a ^ prng.toNormalizedByte() #bitwise XOR the two ints
            resultantString += chr(encrypted_char)
        return resultantString
    cipherText = xorString(message)
    print ("Plaintext  : '%s'" % message)
    print ("Cipher text: '%s'" % cipherText)

    #  decypher the text
    #  since this a a symmetric-key cipher algorithm, we just reset the key and repeat
    prng.setSeed ( key ) # reset the seed
    decypheredText = xorString(cipherText)
    print ("Decyphered text: '%s'" % decypheredText)

    prng.setSeed ( key+1 ) # reset the seed
    decypheredText = xorString(cipherText)
    print ("Incorrectly Decypthered text: '%s'" % decypheredText)
    
def diceTest(prng):
    samples = 100
    samplesList = []
    print ('Rolling the dice %s times' % samples)
           
    for n in range(samples):
        roll = int(prng.getNormalizedPRNG()*6)+1
        samplesList.append(roll)

    print (samplesList)
    mean = sum(samplesList) / len(samplesList)
    import statistics
    res = statistics.pstdev(samplesList) 
    print ("Mean: %s" % mean)
    print ("Stdev: %s" % res)

if __name__ == '__main__':
    print ('Python Implementation of a Stream Encryption Algorithm')
    print ('Christopher M. LaPonsie')
    print ('IAAS221 Security Foundations')
    print ('------------------------------')
    print ('Instantiating linear congruential generator')
    prngLCG = lcgPRNG()
    if (prngLCG):
        print ('...OK')
    print ('Instantiating middle square generator')
    prngMS = MiddleSquarePRNG()
    prngMS.setDigits ( 10 )
    prngMS.setSeed ( 1234567890 )
    if (prngMS):
        print ('...OK')
    print ('------------------------------')
    print ('Dice test using LCG')
    diceTest(prngLCG)
    print ('------------------------------')
    print ('Dice test using middle square')
    diceTest(prngMS)
    print ('------------------------------')
    print ('Cypher test using LCG')
    cypherTest(prngLCG, 123456)
    print ('------------------------------')
    print ('Cypher test using middle square')
    cypherTest(prngMS, 1234567890)
    print ('------------------------------')
