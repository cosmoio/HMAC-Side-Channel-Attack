#!/usr/bin/env python3

from colorama import init, Fore, Style
import os, sys
import datetime

def print_logo(program_name):
    rows, columns = os.popen('stty size', 'r').read().split()
    size = int(columns)-10
    print("\n\n"+Style.BRIGHT+Fore.YELLOW+program_name.center(size,"#")+"\n")
    print(Style.RESET_ALL)
    
def print_message(message, message_type):
    if message_type == "info":
        print(Style.BRIGHT + Fore.BLUE + "[*] " + Style.RESET_ALL + message,end='')
    if message_type == "warning":
        print(Style.BRIGHT + Fore.YELLOW + "[!] " + Style.RESET_ALL + message,end='')
    if message_type == "success":
        print(Style.BRIGHT + Fore.GREEN + "[+] " + Style.RESET_ALL + message,end='')
    if message_type == "error":
        print(Style.BRIGHT + Fore.RED + "[!] " + Style.RESET_ALL + message,end='')
    if message_type == "log":
        print(Style.BRIGHT + Fore.WHITE + "[~] " + Style.RESET_ALL + message,end='')



def lr_justify(left, right, width):
    return '{}{}{}'.format(left, ' '*(width-len(left+right)), right)
