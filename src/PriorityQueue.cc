/*
 * Implementation of the Priority queue
 * Note that this queue is never used in this project, but is ready for further works
 *
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#include "PriorityQueue.h"
#include "packet_m.h"


void PriorityQueue::pop() {
    priorityQueue.pop();
}

Packet* PriorityQueue::front() {
    return priorityQueue.top();
}

void PriorityQueue::push(Packet* packet) {
    priorityQueue.push(packet);
}

int PriorityQueue::size() {
   return priorityQueue.size();
}

bool PriorityQueue::empty() {
    return priorityQueue.empty();
}
