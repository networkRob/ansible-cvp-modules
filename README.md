## Ansible and Cloud Vision Portal
This repo contains custom Ansible modules and playbooks for parsing/evaluating data returned from CVP.

### Ansible-Playbooks
`get-cvp-eos-xcvrs.yaml` - Ansible-Playbook that will query CVP to get all transceiver types installed on all assocaited switches.
#### Requirements
- `rcvp_telem.py` - Module installed on the Ansible host machine
#### Tested Versions
- Ansible: 2.7.x
- CloudVision Portal: 2018.1.4


### Ansible Modules
`modules/rcvp_telem.py` - Module used to parse interface data returned from CVP.