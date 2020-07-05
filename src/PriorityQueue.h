/*
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#ifndef PRIORITYQUEUE_H_
#define PRIORITYQUEUE_H_


#include "Queue.h"


class PriorityQueue: public Queue {
  private:
    struct LessThanByPriority {
        bool operator()(const Packet *a, const Packet *b) const {
            return a->getPriority() < b->getPriority();
        }
    };
    std::priority_queue <Packet*, std::vector<Packet*>, LessThanByPriority> priorityQueue;
  public:
    virtual void pop();
    virtual Packet* front();
    virtual void push(Packet* packet);
    virtual int size();
    virtual bool empty();
};


#endif /* PRIORITYQUEUE_H_ */
