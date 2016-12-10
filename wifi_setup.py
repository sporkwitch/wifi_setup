#!/usr/bin/env python

# Copyright (C) 2016 Robert Klebes
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You can obtain a copy of the GNU General Public License at
# U{https://www.gnu.org/licenses/}.

'''
Simple script to automate wireless configuration for a RaspberryPi running
Raspbian.

@author:        Robert Klebes <rklebes@student.monroecc.edu>
@copyright:     2016, Robert Klebes
@license:       GPLv3
Date created:   20161210
Last modified:  20161210
Python Version: 2.7
'''
__author__      = "Robert Klebes"
__email__       = "rklebes@student.monroecc.edu"
__copyright__   = "Copyright 2016, Robert Klebes"
__license__     = "GPLv3"
__version__     = "0.1"

import subprocess

class Network(object):
    """
    A Network object
    """
    ssid        =   ''
    id_str      =   ''
    key_mgmt    =   'NONE'
    priority    =   '0'

    def __init__(self, ssid_Val, id_str_Val = None, key_mgmt_Val = None,
                 passphrase_Val = None, identity_Val = None):
        """
        Initialize a Network object

        @type ssid_Val: string
        @param ssid_Val: SSID of the Network
        @type id_str_Val: string
        @param id_str_Val: Name for Network profile (no whitespace)
        @type key_mgmt_Val: string
        @param key_mgmt_Val: The type of network authentication
        @type passphrase_Val: string
        @param passphrase_Val: The PSK or user passphrase for the network
        @type identity_Val: string
        @param identity_Val: The username used to authenticate on the network
        """
        self.ssid = ssid_Val
        if id_str_Val:
            self.id_str = id_str_Val
        else:
            self.id_str = self.ssid
        if key_mgmt_Val:
            self.key_mgmt = key_mgmt_Val
        if passphrase_Val:
            self.passphrase = passphrase_Val
        if identity_Val:
            self.identity = identity_Val

    def __str__(self):
        """
        @rtype: string
        @return: A string representation of a Network object in the format
        expected by wpa_supplicant.conf
        """

        blockStr = 'network={\n'
        blockStr += '    ssid="' + self.ssid + '"\n'
        blockStr += '    scan_ssid=1\n'
        blockStr += '    key_mgmt=' + self.key_mgmt + '\n'
        if self.key_mgmt == 'WPA-EAP':
            blockStr += '    eap=PEAP\n'
            blockStr += '    identity="' + self.identity + '"\n'
            blockStr += '    password="' + self.passphrase + '"\n'
            blockStr += '    phase1="peaplabel=auto peapver=0"\n'
            blockStr += '    phase2="MSCHAPV2"\n'
        elif self.key_mgmt == 'WPA-PSK':
            blockStr += '    psk="' + self.passphrase + '"\n'
        blockStr += '    id_str="' + self.id_str + '"\n'
        blockStr += '    priority=' + self.priority + '\n'
        blockStr += '}\n'
        
        return blockStr

def write_wpa_supplicant(netList = None, country = 'US'):
    """
    Write out a wpa_supplicant.conf

    @param netList: A list of Network objects

    @rtype: bool
    @return: True on successful write, else False
    """
    blockStr = 'country=' + country + '\n'
    blockStr += 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n'
    blockStr += 'update_config=1\n\n'
    #TODO Loop to concatenate objects from list
    #TODO write to file
    #TODO chmod 600 file
    #TODO chown root: file
    return False

def write_interfaces(netList = None):
    """
    Take user input and write out an interfaces file

    @param netList: A list of Network objects

    @rtype: bool
    @return: True on successful write, else False
    """
    blockStr = '# interfaces(5) file used by ifup(8) and ifdown(8)\n\n'
    blockStr += '# Please note that this file is written to be used with dhcpcd\n'
    blockStr += '# For static IP, consult /etc/dhcpcd.conf and \'man dhcpcd.conf\'\n\n'
    blockStr += '# Include files from /etc/network/interfaces.d:'
    blockStr += 'source-directory /etc/network/interfaces.d\n\n'
    blockStr += 'auto lo\n'
    blockStr += 'iface lo inet loopback\n\n'
    blockStr += 'auto eth0\n'
    blockStr += 'allow-hotplug eth0\n'
    blockStr += 'iface eth0 inet dhcp\n\n'
    blockStr += 'auto wlan0\n'
    blockStr += 'allow-hotplug wlan0\n'
    blockStr += 'iface wlan0 inet manual\n'
    if netList:
        blockStr += 'wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf\n'
        for net in netList:
            blockStr += 'iface ' + net.id_str + ' inet dhcp\n'
    else:
        blockStr += 'wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n'
    #TODO Write to file
    #TODO change perms on file
    return False

def create_Network():
    """
    Create a Network object from user input

    @rtype: Network
    @return: A Network object
    """
    ssid, id_str = 'MCC-Crypto'
    key_mgmt = 'WPA-EAP'
    identity, passphrase = None
    priority = '0'

    #TODO Get SSID
    #TODO Get friendly name
    #TODO Get encryption type
    #TODO If enterprise, get identity
    #TODO If enterprise or psk, get passphrase
    newNetwork = Network(ssid,id_str,key_mgmt,passphrase,identity)
    #TODO Get and set priority
    newNetwork.priority = priority

    return newNetwork

def main():
    """
    @rtype: number
    @return: 0 on successful completion
    """
    #TODO Loop asking to add networks
    #   TODO list.add(create_Network())
    #TODO Ask to backup original files
    #TODO Ask to copy new files
    if False:
        return 0
    else:
        return 1

if __name__ == "__main__":
    main()
