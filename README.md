# pySimpleEncryption

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
