/*
 * Abstract class for the implementation of a general queue
 *
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#ifndef QUEUE_H_
#define QUEUE_H_


#include <queue>
#include "packet_m.h"


class Queue {
  public:
    virtual void pop() = 0;
    virtual Packet* front()=0;
    virtual void push(Packet* packet) = 0;
    virtual int size() = 0;
    virtual bool empty() = 0;
};


#endif /* QUEUE_H_ */
