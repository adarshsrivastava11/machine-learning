import zmq
import ConfigParser


def main():
    config = ConfigParser.RawConfigParser()  
    config.read('config.ini')
    client_port = config.get('devices', 'client')
    geomapper_port = config.get('devices', 'geomapper')
    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:"+client_port)
        
        frontend.setsockopt(zmq.SUBSCRIBE, "")
        
        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:"+geomapper_port)

        zmq.device(zmq.FORWARDER, frontend, backend)
    except Exception, e:
        print e
        print "bringing down zmq device"
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()

if __name__ == "__main__":
    main()