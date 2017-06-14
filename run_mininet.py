import argparse
import signal

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController

from topology import GMLTopo
from experiments import *


def interrupt_handler(sig, frame):
    global net
    if sig == signal.SIGINT:
        net.stop()

signal.signal(signal.SIGINT, interrupt_handler)


def setup(topo_filename, num_hosts, controller_ip):
    topo = GMLTopo(topo_filename, num_hosts)
    setLogLevel('info')
    controller = RemoteController('remote', ip=controller_ip)
    net = Mininet(topo, controller=controller, waitConnected=True)

    # Set the host IPs in a particular way for easier debugging
    for h in topo.hosts():
        # Assume we can split by .
        snumber, hnumber = map(int, h.lstrip('mh').split('.'))
        if topo.is_mbox(h):
            net.get(h).setIP('10.0.{}.{}'.format(snumber, 128 + hnumber))
        else:
            net.get(h).setIP('10.0.{}.{}'.format(snumber, hnumber))

    return net


def test_experiment(net):
    """
    Just start the console
    :param net: 
    :return: 
    """
    CLI(net)


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

    exp_name = '{}_experiment'.format(options.experiment)
    exp_func = None
    if exp_name in globals():
        exp_func = globals()[exp_name]
    else:
        raise ValueError('No such experiment found')
    # Setup the topology
    net = setup(options.topo, options.num_hosts, options.controller)
    net.start()
    exp_func(net)
    net.stop()
