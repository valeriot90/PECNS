//
// Definition of the AirCraft compound module
//
// Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
//

package aerocomsystem1;


module AirCraft {
    parameters:
        int numberOfServers;	// number of servers   
        @signal[numSwitch](type=long);
	    @statistic[numSwitch](title="Number of switch operation"; record=sum);
	    @signal[queueLength](type=long);
	    @statistic[queueLength](title="Statistic about queue's length"; record=max,vector);
	    @signal[responseTime](type=simtime_t);
	    @statistic[responseTime](title="Statistic about response time"; record=mean,vector);    
    gates:
        output out[numberOfServers];
    submodules:
        source: Source;
        router: Router;
        server[numberOfServers]: Server;
    connections:
        source.out --> router.in;
        for i=0..numberOfServers-1 {
            router.router_server_channel[i] <--> server[i].server_router_channel;
        }
        for i=0..numberOfServers-1 {
            server[i].ct_out --> out[i];
        }  
        for i=1..numberOfServers-1 {
            server[i-1].to_server --> server[i].from_server;
        }
        // It is mandatory to use all the gates, so we link the output of the last server
        // with the input of the first server. Note therefore that it is useless for the
        // correct working of the network
        server[numberOfServers-1].to_server --> server[0].from_server;	 
}
