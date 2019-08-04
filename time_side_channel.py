#!/usr/bin/env python3
"""
Module latex_parse
"""

__author__ = "cosmoio"
__version__ = "0.1.0"
__license__ = "GPL"


import re,sys
import json
from message import print_logo
from message import print_message
import string
import logging, getopt
import signal
from itertools import product, combinations, permutations

from hashlib import sha256
import timeit
from random import randint
import time

EXIT_ERROR = -1
EXIT_SUCCESS = 1
DEBUG=False
SECRET_KEY = "91bbafc5771ef3a2f10ca302c27123f4"


def print_purpose(PROGRAM_NAME):
    print("The purpose of this program is to showcase a timing side-channel attack of non-constant string comparisons that leaks a cryptographic key.")
    sys.exit(EXIT_SUCCESS)

def print_usage(PROGRAM_NAME):
    print(PROGRAM_NAME+"\n  Usage: Just run it")
    sys.exit(EXIT_ERROR)


def main():
    PROGRAM_NAME = "[ Timing side-channel ]"

    """ Main entry point of the app """
    print_logo(PROGRAM_NAME)

    # we would like to be able to create data that results in an HMAC that is produced by a secret that is unknown to us
    # either we get to the secret key
    # the secret key is used in a string comparison method (one, which allows a timing side channel attack)
    # or we "bruteforce" the correct HMAC by estimating how long the comparison takes of the user supplied and the other hmac takes
    # e.g. USER_SUPPLIED_HMAC == hmac(sha256,message,secret)

    USER_COMMAND = "Transfer 1000 id:01029292030437 id:05929872910221"
    
    # CORRECT HMAC
    HMAC_COMMAND = sign_request(SECRET_KEY,USER_COMMAND)

    print_message("Example: \n","info")
    print_message("Command: {}\n\tKey: {}\n\tHMAC (base64 encoded): {}\n".format(USER_COMMAND, SECRET_KEY, HMAC_COMMAND),"info")

    # An evil command to transfer more cryptos to our account
    EVIL_COMMAND = "Transfer 100000000 id:01029292030437 id:000003133700000"
    # Initial hmac guess (base64)
    provided_hmac = "0000000000000000000000000000"

    timed_attack_create_hmac(provided_hmac, EVIL_COMMAND)


def timed_attack_create_hmac(initial_mac,user_command):
    print_message("Creating hmac for {} without knowledge of secret key.\n".format(user_command),"info")

    hmac_user_command = sign(user_command)

    print_message("HMAC we need to crack: {}\n".format(hmac_user_command),"info")

    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "/" + "="

    print_message("Using charset: {}\n".format(charset),"info")

    print_message("Starting cracking ..\n","success")

    k = 0
    precision = 1
    for index in range(0,28):
        current_char = initial_mac[index]
        
        current_max = 0
        current_time = 0
        for guess_char in product(charset, repeat=1):
            k+=1
            
            initial_mac = initial_mac[:index] + guess_char[0] + initial_mac[index+1:]
            print_message("Testmac: {}\r".format(initial_mac),"info")

            t0 = time.time()
            for i in range(precision): verify(initial_mac,hmac_user_command)
            t1 = time.time()            
            current_time = t1-t0


            #print(" ctm: {}".format(current_time))
            if (current_max < current_time):
                current_max = current_time
                current_char = guess_char[0]

        initial_mac = initial_mac[:index] + current_char + initial_mac[index+1:]


    print_message("Final HMAC: {}, HMAC we need to crack: {}\n".format(initial_mac,hmac_user_command),"info")

    print("\n")


def sign(user_command):
    return sign_request(SECRET_KEY,user_command)


# Insecure HMAC check
def verify(provided_hmac,legitimate_hmac):
    if len(provided_hmac) != len(legitimate_hmac):
        return
    else:
        for i in range(0,len(provided_hmac)):
            if (provided_hmac[i] != legitimate_hmac[i]):
                return
            else:
                #print(provided_hmac[i])
                time.sleep(0.0017)

    print_message("Valid transaction\n","success") 

#    if(HMAC_COMMAND == provided_hmac):


def sign_request(secret_key, message):
    import hashlib
    import hmac
    import base64

    hashed = hmac.new(bytearray(secret_key, "ASCII") , bytearray(message, "ASCII"), hashlib.sha1)

    # The signature
    return base64.b64encode(hashed.digest()).decode("ASCII").replace("\n", "")

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, ORIGINAL_SIGINT)

    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(EXIT_SUCCESS)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(EXIT_SUCCESS)    

if __name__ == "__main__":
    """ This is executed when run from the command line """
    ORIGINAL_SIGINT = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    main()



        
