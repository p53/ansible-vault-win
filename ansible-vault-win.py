#!/usr/bin/python

import sys
import os
import io

pathname = os.path.dirname(sys.argv[0])
abs_pathname = os.path.abspath(pathname)
sys.path.append(abs_pathname)

import vaultslib
import argparse

if len(sys.argv) <= 1:
    print "You have to provide arguments!"
    exit(1)

parser = argparse.ArgumentParser(
        description="description: Utility for encrypting/decrypting in ansible vault format"
    )

group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-e", 
    "--encrypt", 
    help="Encrypt specified file",
    action='store_const', 
    dest='action',
    const='encrypt'
)

group.add_argument(
    "-d", 
    "--decrypt", 
    help="Decrypt specified file",
    action='store_const', 
    dest='action',
    const='decrypt'
)

parser.add_argument(
    "-f", 
    "--file", 
    help="Path to file",
    dest='encrypt_file'
)

parser.add_argument(
    "-p", 
    "--password", 
    help="Password for encryption",
    dest='encrypt_pass'
)

results = parser.parse_args()

old_file_content = ''

if os.path.isfile(results.encrypt_file) :
    f = io.open(results.encrypt_file, 'r+',newline='')
    old_file_content = f.read()
    f.seek(0,0)
    
    if results.action == 'encrypt':
        vobj = vaultslib.VaultLib(results.encrypt_pass)
        
        if vobj.is_encrypted(old_file_content):
            print "Your data are already encrypted!"
            exit(2)

        encrypted_data = vobj.encrypt(old_file_content)
        unicode_encr_data = unicode(encrypted_data)

        try:       
            f.truncate()
            f.write(unicode_encr_data)
        finally:
            f.close()
            
    elif results.action == 'decrypt':
        vobj = vaultslib.VaultLib(results.encrypt_pass)

        if not vobj.is_encrypted(old_file_content):
            print "Your data are already decrypted!"
            exit(2)
            
        decrypted_data = vobj.decrypt(old_file_content)
        unicode_decr_data = unicode(decrypted_data)
        
        try:
            f.truncate()
            f.write(unicode_decr_data)
        finally:
            f.close()
            
    f.close()
            
else:
    raise Exception("File doesn't exist")
