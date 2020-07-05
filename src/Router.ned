//
// Definition of the Router simple module
//
// Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
//

package aerocomsystem1;


simple Router {
    parameters:
		int numberOfServers;	  // number of inout gates between the Router simple module and 
								  // the Server simple module (it is the same as number of available links)
		volatile double targetCapacity @unit(bps);		// target capacity of each server (in bit/sec)
		double switchTime @unit(s);		// time needed for the link-switch operation  (in seconds)
		double X;	  // minimun capacity variation beetween two transmissions needed for the activation
					  // of the link-switch operation (in percentage)
		string queuePolicy;		// policy of the queue
		string routingAlgorithm;	// routing algorithm
		@display("i=block/fork");
	gates:
	    input in ;
	    inout router_server_channel[numberOfServers];
}