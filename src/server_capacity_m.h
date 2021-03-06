//
// Generated file, do not edit! Created by nedtool 5.0 from server_capacity.msg.
//

#ifndef __SERVER_CAPACITY_M_H
#define __SERVER_CAPACITY_M_H

#include <omnetpp.h>

// nedtool version check
#define MSGC_VERSION 0x0500
#if (MSGC_VERSION!=OMNETPP_VERSION)
#    error Version mismatch! Probably this file was generated by an earlier version of nedtool: 'make clean' should help.
#endif



/**
 * Class generated from <tt>server_capacity.msg:1</tt> by nedtool.
 * <pre>
 * message ServerCapacityMsg
 * {
 *     double currentServerCapacity = 0.0;
 * }
 * </pre>
 */
class ServerCapacityMsg : public ::omnetpp::cMessage
{
  protected:
    double currentServerCapacity;

  private:
    void copy(const ServerCapacityMsg& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const ServerCapacityMsg&);

  public:
    ServerCapacityMsg(const char *name=nullptr, int kind=0);
    ServerCapacityMsg(const ServerCapacityMsg& other);
    virtual ~ServerCapacityMsg();
    ServerCapacityMsg& operator=(const ServerCapacityMsg& other);
    virtual ServerCapacityMsg *dup() const {return new ServerCapacityMsg(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b);

    // field getter/setter methods
    virtual double getCurrentServerCapacity() const;
    virtual void setCurrentServerCapacity(double currentServerCapacity);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const ServerCapacityMsg& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, ServerCapacityMsg& obj) {obj.parsimUnpack(b);}


#endif // ifndef __SERVER_CAPACITY_M_H

