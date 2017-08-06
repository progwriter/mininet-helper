Mininet helper
--------------

A set of scripts that automate starting simulations using [Mininet][mn]
and injecting traffic.

For details on traffic generation and injection,
see [TMgen] repository and [DITG] injector.

Getting started
---------------

1. Run ``vagrant up`` to start a virtual machine containing Mininet, ONOS controller and the DITG traffic generator
2. ``vagrant ssh`` to connect to the VM.
3. ``cd /mn_helper``
4. ``python run_mininet.py --help``

From here you can run mininet with different GML topologies (just pass ``-t filename.gml`` to the script).
As a special test case, ``-t`` argument recognizes "complete" and "linear" values. This creates a network
of 5 nodes as a complete and path graph, respectively.

By default this will just create the network and drop you into the Mininet CLI.

Customization
-------------
You can implement custom experiments as python functions/modules and dropping them in the *experiments* folder.
If the name of the function is "my_experiment" you can trigger it's execution with the ``-e my`` parameter
to the ``run_mininet.py`` script.

For an example, see *experiments/inject_ditg.py*  
The inject_experiment function will utilize pre-installed [TMgen] and [DITG] to inject
sample data into the simulation. The sample data contains a uniform 5-node traffic matrix.


[mn]: http://www.grid.unina.it/software/ITG/
[TMgen]: https://github.com/progwriter/TMgen
[DITG]: http://www.grid.unina.it/software/ITG/
