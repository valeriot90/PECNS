/*
 * Behavior of the ControlTower simple module
 * Basically this module is a sink that receives packets, delete them and collects statistics
 *
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#include <omnetpp.h>

using namespace omnetpp;


class ControlTower : public cSimpleModule {
  private:
    simsignal_t packetReceivedSignal;

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(ControlTower);


void ControlTower::initialize() {
    packetReceivedSignal = registerSignal("packetReceived");
}

void ControlTower::handleMessage(cMessage *msg) {
    // DEBUG
    EV << "Packet received at time: " << simTime() << endl;

    emit(packetReceivedSignal, 1);

    delete msg;
}
