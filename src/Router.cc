/*
 * Behavior of the Router simple module
 * This module receives packets from the source module through an input gate and, if necessary
 * (i.e. if a server is busy), pushes them in the queue.
 * Whenever it receives a notification from a server (i.e. a server has completed its service and
 * now the aircraft can transmit another packet), it pulls a packet from the queue (if available),
 * it chooses a server and it sends the packet to it through an output gate.
 * The selection of the server is done relying on a routing algorithm and using a routing table
 * updated at each packet transmission.
 * The queue is implemented as an abstract class, and the actual class used is chosen relying on
 * a parameter which can be set in the configuration file. This allows the module to work
 * flawlessly with different policies. The policy actually used is the FIFO, but also a priority-based
 * policy is implemented and could be used for performance comparisons in a future work; other policies
 * are still easily implementable without changing this module.
 * Routing algorithms available and used as a meter of comparison are three: the first is the one
 * described above that basically chooses a new server with the maximum capacity only if the last
 * two transmissions are decreased by a certain percentage (set in the configuration file), the
 * second chooses randomly a server at each transmission, while the third uses always the same server.
 * The algorithm actually used can be set in the configuration file without changing this module.
 * The routing table contains the indexes of the servers used in the last transmissions with their
 * current capacities, and is maintained up-to-date asking to the chosen server its current capacity
 * with a particular message.
 * If the router wants to know the server having the maximum capacity, it sends a particular message
 * to the first server: this message is then propagated to the other servers and finally comes back
 * to the router within the requested information.
 * Finally note that if the server-switch operation is needed, the router must wait S seconds before
 * sending the packet (where S is a parameter defined in the configuration file): this waiting time
 * is implemented with an Omnet++ self-message.
 *
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#include <omnetpp.h>
#include <map>
#include "Queue.h"
#include "FifoQueue.h"
#include "PriorityQueue.h"
#include "packet_m.h"
#include "choose_server_m.h"
#include "server_capacity_m.h"
#include <string>
#include "KindMsgDef.h"

using namespace omnetpp;


class Router : public cSimpleModule {
  private:
    struct pastTransmissionData {
        double currentCapacity;
        int serverIndex;
    };
    std::map<int, pastTransmissionData> routerTable;   // This map stores pairs of: server_index | current_capacity
    Queue *queue;
    bool serverAvailable;   // If false, a server (doesn't matter which) is transmitting a packet, and a new
                            // packet arriving from the source must be stored in the queue.
                            // Note that just a server at a time can transmit a packet while other N-1 are free.
    std::string routingAlgorithm;   // Routing algorithm
    std::string queuePolicy;    // Policy of the queue
    Packet *packet;     // Packet to send that is arrived from source
    Packet *packetDelayed;      // Packet in the router that is delayed by a link switch operation
    ChooseServerMsg *chooseServerMsg;   // Message used for the discovery operation of the new server to be used
    ServerCapacityMsg *serverCapacityMsg;   // Message used for asking the current capacity of a server
    cMessage *switchDelayTimer;     // Timer: if an operation of link-switch is needed, we must wait

    simsignal_t queueLengthSignal, numSwitchSignal;

    void handlePacket(cMessage *msg);
    void handleEndTransmissionMsg(cMessage *msg);
    void handleServerCapacityMsg(cMessage *msg);
    void handleChooseServerMsg(cMessage *msg);
    void handleSwitchDelayTimer(cMessage *msg);

    void sendPacketToServer();
    bool checkLinkSwitchOperation();
    void chooseNewServer();
    void askServerCapacity();
    void printTable();      // Debug function

  public:
    Router();
    ~Router();

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(Router);


Router::Router() {
    serverAvailable = true;
    packet = nullptr;
    packetDelayed = nullptr;
    chooseServerMsg = nullptr;
    serverCapacityMsg = nullptr;
    switchDelayTimer = nullptr;
}

Router::~Router() {
    // TODO important: empty the queue
}

void Router::initialize() {
    // We initialize the routing table: we need to store just the data of two transmissions.
    // We initialize the indexes of the two links and their current capacities with random values.
    routerTable[0].currentCapacity = par("targetCapacity").doubleValue();
    routerTable[1].currentCapacity = par("targetCapacity").doubleValue();
    routerTable[0].serverIndex = rand()%(par("numberOfServers").longValue());
    routerTable[1].serverIndex = rand()%(par("numberOfServers").longValue());
//    // DEBUG
//    EV << "Initialization of the router table:\n" ;
//    printTable();

    // We choose the routing algorithm
    routingAlgorithm = par("routingAlgorithm").stringValue();

    // We choose the policy of the queue
    queuePolicy = par("queuePolicy").stringValue();
    if (queuePolicy == "FIFO_POLICY") {
        queue = new FifoQueue();
    }
    // Note that this policy is implemented but it is never used in this project
    if (queuePolicy == "PRIORITY_POLICY") {
        queue = new PriorityQueue();
    }

    // We initialize the timer
    switchDelayTimer = new cMessage();
    switchDelayTimer->setKind(SWITCH_DELAY_TIMER);

    // We register the signals
    queueLengthSignal = getParentModule()->registerSignal("queueLength");
    numSwitchSignal = getParentModule()->registerSignal("numSwitch");
}

void Router::handleMessage(cMessage *msg) {
    switch(msg->getKind()) {
        case PACKET :
//            // DEBUG
//            EV << "A new packet is arrived from the source\n";
            // A new packet to be processed from the source is arrived
            handlePacket(msg);
            break;
        case END_TRANSMISSION_MSG :
//            // DEBUG
//            EV << "A server has transmitted a packet and now all servers are available for processing a new packet\n";
            // A server has completed the transmission of a packet
            handleEndTransmissionMsg(msg);
            break;
        case SERVER_CAPACITY_MSG :
            // A server has answered sending his current capacity available
            handleServerCapacityMsg(msg);
            break;
        case CHOOSE_SERVER_MSG :
            // A message containing the new server chosen for the transmission is arrived
            handleChooseServerMsg(msg);
            break;
        case SWITCH_DELAY_TIMER :
            // Timer expired: the switch link operation is terminated, now we can send the packet to the server
            handleSwitchDelayTimer(msg);
            break;
    }
}

void Router::handlePacket(cMessage *msg) {
    packet = check_and_cast<Packet *>(msg);
    // If no servers are transmitting a packet we choose the right server and we send the packet to it
    if (serverAvailable) {
//        // DEBUG
//        EV << "Servers are free, Packet Id: " << packet->getId() << " will be processed\n";
        // From now until a server has finished the transmission of the packet, we can't process
        // another packet
        serverAvailable = false;
        // We send the packet to a server
        sendPacketToServer();
    }
    // Else if a server is transmitting a packet we just insert the packet in the queue
    else {      // serverAvailable == false
        queue->push(packet);
        getParentModule()->emit(queueLengthSignal, queue->size());
//        // DEBUG
//        EV << "Packet stored in the queue. Queue length: " << queue->size() << "\n";
    }
}

void Router::handleEndTransmissionMsg(cMessage *msg) {
    // We delete the message
    delete(msg);
    // If no packets to be processed are available, we just set the variable
    // serverAvailable to true (all servers are now free and we are waiting for a new packet to be processed)
    if (queue->empty()) {
        serverAvailable = true;
//        // DEBUG
//        EV << "No packets are available in the queue, waiting for packets...\n";
    }
    // Else if there is at least one packet to be processed in the queue, we pop it, we choose the
    // right server and we send the packet to it
    else {
        packet = queue->front();
        queue->pop();
        getParentModule()->emit(queueLengthSignal, queue->size());
//        // DEBUG
//        EV << "Packet id: " << packet->getId() << " is popped from the queue and will be processed\n";
//        EV << "Queue length: " << queue->size() << "\n";
        sendPacketToServer();
    }
}

void Router::handleServerCapacityMsg(cMessage *msg) {
    serverCapacityMsg = check_and_cast<ServerCapacityMsg *>(msg);
    // We send the packet to the server and we update the router table
    send(packet, "router_server_channel$o", routerTable[0].serverIndex);
    routerTable[1].serverIndex = routerTable[0].serverIndex;
    routerTable[1].currentCapacity = routerTable[0].currentCapacity;
    routerTable[0].currentCapacity = serverCapacityMsg->getCurrentServerCapacity();
    // We delete the message
    delete(serverCapacityMsg);
//    // DEBUG
//    EV << "Table updated, sending to server number: " << routerTable[0].serverIndex << "\n";
//    printTable();
}

void Router::handleChooseServerMsg(cMessage *msg) {
    chooseServerMsg = check_and_cast<ChooseServerMsg *>(msg);
    // We update the router table
    routerTable[1].serverIndex = routerTable[0].serverIndex;
    routerTable[1].currentCapacity = routerTable[0].currentCapacity;
    routerTable[0].serverIndex = chooseServerMsg->getServerIndex();
    routerTable[0].currentCapacity = chooseServerMsg->getCurrentServerCapacity();
    // We delete the message
    delete(chooseServerMsg);

//    // DEBUG
//    EV << "A new server was chosen: " << routerTable[0].serverIndex << " with current capacity: " << routerTable[0].currentCapacity << "\n";
//    printTable();

    // We check if the same server is chosen: in this case we don't need the switch operation
    if (routerTable[1].serverIndex == routerTable[0].serverIndex) {
        send(packet, "router_server_channel$o", routerTable[0].serverIndex);
//        // DEBUG
//        EV << "The same server was chosen, the link-switch operation is not needed. Sending packet Id: " << packet->getId() << " to server: " << routerTable[0].serverIndex <<"\n";
    }
    else {
        // The link-switch operation is needed, so we must wait for the conclusion of it
        packetDelayed = packet;
        getParentModule()->emit(numSwitchSignal, 1);
        scheduleAt(simTime()+par("switchTime").doubleValue(), switchDelayTimer);
//        // DEBUG
//        EV << "Link switch operation started at time: " << simTime() << "\n";
    }
}

void Router::handleSwitchDelayTimer(cMessage *msg) {
    send(packetDelayed, "router_server_channel$o", routerTable[0].serverIndex);
//    // DEBUG
//    EV << "Link switch operation ended, sending packet Id: " << packetDelayed->getId() << " to server: " << routerTable[0].serverIndex << "\n";
}

void Router::sendPacketToServer() {
    // We handle the transmission of the packet depending on the routing algorithm chosen
    if (routingAlgorithm == "MAX_CAPACITY") {
        // We check if a link switch operation is needed
        if (checkLinkSwitchOperation()) {     // A link switch operation is needed
//            // DEBUG
//            EV << "Link switch needed, looking for the right server...\n";
            // We choose a new server
            chooseNewServer();
        }
        else {    // No link switch operation needed
//            // DEBUG
//            EV << "No switch needed, asking current capacity to server for update the table\n";
            // Before sending the packet we must compute the current server capacity and update the router table
            askServerCapacity();
        }
    }
    if (routingAlgorithm == "RANDOM") {
        // We choose at random a new server
        int newServerIndex = rand()%(par("numberOfServers").longValue());
        // We check if a link switch operation is needed
        if (routerTable[0].serverIndex == newServerIndex) {    // No link switch operation needed
            send(packet, "router_server_channel$o", routerTable[0].serverIndex);
        }
        else {      // A link switch operation is needed
            routerTable[0].serverIndex = newServerIndex;
            // The link-switch operation is needed, so we must wait for the conclusion of it
            packetDelayed = packet;
            getParentModule()->emit(numSwitchSignal, 1);
            scheduleAt(simTime()+par("switchTime").doubleValue(), switchDelayTimer);
//            // DEBUG
//            EV << "Link switch operation started at time: " << simTime() << "\n";
        }
    }
    if (routingAlgorithm == "SINGLE_CHANNEL") {
        // We use the same server for each transmission.
        send(packet, "router_server_channel$o", routerTable[0].serverIndex);
//        // DEBUG
//        EV << "Sending packet Id: " << packet->getId() << " to server: " << routerTable[0].serverIndex <<"\n";
    }
}

bool Router::checkLinkSwitchOperation() {
    if ((((routerTable[1].currentCapacity-routerTable[0].currentCapacity)/routerTable[1].currentCapacity)*100) > par("X").doubleValue())
        return true;
    else
        return false;
}

void Router::chooseNewServer() {
    // A new server must be chosen for the transmission of the packet, in particular the server with
    // the maximum current capacity available must be chosen.
    // We find this server using a distributed approach: we send a particular message (that keeps
    // track of the index of the server with the max capacity) to the first server,
    // then each server forwards this message to its neighbor server and finally the last server
    // sends back the message to the router
    chooseServerMsg = new ChooseServerMsg();
    chooseServerMsg->setKind(CHOOSE_SERVER_MSG);
    send(chooseServerMsg, "router_server_channel$o", 0);
}

void Router::askServerCapacity() {
    serverCapacityMsg = new ServerCapacityMsg();
    serverCapacityMsg->setKind(SERVER_CAPACITY_MSG);
    send(serverCapacityMsg, "router_server_channel$o", routerTable[0].serverIndex);
}

void Router::printTable() {
    EV << "Printing router table:\n " << routerTable[0].serverIndex << " | " << routerTable[0].currentCapacity << "\n"
            << routerTable[1].serverIndex << " | " << routerTable[1].currentCapacity << "\n";
}
