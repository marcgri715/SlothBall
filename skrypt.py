import bge
import math
import time
from math import sin, cos, pi

def main():

    t1 = time.perf_counter()
    cont = bge.logic.getCurrentController()
    player = cont.owner
    lastTimeProp = player.actuators['lastTimeProp']
    lastTimeVal = player.get(lastTimeProp.propName)
    if lastTimeVal == 0.0:
        lastTimeVal = t1
        lastTimeProp.value = str(lastTimeVal)
        cont.activate(lastTimeProp)
    t2 = t1 - lastTimeVal
    lastTimeVal = t1
    lastTimeProp.value = str(lastTimeVal)
    cont.activate(lastTimeProp)
    rotation = player.actuators['rotProp']
    value = player.get(rotation.propName)
    timer = player.actuators['timeProp']
    timeVal = player.get(timer.propName)
    lap = player.actuators['lapProp']
    lapVal = player.get(lap.propName)
    collision = cont.sensors["collision"]
    camera = bge.logic.getCurrentScene().cameras[0]
    timeText = camera.children[0]
    lapText = camera.children[2]
    bestText = camera.children[3]
    bestProp = player.actuators['bestProp']
    bestVal = player.get(bestProp.propName)
    keyboard = cont.sensors["Keyboard"]
    hitObj = collision.hitObject
    if hitObj is not None:
        if hitObj.get("startLine") == True:
            inMidProp = player.actuators['inMidProp']
            inMidBool = player.get(inMidProp.propName)
            if inMidBool == True:
                lapVal = lapVal + 1
                lap.value = str(lapVal)
                cont.activate(lap)
                if bestVal == -1.0 or bestVal > timeVal:
                    bestVal = timeVal
                    bestProp.value = str(bestVal)
                    cont.activate(bestProp)
                timeVal = 0
                timer.value = str(timeVal)
                cont.activate(timer)
            inMidBool = False
            inMidProp.value = str(inMidBool)
            cont.activate(inMidProp)
        else:
            inMidProp = player.actuators['inMidProp']
            inMidProp.value = str(True)
            cont.activate(inMidProp)
    for key,status in keyboard.events:
        if status == bge.logic.KX_INPUT_ACTIVE:
            if key == bge.events.WKEY:
                player.applyMovement((0.2*math.cos(math.radians(value)),0.2*math.sin(math.radians(value)),0.0))
                player.applyRotation((-0.20*math.sin(math.radians(value)),0.20*math.cos(math.radians(value)),0.0))
            if key == bge.events.SKEY:
                player.applyMovement((-0.1*math.cos(math.radians(value)),-0.1*math.sin(math.radians(value)),0.0))
                player.applyRotation((0.10*math.sin(math.radians(value)),-0.10*math.cos(math.radians(value)),0.0))
            if key == bge.events.AKEY:
                player.applyRotation((0.0,0.0,0.05))
                camera.applyRotation((0.0,0.0,0.05))
                rot = math.degrees(0.05)
                newValue = value + rot
                if newValue > 180:
                    newValue = newValue - 360
                rotation.value = str(newValue)
                cont.activate(rotation)
                value = newValue
            if key == bge.events.DKEY:
                player.applyRotation((0.0,0.0,-0.05))
                camera.applyRotation((0.0,0.0,-0.05))
                rot = math.degrees(0.05)
                newValue = value - rot
                if newValue < -180:
                    newValue = newValue + 360
                rotation.value = str(newValue)
                cont.activate(rotation)
                value = newValue
        if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            if key == bge.events.SPACEKEY:
                player.applyForce((0.0,0.0,600.0))
    position = player.worldPosition
    camera.worldPosition = (position[0]-8.0*math.cos(math.radians(value)), position[1] - 8.0*math.sin(math.radians(value)), position[2] + 3.5)
    timeVal = timeVal + t2
    timer.value = str(timeVal)
    cont.activate(timer)
    timeText['Text'] = "%.3f s" % (timeVal)
    lapText['Text'] = "Lap " + str(lapVal + 1)
    bestText['Text'] = "Best: %.3f" % (bestVal)
main()
