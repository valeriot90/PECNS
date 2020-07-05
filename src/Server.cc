/*
 * Behavior of the Server simple module
 * The main task is to process a packet arrived from the router module through an input gate
 * (i.e. simulate the time needed for the transmission of the packet using an Omnet++ self-message)
 * and then send it to the CT module through an output gate.
 * This service time depends on the packet length (fixed to 2048 bits) and on the capacity of
 * the server itself that, as mentioned before, is time-varying and rely on a distribution
 * (characterizing a RV t, time of selection of a new target capacity) and on a set of target
 * capacity specified in the configuration file.
 * Whenever it receives a packet from the router, this module computes the service time and then,
 * when the timer is expired, it sends a notification to the router and the packet to the CT.
 * Furthermore, a second timer is needed: every t seconds the module must update its target capacity,
 * selecting a new value of it from a set of possible value (this set belongs to a uniform
 * distribution).
 * Servers can also communicate each other because they must propagate particular messages coming
 * from the router with the purpose of discovering the server with the current maximum capacity
 * available.
 *
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#include <omnetpp.h>
#include "packet_m.h"
#include "choose_server_m.h"
#include "server_capacity_m.h"
#include "KindMsgDef.h"

using namespace omnetpp;


class Server : public cSimpleModule {
  private:
    double targetCapacity, pastTargetCapacity;
    simtime_t timeTargetCapacity, pastTimeTargetCapacity;
    Packet *packet;     // Packet to send
    cMessage *endTransmissionMsg;
    ServerCapacityMsg *serverCapacityMsg;   // Message used for asking the current capacity of a server
    ChooseServerMsg *chooseServerMsg;   // Message used for the discovery operation of the new server to be used
    cMessage *transmissionTimeTimer;   // Timer: it represents the transmission time (i.e. the service time)
    cMessage *selectionTargetCapacityTimer;    // Timer: every t seconds a new target capacity must be chosen
    simsignal_t responseTimeSignal;

    void handlePacket(cMessage *msg);
    void handleServerCapacityMsg(cMessage *msg);
    void handleChooseServerMsg(cMessage *msg);
    void handleTransmissionTimeTimer(cMessage *msg);
    void handleSelectionTargetCapacityTimer(cMessage *msg);

    double getCurrentServerCapacity();

  public:
    Server();
    virtual ~Server();

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(Server);


Server::Server() {
    packet = nullptr;
    transmissionTimeTimer = nullptr;
    endTransmissionMsg = nullptr;
    serverCapacityMsg = nullptr;
    chooseServerMsg = nullptr;
    selectionTargetCapacityTimer = nullptr;
}

Server::~Server() {
    // TODO
}

void Server::initialize() {
    // We initialize the timers
    transmissionTimeTimer = new cMessage();
    transmissionTimeTimer->setKind(TRANSMISSION_TIME_TIMER);
    selectionTargetCapacityTimer = new cMessage();
    selectionTargetCapacityTimer->setKind(SELECTION_TARGET_CAPACITY_TIMER);

    targetCapacity = par("targetCapacity");
    pastTargetCapacity = par("targetCapacity");
    timeTargetCapacity = par("t").doubleValue();
    pastTimeTargetCapacity = 0;

    responseTimeSignal = getParentModule()->registerSignal("responseTime");

    scheduleAt(timeTargetCapacity, selectionTargetCapacityTimer);

//    // DEBUG
//    EV << "Server initial values: " << "Target Capacity: " << targetCapacity << ", Past Target Capacity: " << pastTargetCapacity << "\n";
}

void Server::handleMessage(cMessage *msg) {
    switch(msg->getKind()) {
        case PACKET :
            // A new packet to be processed from the router is arrived
            handlePacket(msg);
            break;
        case SERVER_CAPACITY_MSG :
            // A message from the router that asks to the server its current capacity is arrived
            handleServerCapacityMsg(msg);
            break;
        case CHOOSE_SERVER_MSG :
            // A message for the discovery server operation is arrived
            handleChooseServerMsg(msg);
            break;
        case TRANSMISSION_TIME_TIMER :
            // Timer expired: service time is over, we can send the packet to the CT
            handleTransmissionTimeTimer(msg);
            break;
        case SELECTION_TARGET_CAPACITY_TIMER :
            // Timer expired: a new target capacity must be chosen
            handleSelectionTargetCapacityTimer(msg);
            break;
    }
}

void Server::handlePacket(cMessage *msg) {
    packet = check_and_cast<Packet *>(msg);
    // We compute the service time and we trigger the timer
    scheduleAt(simTime()+(packet->getPacketSize()/getCurrentServerCapacity()), transmissionTimeTimer);
//    // DEBUG
//    EV << "A new packet Id: " << packet->getId() << " to be processed from the router is arrived.\n";
//    EV << "Service Time is: " << packet->getPacketSize()/getCurrentServerCapacity() << "\n";
}

void Server::handleServerCapacityMsg(cMessage *msg) {
    serverCapacityMsg = check_and_cast<ServerCapacityMsg *>(msg);
    // We get the current capacity of the server, we keep track of this value in the
    // message, and we send it back
    serverCapacityMsg->setCurrentServerCapacity(getCurrentServerCapacity());
    send(serverCapacityMsg, "server_router_channel$o");
//    // DEBUG
//    EV << "Server has computed its current capacity: " << serverCapacityMsg->getCurrentServerCapacity() << "\n";
}

void Server::handleChooseServerMsg(cMessage *msg) {
    chooseServerMsg = check_and_cast<ChooseServerMsg *>(msg);
    // If the server that has received the message has the max current capacity, we store its
    // index and the value of the current capacity in the message
    if (getCurrentServerCapacity() > chooseServerMsg->getCurrentServerCapacity()) {
        chooseServerMsg->setCurrentServerCapacity(getCurrentServerCapacity());
        chooseServerMsg->setServerIndex(chooseServerMsg->getHopCounter());
//        // DEBUG
//        EV << "Updating of the current capacity value of the message. New value: " << chooseServerMsg->getCurrentServerCapacity() << "\n";
    }
    // We increment the hopCounter
    chooseServerMsg->setHopCounter(chooseServerMsg->getHopCounter() + 1);

    // If the message is arrived in the last server we send back the message to the router
    if (chooseServerMsg->getHopCounter() == getParentModule()->par("numberOfServers").longValue()) {
        send(chooseServerMsg, "server_router_channel$o");
//        // DEBUG
//        EV << "We have reached the last server, so we forward the message to the router\n";
    }
    // Otherwise we send the message to the next server
    else {
        send(chooseServerMsg, "to_server");
//        // DEBUG
//        EV << "We forward the message to the next server\n";
    }
}

void Server::handleTransmissionTimeTimer(cMessage *msg) {
    // We send the packet to the CT
    send(packet, "ct_out");
    // We compute the response time and we emit a signal
    getParentModule()-> emit(responseTimeSignal, simTime()-packet->getCreationTime());
    // We send to the router a notification: now servers are available for processing another packet
    endTransmissionMsg = new cMessage("");
    endTransmissionMsg->setKind(END_TRANSMISSION_MSG);
    send(endTransmissionMsg, "server_router_channel$o");
//    // DEBUG
//    EV << "Service time over, sending packet to the CT and notification to the router\n";
}

void Server::handleSelectionTargetCapacityTimer(cMessage *msg) {
    pastTargetCapacity = targetCapacity;
    targetCapacity = par("targetCapacity");
    pastTimeTargetCapacity = timeTargetCapacity;
    timeTargetCapacity = pastTimeTargetCapacity + par("t").doubleValue();
//    // DEBUG
//    EV << "Past Time Target Capacity: " << pastTimeTargetCapacity << " , Time Target Capacity: " << timeTargetCapacity << "\n";

    scheduleAt(timeTargetCapacity, msg);
//    // DEBUG
//    EV << "A new target capacity of: " << targetCapacity << " is chosen at time: " << simTime() << "\n";
}

double Server::getCurrentServerCapacity() {
    // Cx = C0 + ((C1-C0)/(T1-T0))*(Tx-T0))
    double timeInterval;
    double capacityInterval;
    double elapsedTime;

    timeInterval = SIMTIME_DBL(timeTargetCapacity-pastTimeTargetCapacity);
    capacityInterval = targetCapacity-pastTargetCapacity;
    elapsedTime = SIMTIME_DBL(simTime() - pastTimeTargetCapacity);

//    // DEBUG
//    EV << "getCurrentServerCapacity values:\n" << "timeInterval: " << timeInterval << ", capacityInterval: " << capacityInterval
//            << ", elapsedTime: " << elapsedTime << ", currentDifferenceCapacity: " << (capacityInterval/timeInterval)*elapsedTime << "\n";

    return (pastTargetCapacity + ((capacityInterval/timeInterval)*elapsedTime));
}

