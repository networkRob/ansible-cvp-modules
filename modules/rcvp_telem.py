#!/usr/bin/env python
#
# Copyright (c) 2019, Arista Networks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

ANSIBLE_METADATA = {
    'metadata_version': '1.3',
    'status': ['stable'],
    'supported_by': 'Rob Martin'
}

DOCUMENTATION = '''
---
module: rcvp_telem

short_description: Module to parse Telemetry data from CVP

version_added: "2.7"

description:
    - "This module will parse certain CVP Telemtry data aspects"

options:
    cvp_arg:
        description:
            - This is to specify what function to run
            - Possible completions ['Intfs','Eval']
        required: true
    sw_ports:
        description:
            - List object of all interfaces returned by CVP Telemtry
        required: true

author:
    - Rob Martin (robmartin@arista.com)
'''

from ansible.module_utils.basic import AnsibleModule

def parseSwIntfs(sw_ports):
    all_list = []
    for switch in sw_ports:
        tmp_dict = {}
        tmp_list = []
        for intfs in switch['json']['notifications']:
            keys_intf = intfs['updates'].keys()
            for cur_intf in keys_intf:
                if '/' in cur_intf:
                    tmp_intf = cur_intf[:cur_intf.find('/')]
                else:
                    tmp_intf = cur_intf
                if tmp_intf.find('Ethernet') == 0 and tmp_intf not in tmp_list:
                    tmp_list.append(tmp_intf)
        tmp_dict['ports'] = tmp_list
        tmp_dict['serialNumber'] = switch['item']
        all_list.append(tmp_dict)
    return(all_list)
    
def evalPorts(sw_ports):
    all_list = []
    for s_intf in sw_ports:
        tmp_dict = {}
        if len(s_intf['json']['notifications']) > 0:
            for update in s_intf['json']['notifications']:
                if 'presence' in update['updates'].keys():
                    if update['updates']['presence']['value']['Name'] == 'xcvrPresent':
                        if 'actualIdEepromContents' in update['updates'].keys():
                            tmp_dict = {"serialNumber":s_intf['item'][0]['serialNumber'],"interface":s_intf['item'][1],"xcvr":update['updates']['actualIdEepromContents']['value']['mediaType']}
        if len(tmp_dict.keys()) > 0:
            all_list.append(tmp_dict)
    return(all_list)

def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        cvp_arg=dict(required=True),
        sw_ports=dict(type='list',required=True)
    )
    
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)
    result = dict(changed=False)

    if module.params['cvp_arg'] == 'Intfs':
        result['results'] = parseSwIntfs(module.params['sw_ports'])
        result['status'] = "Success"
    elif module.params['cvp_arg'] == 'Eval':
        result['results'] = evalPorts(module.params['sw_ports'])
        result['status'] = "Success"

    module.exit_json(**result)

if __name__ == "__main__":
    main()