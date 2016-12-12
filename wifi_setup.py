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

import subprocess


__author__ = "Robert Klebes"
__email__ = "rklebes@student.monroecc.edu"
__copyright__ = "Copyright 2016, Robert Klebes"
__license__ = "GPLv3"
__version__ = "0.1"

YES = ['y', 'Y', 'yes', 'Yes', 'YES']
NO = ['n', 'N', 'no', 'No', 'NO']


class Network(object):
    """
    A Network object
    """
    ssid = ''
    id_str = ''
    key_mgmt = 'NONE'
    priority = '0'

    def __init__(self, ssid_Val, id_str_Val=None, key_mgmt_Val=None,
                 passphrase_Val=None, identity_Val=None):
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


def chmod(modeStr, targetFile):
    """
    set modeStr on targetFile

    @type modeStr: string
    @param modeStr: the octal permissions to be set
    @type targetFile: string
    @param targetFile: the relative or absolute path to the target file

    @rtype: number
    @return: 0 if successful
    """
    # TODO implement


def chown(userName, targetFile):
    """
    set userName as owner of targetFile

    @type userName: string
    @param userName: the name of the user to set as owner
    @type targetFile: string
    @param targetFile: the relative or absolute path to the target file

    @rtype: number
    @return: 0 if successful
    """
    # TODO implement


def gen_wpa_supplicant(netList=None, country='US'):
    """
    Generate a wpa_supplicant.conf

    @type netList: string
    @param netList: A list of Network objects
    @type country: string
    @param country: Wifi country code

    @rtype: string
    @return: A wpa_supplicant.conf file in string form
    """
    blockStr = 'country=' + country + '\n'
    blockStr += 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n'
    blockStr += 'update_config=1\n'
    if netList:
        for net in netList:
            blockStr += '\n' + str(net)

    return blockStr


def gen_interfaces(netList=None):
    """
    Generate an interfaces file

    @param netList: A list of Network objects

    @rtype: string
    @return: An interfaces file in string form
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

    return blockStr


def create_Network():
    """
    Create a Network object from user input

    @rtype: Network
    @return: A Network object
    """
    ssid = 'MCC-Guest'
    id_str = 'MCC-Guest'
    key_mgmt = 'NONE'
    identity = None
    passphrase = None
    priority = '0'

    new_ssid = raw_input("Please enter the desired SSID (default is " + ssid +
                         " if blank; spaces not supported)\n> ")
    if new_ssid != '':
        ssid = new_ssid
        id_str = ssid
    print("Network encryption is supported:")
    while True:
        print("1) Non-secure")
        print("2) WPA Personal (such as a home router)")
        print("3) WPA Enterprise (such as university wifi")
        encryption_type = raw_input("What type of encryption will this network"
                                    "use? (Default: Non-secure)\n> ")
        if encryption_type in ['', '1', '2', '3']:
            if encryption_type == '2':
                key_mgmt = 'WPA-PSK'
            elif encryption_type == '3':
                key_mgmt = 'WPA-EAP'
            break
    friendly_name = raw_input("What would you like to name this profile? "
                              "(Default is " + ssid + "; spaces not supported)\n> ")
    if friendly_name != '':
        id_str = friendly_name
    if key_mgmt == 'WPA-EAP':
        identity = raw_input("Please input your username.  This will usually"
                             " be either your account username or the full"
                             " email address associated with your account\n> ")
    if key_mgmt != 'NONE':
        passphrase = raw_input("Please input the passphrase for this network /"
                               " account\n> ")
    newNetwork = Network(ssid, id_str, key_mgmt, passphrase, identity)
    print("A priority can be assigned to this network.  Negative and positive"
          " values are supported.  The device will attempt to connect to the"
          " network with the highest value currently available.")
    priority = raw_input("Please set a priority, or leave blank for neutral"
                         " (0)\n> ")
    if priority != '':
        newNetwork.priority = priority

    return newNetwork


def main():
    """
    @rtype: number
    @return: 0 on successful completion
    """
    # TODO Loop asking to add networks
    first_run = True
    netList = []
    while True:
        if not first_run:
            response = raw_input("Would you like to add another network?"
                                 " (Y/N)\n> ")
            if response in NO:
                break
        elif first_run:
            response = raw_input("Would you like to add a wireless network?"
                                 " (Y/N)\n> ")
            if response in NO:
                print("Bye!")
                exit()
            elif response in YES:
                first_run = False
            else:
                continue
        netList.append(create_Network())
    wpa_supplicant_conf = gen_wpa_supplicant(netList)
    interfaces_conf = gen_interfaces(netList)
    show_new = raw_input("Would you like to see the new configuration files?"
                         " (Y/N)\n> ")
    if show_new in YES:
        print(wpa_supplicant_conf)
    save_new = raw_input("Would you like to save the new configuration files?"
                         " (Y/N)\n> ")
    if save_new in YES:
        wpa_supplicant_file = open('wpa_supplicant.conf', 'w')
        wpa_supplicant_file.write(wpa_supplicant_conf)
        wpa_supplicant_file.close()
        chmod('600', 'wpa_supplicant.conf')
        chown('root:', 'wpa_supplicant.conf')
        interfaces_file = open('interfaces', 'w')
        interfaces_file.write(interfaces_conf)
        interfaces_file.close()
        chmod('644', 'interfaces')
        chown('root:', 'interfaces')

    backup = raw_input("Would you like to backup the original, default"
                       " configuration files? (Y/N)\n> ")
    install = raw_input("Would you like to install the new configuration files?"
                        " (Y/N)\n> ")
    return 0


if __name__ == "__main__":
    main()
