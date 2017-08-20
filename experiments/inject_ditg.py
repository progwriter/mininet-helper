import json
from collections import defaultdict
from functools import partial

import sys

from .base import ExpBase


class InjectFuture(ExpBase):
    def __init__(self, processes):
        # Save all process objects. Make a list so we can iterate multiple times
        # over it if necessary
        self.procs = list(processes)

    def wait(self):
        # Just wait for all processes
        for p in self.procs:
            p.wait()

    def stop(self):
        # Kill everything
        for p in self.procs:
            p.terminate()


def inject_experiment_params(net, tm_fname, num_hosts=1):
    mapping = defaultdict(lambda: [])
    base_port = 8999
    for host in net.hosts:
        # print(host.IP())
        if host.name.startswith('h'):
            tm_id = int(host.name.lstrip('h').split('.')[0])-1
            mapping[tm_id].append(host.IP())
    # print(mapping)
    host_procs = {}
    for host in net.hosts:
        if host.name.startswith('h'):
            tm_id = int(host.name.lstrip('h').split('.')[0])-1
            port = base_port + tm_id
            host_procs[host] = host.popen(['tmditg', '--tm', tm_fname,
                                           '-l', '10', '-i', str(tm_id), '-s', str(1.0 / num_hosts),
                                           '-d', json.dumps(mapping),
                                           '-p', str(port)], stdout=sys.stdout, stderr=sys.stderr)
    return InjectFuture(host_procs.values())


inject_experiment = partial(inject_experiment_params, tm_fname='sample_data/test_tm_5', num_hosts=1)
