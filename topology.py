from mininet.topo import Topo
from networkx import read_gml, complete_graph, path_graph


class GMLTopo(Topo):
    """
    Implements custom topology class that allows loading
    GML files.
    """

    def __init__(self, file_name, num_hosts, **params):
        """
        Create a new topology 
        :param file_name:  the filename (or special name, e.g., linear) of the topology
        :param num_hosts: number of hosts to attach to each switch
        :param params: any keyword arguments accepted by :py:class:mininet.topo.Topo
        """

        Topo.__init__(self, **params)

        g = None
        # Add linear topologies and complete topologies as a special case,
        # helps with quick debugging
        if file_name.lower() == 'linear':
            g = path_graph(5)
        elif file_name.lower() == 'complete':
            g = complete_graph(5)
        else:
            g = read_gml(file_name, label='id')
        offset = 0
        # 0-nodes will mess with MAC addresses, offset to start from 1
        if any(n == 0 for n in g.nodes()):
            offset = 1
        for n in g.nodes():
            self.addSwitch(str(n + offset))
            for hnumber in range(1, num_hosts):
                self.addHost('h{}.{}'.format(n + offset, hnumber))
                self.addLink(str(n + offset), 'h{}.{}'.format(n + offset, hnumber))

            if 'hasMbox' in g.node[n] and bool(g.node[n]['hasMbox']):
                self.addHost('m{}'.format(n + offset))
                self.addLink(str(n + offset), 'm{}'.format(n + offset))

        # add links here:
        for u, v in g.to_undirected().edges():
            self.addLink(str(u + offset), str(v + offset))

    def is_mbox(self, hostname):
        """Check if the node is a middlebox"""
        hostname.startswith('m')

    def mboxes(self):
        """
        Returns a list of all middleboxes
        """
        return [n for n in self.hosts() if self.is_mbox(n)]


# Support for mininet --custom parameter, just in case.
# Although we will likely not use this, due to our custom run_mininet.py script
topos = {'anytopo': (lambda f, n: GMLTopo(f, n))}
