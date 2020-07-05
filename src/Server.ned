//
// Definition of the Server simple module
//
// Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
//

package aerocomsystem1;


simple Server {
	parameters:
	    volatile double t @unit(s);		// time between selection of a new target capacity (in seconds)
	    volatile double targetCapacity @unit(bps);		// target capacity of each data-link (in bit/sec)
	    @display("i=device/server2");
	gates:
	    inout server_router_channel;
	    output ct_out;
	    input from_server;
	    output to_server;
}
