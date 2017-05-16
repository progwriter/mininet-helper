import argparse

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController

from topology import GMLTopo
from experiments import *


def setup(topo_filename, num_hosts, controller_ip):
    topo = GMLTopo(topo_filename, num_hosts)
    setLogLevel('info')
    controller = RemoteController('remote', ip=controller_ip)
    net = Mininet(topo, controller=controller, waitConnected=True)

    # Set the host IPs in a particular way for easier debugging
    for h in topo.hosts():
        # Assume we can split by .
        hnumber = int(h.split('.')[-1])
        if topo.is_mbox(h):
            net.get(h).setIP('10.0.{}.{}'.format(h.lstrip('m'), 128 + hnumber))
        else:
            net.get(h).setIP('10.0.{}.{}'.format(h.lstrip('h'), 1 + hnumber))

    return net


def test_experiment(net):
    """
    Just start the console
    :param net: 
    :return: 
    """
    CLI(net)


# def load_modules():
#     """
#     Based loosely on http://stackoverflow.com/questions/951124/dynamic-loading-of-python-modules
#     """
#     dirname = 'experiments'
#     result = {}
#     lst = os.listdir(dirname)
#     mods = []
#     for f in lst:
#         if os.path.isfile(f) and f.endswith('.py'):
#             mods.append(f)
#     # load the modules
#     for m in mods:
#         modname = m.split('.')[-1]
#         print(modname)
#         result[m] = import_module(modname, package=dirname)
#     return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topo', required=True, help='Name (or filename) of the topology to create in Mininet')
    parser.add_argument('-c', '--controller', default="127.0.0.1",
                        help='IP address of the controller. Default is 127.0.0.1')
    parser.add_argument('-e', '--experiment', default='test',
                        help='Name of the experiment to run. Functions of the form foo_experiment are '
                             'automatically loaded form the files in experiments folder and can be addressed by foo')
    parser.add_argument('--num_hosts', type=int, default=1,
                        help='Number of hosts to attach to each switch')
    options = parser.parse_args()

    # extras = load_modules()
    # print(extras)
    # print(globals())
    exp_name = '{}_experiment'.format(options.experiment)
    exp_func = None
    if exp_name in globals():
        exp_func = globals()[exp_name]
    # elif exp_name in extras:
    #     exp_func = extras[exp_name]
    else:
        raise ValueError('No such experiment found')
    net = setup(options.topo, options.num_hosts, options.controller)
    net.start()
    exp_func(net)
    net.stop()
