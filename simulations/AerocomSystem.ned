//
// Definition of the AerocomSystem network
//
// Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
//

package aerocomsystem1.simulations;

import aerocomsystem1.Source;
import aerocomsystem1.AirCraft;
import aerocomsystem1.ControlTower;


network AerocomSystem {
    parameters:
        int N;		// number of aircrafts
        int numberOfServers;	// number of servers
	submodules:
	    airCraft[N]: AirCraft;
	    controlTower: ControlTower;
	connections:
	    for i=0..N-1, for j=0..numberOfServers-1 { 
	        airCraft[i].out[j] --> controlTower.in[i*numberOfServers+j];
	    }
}

