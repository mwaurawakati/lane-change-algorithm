class Lane:
    """
    This is the class that keeps the details of a lane
    The details of a lane include: latitude,longitude(start and end) and id

    """
    def __init__(self,lanelatstart, lanelongstart, lanelatend, lanelongend, laneid):
        """
        :param lanelongstart: This is the longitude where the lane starts
        :param lanelatstart: This is the latitude where the lane starts
        :param lanelongend: This is the logitude where the lane ends
        :param lanelatend: This is the latitude that the lane ends
        :param laneid: This is the id of the lane. If a route has five lanes, then the first lane shall have
        id=1 and the last lane shall have id=5
        """
        self.lane_starting_latitude=lanelatstart
        self.lane_starting_longitude=lanelongstart
        self.lane_ending_latitude=lanelatend
        self.lane_ending_longitude=lanelongend
        self.id=laneid
class route(Lane):
    """
    This is the class that carries the details of the
    """
    def __init__(self,routelatstart, routelongstart, routelatend, routelongend,routename, NOL=None):
        """
        :param routelongstart: This is the longitude where the route starts
        :param routelatstart: This is the latitude where the route starts
        :param routelongend: This is the logitude where the route ends
        :param routelatend: This is the latitude that the route ends
        :param routename: This is route name
        :param NOL:This is the number of lanes in the route. If not specified, it is
        assumed that the route has one lane
        """
        self.route_starting_latitude=routelatstart
        self.route_starting_longitude=routelongstart
        self.route_ending_latitude=routelatend
        self.route_ending_longitude=routelongend
        self.name=routename
        if NOL is None:
            self.NOL=1
        else:
            self.NOl=NOL
        self.lanes={}

    def add_lane(self, lanelatstart, lanelongstart, lanelatend, lanelongend):
        id=len((self.lanes).keys)
        if id<self.NOL:
            lane=Lane(lanelatstart, lanelongstart, lanelatend, lanelongend, id+1)
            lanes={id+1: lane}
            self.lanes.update(lanes)
        else:
            exit()
            print("The route has list of lanes fully registered")
def goto(linenum):
    """
    This is the code that implements the goto functionality incase a block of code needs to be implemented
    over again
    :param linenum:
    :return:
    """
    global line
    line = linenum


class Vehicle:
    """
    This is the class that keeps the details of a vehicle/truck. Each truck vehicle has a class like this

    :param lane:This is the lane that the vehicle is in
    :param speed:This is the speed of the vehicle
    :param role:This is the role of the vehicle. The roles are leader, which is
        the vehicle that processes the request,preceder , which is the vehicle that
        precedes the vehicle asking to change lane, follower, which is the vehicle
    :param vehicleid: This is a unique id representing a vehicle
    """
    def __init__(self, name, port, laneid, speed, long, lat,  routename, vehicleid=None):
        self.name=name
        self.port=port
        self.laneid=laneid
        self.speed=speed
        self.vehicleid=vehicleid
        self.long=long
        self.lat=lat
        self.route=routename
        self.lanechangestatus="no change"