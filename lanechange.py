"""
This is the implementation of truck platooning algorithm
several algorithm are implemented here
1. Lane changing algorithm
2. Gap creation algorithm
"""

from math import sin, cos, sqrt, atan2, radians
import numpy as np
import time
def goto(linenum):
    """
    This is the code that implements the goto functionality incase a block of code needs to be implemented
    over again
    :param linenum:
    :return:
    """
    global line
    line = linenum
class Lane_Change:

    def __init__(self, platoon):
        platoonsize = len(platoon.port)
        self.platoonsize = platoonsize

    def change_lane(self, Vehicle1, Vehicle2, Vehicle3, Vehicle4, Vehicle5, route):
        """
        This is the function that implements lane change algorithm
        :param Vehicle1: This is the preceding Vehicle in the platoon
        :param Vehicle2: This is the tailing Vehicle in the platoon
        :param Vehicle3: This is the preceding Vehicle in the target lane
        :param Vehicle4: This is the tailing Vehicle in the target lane
        :param Vehicle5: This is the Vehicle requesting to change lane
        :return:
        """
        a = abs(self.calculate_distance(Vehicle5.lat, Vehicle5.long, Vehicle3.lat, Vehicle3.long))
        b = abs(self.calculate_distance(Vehicle5.lat, Vehicle5.long, Vehicle4.lat, Vehicle4.long))
        state1 = self.check_space(a, b)

        # The algorithm starts by checking desirability for lane lane change
        mandatory_change, desire, desirevalue_target_lane = self.lane_change_desire_necessity(Vehicle5, route, Vehicle3.laneid)
        if mandatory_change == 'True':
            print('Mandatory change.Checking space...')
            goto(2)

            if line == 2:
                state1 = self.check_space(a, b)
                if state1 == True:
                    print('space for lane change available...')
                    Vehicle5.lanechangestatus = 'in progress'
                else:
                    while state1 == False:
                        state1 = self.check_space(a, b)
                        goto(2)
            self.gap_creation(Vehicle5, Vehicle1, Vehicle3)
        else:
            if desirevalue_target_lane > 0.5:
                goto(2)
                self.gap_creation(Vehicle5, Vehicle1, Vehicle3)
            else:
                print('Lane changing is not necessary')

        if state1 == True:
            print("Passed State-1 test:There is ample space for lane changing")
            state2 = self.check_speed(Vehicle5.speed, Vehicle4.speed)
            if state2 == True:
                print("Passed State-2 test: The ")
                state3 = 3
            else:

                print('Failed State-2 test:')


        else:

            print('Failed State-1:There is no ample space for lane changing. Try again after sometime')

    def check_space(self, a, b=None, allowed_distance=None):
        """
        This is the function that checks whether there is enough space for lane changing in the
            lane changing algorithm
        :param a: This is the distance between the Vehicle that requests to change the lane and the
            that ahead of it in the target lane
        :param b: This is the distance between the Vehicle requesting to change lane and the Vehicle behind it
            in the target lane. This can be none for Gap algorithm
        :return: Return True if the space is ample for lane changing and False otherwise
        """
        if allowed_distance == None:
            allowed_distance = 50
        else:
            allowed_distance = allowed_distance
        if a >= allowed_distance:
            if b is not None:
                if b >= allowed_distance:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def check_speed(self, self_speed, preceded_speed, platoon, threshold_speed=None):
        """
        This is the function that checks whether the preceded Vehicle in the target lane has a higher speed
            or that equal to the speed of the platoon
        :param self_speed: This is the speed of the Vehicle that sends the request to change the lane
        :param preceded_speed: This is the speed of the preceded Vehicle in the target lane
        :return: Returns true or false of whether the Vehicle should change lane
        """
        if preceded_speed > threshold_speed:
            return False

        else:
            if self_speed <= preceded_speed:
                return False
            else:
                if self_speed > platoon.threshspeed:
                    return False
                else:
                    return True

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        This is the function that calculates the distance between two Vehicles/two functions
        :param lat1: This is the latitude of the first Vehicle
        :param lat2: This is the latitude of the second Vehicle
        :param lon1: This is the longitude of the first Vehicle
        :param lon2: This is the longitude of the second Vehicle
        :return: the distance between the two vehicles
        """
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def lane_change_desire_necessity(self, Vehicle, route, laneid):
        """
        This is the function that calculates whether it is necessary to change the lane or not.
        It returns True if changing of lane(s) is viable
        :return:
        """

        def dkr(Vehicle, route, laneid):
            """
            This is the function that calculates the desire to change
            :param Vehicle: This is the class with Vehicle details
            :param route: This is the class with route details
            :param laneid: This is the laneid or the target lane
            :return: returns whether the change is desirable and the desire value
            """
            x0 = 200  # This is the avaailable look distance
            lane = route[laneid]
            nk = self.path_distance(lane.lane_ending_latitude, lane.lane_ending_longitude, Vehicle.lat, Vehicle.long)
            xk = nk
            tk = xk / Vehicle.speed
            desire_based_on_distance = 1 - (xk / (nk * x0))
            desire_based_on_time = 1 - (tk / (nk * x0))
            testarray = [desire_based_on_distance, desire_based_on_time, 0]
            desire = np.argmax(testarray)
            desirevalue = np.max(testarray)

            if desire == 0:
                change_desirable = 'Yes'
                print('The desire is based on distance. The platoon is moving at a relatively low speed')
            elif desire == 1:
                change_desirable = "Yes"
                print('The desire is based on time. The platoon is moving at a relatively high speed')
            else:
                change_desirable = 'No'
                print('There is no desire to change or change or lane is undesirable')
            return change_desirable, desirevalue

        def mandatory_change(desirevalue_platoon_lane, desirevalue_target_lane):
            """
            This is the function that checks for mandatory change
            :param desirevalue_platoon_lane: This is the desire value of the platoon lane
            :param desirevalue_target_lane:  This is the desire value of the target lane
            :return: It returns desire for mandatory change and the 'boolean of mandatory change
            """
            if desirevalue_platoon_lane > desirevalue_target_lane:
                mandatory_change = "True"
                desire = desirevalue_platoon_lane
            elif desirevalue_platoon_lane == desirevalue_target_lane:
                mandatory_change = "False"
                desire = desirevalue_platoon_lane
            elif desirevalue_platoon_lane < desirevalue_target_lane:
                mandatory_change = "False"
                desire = 0
            else:
                desire = 0
            return mandatory_change, desire

        if laneid < 0:
            exit()
            print('Invalid lane ID. Lane change aborted')
        elif laneid > len(route.lanes):
            print('The lane does not exist. Lane change aborted')
        else:
            # We check whether the desire is mandatory
            change_desirable_target_lane, desirevalue_target_lane = dkr(Vehicle, route, laneid)
            change_desirable_platoon_lane, desirevalue_platoon_lane = dkr(Vehicle, route, Vehicle.laneid)
            if change_desirable_platoon_lane == 'Yes':
                if change_desirable_target_lane == "Yes":
                    mandatory_change, desire = mandatory_change(desirevalue_platoon_lane, desirevalue_target_lane)
                else:
                    mandatory_change, desire = mandatory_change(desirevalue_platoon_lane, desirevalue_target_lane)
            else:
                mandatory_change, desire = mandatory_change(desirevalue_platoon_lane, desirevalue_target_lane)
        return mandatory_change, desire, desirevalue_target_lane

    def path_distance(self, pathlat, pathlong, Vehiclelat, Vehiclelong):
        """
        This is the function that uses googlemaps API(Openstreetmap API) to calculate the remaining
            distance for the lane and the route.
            This function may also be used to calculate whether the lane and route have the same length
            or the lane ends before the route.
        :param path: These are the coordinates of a lane or a route
        :param Vehicle: these are the coordinates of a Vehicle that wants to change lane(we use the last Vehicle of a
            platoon as the reference
        :return: the distance
        """
        try:
            try:
                import requests
                import json  # call the OSMR API
                from geopy import distance

                d = distance.distance((pathlat, pathlong),
                                      (Vehiclelat, Vehiclelong))
                return (abs(getattr(d, "km") * 1000))


            except:
                # This works incase the google API fails
                d = self.calculate_distance(pathlat, pathlong, Vehiclelat, Vehiclelong)
                return abs(d)
        except:
            print('System Error')

    def gap_creation(self, Vehicle1, Vehicle2, Vehicle3):
        """
        This is the function that implements gap creation algorithm once the
        :param Vehicle1: This is the last Vehicle is the platoon
        :param Vehicle2: This is the first Vehicle in the platoon
        :param Vehicle3: This is the preceding Vehicle in the target lane
        :return:success message
        """
        a = self.calculate_distance(Vehicle3.lat, Vehicle3.long, Vehicle2.lat, Vehicle2.long)
        if Vehicle1.lanechangestatus == 'complete':

            if Vehicle2.lanechangestatus == 'in progress':
                goto(1)
                if line == 1:
                    space = self.check_space(a)
                    if space == True:
                        print("Lane change safe")
                        condtion = 'safe'
                    else:
                        print("Lane change not safe")
                        print('decelerating')
                        # decelerate until its safe for all trucks to change lane
                        while space == False:
                            deceleration = (Vehicle2.speed - 5) / 0.016666
                            dv = deceleration * 0.0166666
                            time.sleep(60)
                            Vehicle2.speed = Vehicle2.speed - dv
                        print('decelation complete. Safe to change lane')
                        condition = 'safe'
            elif Vehicle2.lanechangestatus == 'complete':
                print("Lane change completed safely")
            elif Vehicle2.lanechange == '':
                print("Lane change for the lead truck not initiated. Initiate")
                goto(1)
            else:
                print('there is no desire to change lane')
        else:
            print("Gap algorithm not needed")
