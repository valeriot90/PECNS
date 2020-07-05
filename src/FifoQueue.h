/*
 * Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferna
 */

#ifndef FIFOQUEUE_H_
#define FIFOQUEUE_H_


#include "Queue.h"


class FifoQueue: public Queue {
  private:
    std::queue <Packet*> fifoQueue;
  public:
    virtual void pop();
    virtual Packet* front();
    virtual void push(Packet* packet);
    virtual int size();
    virtual bool empty();
};


#endif /* FIFOQUEUE_H_ */
