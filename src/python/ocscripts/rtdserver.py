import sys,os
import logging
import time
import zmq

STATE_PRIMARY = 1
STATE_BACKUP = 2
STATE_ACTIVE = 3
STATE_PASSIVE = 4

PEER_PRIMARY = 1
PEER_BACKUP = 2
PEER_ACTIVE = 3
PEER_PASSIVE = 4
CLIENT_REQUEST = 5
HEARTBEAT = 400


sys.path.extend([os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')])

from opencluster.configuration import setLogger
setLogger("rtdserver","1")
logger = logging.getLogger(__name__)

class BStarState(object):
    def __init__(self, state, event, peer_expiry):
        self.state = state
        self.event = event
        self.peer_expiry = peer_expiry

class BStarException(Exception):
    pass

fsm_states = {
    STATE_PRIMARY: {
        PEER_BACKUP: ("I: connected to backup (slave), ready as master",
                      STATE_ACTIVE),
        PEER_ACTIVE: ("I: connected to backup (master), ready as slave",
                      STATE_PASSIVE)
        },
    STATE_BACKUP: {
        PEER_ACTIVE: ("I: connected to primary (master), ready as slave",
                      STATE_PASSIVE),
        CLIENT_REQUEST: ("", False)
        },
    STATE_ACTIVE: {
        PEER_ACTIVE: ("E: fatal error - dual masters, aborting", False)
        },
    STATE_PASSIVE: {
        PEER_PRIMARY: ("I: primary (slave) is restarting, ready as master",
                       STATE_ACTIVE),
        PEER_BACKUP: ("I: backup (slave) is restarting, ready as master",
                      STATE_ACTIVE),
        PEER_PASSIVE: ("E: fatal error - dual slaves, aborting", False),
        CLIENT_REQUEST: (CLIENT_REQUEST, True)  # Say true, check peer later
        }
    }

def run_fsm(fsm):
    # There are some transitional states we do not want to handle
    state_dict = fsm_states.get(fsm.state, {})
    res = state_dict.get(fsm.event)
    if res:
        msg, state = res
    else:
        return
    if state == False:
        raise BStarException(msg)
    elif msg == CLIENT_REQUEST:
        assert fsm.peer_expiry > 0
        if int(time.time() * 1000) > fsm.peer_expiry:
            fsm.state = STATE_ACTIVE
        else:
            raise BStarException()
    else:
        logger.info(msg)
        fsm.state = state

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3 :
        print "Usage: python " + sys.argv[0] + " p(or b) [ip of slave or master]"
        sys.exit(0)
    ctx = zmq.Context()
    statepub = ctx.socket(zmq.PUB)
    statesub = ctx.socket(zmq.SUB)

    datapub = ctx.socket(zmq.PUB)
    frontend = ctx.socket(zmq.REP)

    fsm = BStarState(0, 0, 0)

    ip = "localhost"
    if len(sys.argv) >= 3:
        ip = sys.argv[2]


    if sys.argv[1]=="p":
        print "I: Primary master, waiting for backup (slave)"
        frontend.bind("tcp://*:5001")
        statepub.bind("tcp://*:5003")
        statesub.connect("tcp://%s:5004"%ip)
        statesub.setsockopt(zmq.SUBSCRIBE, "")

        fsm.state = STATE_PRIMARY
        datapub.bind("tcp://*:5005")

    elif sys.argv[1]=="b":
        print "I: Backup slave, waiting for primary (master)"
        frontend.bind("tcp://*:5002")
        statepub.bind("tcp://*:5004")
        statesub.connect("tcp://%s:5003"%ip)
        statesub.setsockopt(zmq.SUBSCRIBE, "")

        fsm.state = STATE_BACKUP
        datapub.bind("tcp://*:5006")
    else:
        print "Usage: python " + sys.argv[0] + " p(or b) [ip of slave or master]"
        sys.exit(1)


    send_state_at = int(time.time() + HEARTBEAT)
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(statesub, zmq.POLLIN)

    while True:
        time_left = send_state_at - int(time.time() * 1000)
        if time_left < 0:
            time_left = 0
        socks = dict(poller.poll(time_left))
        if socks.get(frontend) == zmq.POLLIN:
            hd = frontend.recv_string()
            if hd and hd.find("str_") > -1 :
                data = frontend.recv_string()
            else :
                data = frontend.recv_pyobj()

            logger.info("received " + hd)
            fsm.event = CLIENT_REQUEST
            try:
                run_fsm(fsm)
                #send data to datapub
                datapub.send_string(hd,zmq.SNDMORE)
                if hd and hd.find("str_") > -1 :
                    logger.info("received data : " + data)
                    datapub.send_string(data)
                else:
                    datapub.send_pyobj(data)
                frontend.send_string("ok")
            except BStarException:
                del hd
                del data

        if socks.get(statesub) == zmq.POLLIN:
            msg = statesub.recv()
            fsm.event = int(msg)
            del msg
            try:
                run_fsm(fsm)
                fsm.peer_expiry = int(time.time()) + (2 * HEARTBEAT)
            except BStarException:
                break
        if int(time.time() * 1000) >= send_state_at:
            statepub.send("%d" % fsm.state)
            send_state_at = int(time.time()) + HEARTBEAT

if __name__ == '__main__':
    main()