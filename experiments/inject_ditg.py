import json
from collections import defaultdict
from functools import partial

import sys


def inject_experiment_params(net, tm_fname, num_hosts=1):
    mapping = defaultdict(lambda: [])
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
            host_procs[host] = host.popen(['tmditg', '--tm', tm_fname,
                                           '-l', '60', '-i', str(tm_id), '-s', str(1.0 / num_hosts),
                                           '-d', json.dumps(mapping)], stdout=sys.stdout, stderr=sys.stderr)
    for p in host_procs.values():
        p.wait()


inject_experiment = partial(inject_experiment_params, tm_fname='sample_data/test_tm_5', num_hosts=1)
