/*
 * Implementation of the FIFO queue
 *
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#include "FifoQueue.h"
#include "packet_m.h"


void FifoQueue::pop() {
    fifoQueue.pop();
}

Packet* FifoQueue::front() {
    return fifoQueue.front();
}

void FifoQueue::push(Packet* packet) {
    fifoQueue.push(packet);
}

int FifoQueue::size() {
   return fifoQueue.size();
}

bool FifoQueue::empty() {
    return fifoQueue.empty();
}
