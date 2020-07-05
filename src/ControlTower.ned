//
// Definition of the ControlTower simple module
//
// Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
//

package aerocomsystem1;


simple ControlTower {
	parameters:
	    int N;		// number of aircrafts
	    int numberOfServers;	// number of servers
	   	@signal[packetReceived](type=long);
	   	@statistic[packetReceived](title="Number of packets received"; record=sum);
	    @display("i=device/receiverdish");
	gates:
	    input in[N*numberOfServers];
}