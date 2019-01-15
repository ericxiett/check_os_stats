import random
import string
import time

from common.config import CONF
from common.log import LOG
from common.os_clients import get_nova_client


class CheckPet(object):
    '''
    Pet that used for checking vxlan link
    One pet is one vm on each cmp node
    '''
    def __init__(self, cmp, ip=None, uuid=None):
        self.cmp_node = cmp
        self.vm_ip = ip
        self.vm_uuid = uuid

class VxlanLinkCheck(object):

    def __init__(self):
        super(VxlanLinkCheck, self).__init__()
        self.novac = get_nova_client()

    def _set_up(self):
        # TODO: Create test project and test user, now can use fiptest
        # that already be created before

        self.pets = []
        # Get all compute nodes
        compute_services = \
            self.novac.services.list(binary='nova-compute')
        for srv in compute_services:
            LOG.info('compute service: %s', srv.__dict__)
            if srv.status == 'disabled' or \
                    srv.state == 'down':
                LOG.info('host %s not ok for boot vm', srv.host)
                continue
            cmp = srv.host

            vm_name = 'ckpet-' + ''.join(random.sample(
                string.ascii_letters + string.digits, 8
            ))
            flavor = CONF.get('DEFAULT', 'flavor')
            image = CONF.get('DEFAULT', 'image')
            nics = [{'net-id':  CONF.get('DEFAULT', 'network')}]
            availability_zone = ':' + cmp + ':'
            vm = self.novac.servers.create(
                name=vm_name,
                flavor=flavor,
                image=image,
                nics=nics,
                availability_zone=availability_zone
            )

            # Wait for vm OK
            vm_ip = None
            vm_uuid = None
            while True:
                vm_info = self.novac.servers.get(vm.id)
                if vm_info.status != 'ACTIVE' and vm_info.status != 'ERROR':
                    time.sleep(3)
                elif vm_info.status == 'ERROR':
                    LOG.info('vm %s %s on %s is ERROR', vm.id, vm_name, cmp)
                    break
                else:
                    LOG.info('vm %s %s is ACTIVE', vm.id, vm_name)
                    vm_uuid = vm.id
                    for key, value in vm_info.addresses.items():
                        for add_id in iter(value):
                            if add_id.get('OS-EXT-IPS:type') == 'fixed':
                                vm_ip = add_id.get('addr')
                                break
                    self.pets.append(CheckPet(cmp, ip=vm_ip, uuid=vm_uuid))
                    break

        index = 0
        with open('iplist', 'a+') as f:
            for pt in self.pets:
                LOG.info("%s: vm %s %s on %s", index, pt.vm_uuid,
                         pt.vm_ip, pt.cmp_node)
                f.write(pt.vm_ip)
                index += 1

    def _clean_up(self):
        for pt in self.pets:
            LOG.info('Delete %s', pt.vm_uuid)
            self.novac.servers.force_delete(pt.vm_uuid)

    def execute(self):
        self._set_up()
        #self._clean_up()
