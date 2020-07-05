//
// Definition of the Source simple module
//
// Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
//

package aerocomsystem1;


simple Source {
	parameters:
	    volatile double k @unit(s); 	// time between packets generation (in seconds)	
	    int packetSize @unit(bit);	  // size of the packet to send (in bits)
	    int packetPriority;		// priority of the packet (useful only if a Priority Queue is used)
	    @display("i=block/source");
	gates:
	    output out;	
}