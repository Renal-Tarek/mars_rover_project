import numpy as np
import time

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):
    X=0
    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward':
            if Rover.samples_collected>=6:
                if abs(Rover.pos[0] - Rover.Home_pos[0]) < 20 and abs(Rover.pos[1] - Rover.Home_pos[1]) < 20:
                   Rover.mode='home_sweet_home'
            if Rover.vel < 0.2 and Rover.throttle != 0:
                Rover.stuck_times+=1
                # If the velocity is still 0 after throttle, it's stuck
                if Rover.stuck_times > Rover.MAX_stuck_time:
                    # Initiate stuck mode after 5 seconds of not moving
                    Rover.mode = 'stuck'
            # Check the extent of navigable terrain
            elif len(Rover.nav_angles) >= Rover.stop_forward:
                Rover.stuck_times=0
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -13, 13)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                elif len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
                
        elif Rover.mode=='rock':
            '''''
            if time.time()-Rover.time>20:
                Rover.time=time.time()
                Rover.mode='forward'
                Rover.found= False
                return Rover
            '''
            if Rover.picking_up != 0 or Rover.Rock_stuck>=400:
                # Reset sample_seen flag
                Rover.found= False
                Rover.mode='forward'
                Rover.Rock_stuck=0
                return Rover
            else:
                Rover.Rock_stuck+=1
            avg_rock_angle = np.mean(Rover.Rock_angle * 180/np.pi)
            if -15 < avg_rock_angle < 15:
                # Only drive straight for sample if it's within 13 deg
                if max(Rover.Rock_dist) <= 20:
                    if Rover.vel <= 0.2:
                        Rover.throttle = Rover.throttle_set
                        Rover.steer = avg_rock_angle
                    else:
                        Rover.throttle = 0
                        Rover.brake = Rover.brake_set
                        Rover.steer = avg_rock_angle
                else:
                    # Set throttle at half normal speed during approach
                    Rover.throttle = Rover.throttle_set
                    Rover.steer = avg_rock_angle
            elif -50 < avg_rock_angle < 50:
                if Rover.vel > 0 and max(Rover.Rock_dist) < 40:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                else:
                    Rover.throttle = 0
                    Rover.brake = 0
                    Rover.steer = avg_rock_angle/6
            else:
                # Keep the logic simple and ignore samples +/-13 degrees
                Rover.found = False
                Rover.mode='forward'
                return Rover
            # Just to make the rover do something 
            # even if no modifications have been made to the cod
        elif Rover.mode == 'stuck':
            if Rover.stuck_times > (Rover.MAX_stuck_time + 20):
                Rover.stuck_times =0
                Rover.mode = 'forward'
            else:
            # Perform evasion to get unstuck
                Rover.throttle = 0
                Rover.brake = 0
                Rover.steer = -15
                Rover.stuck_times +=1
        elif Rover.mode=='home_sweet_home':
            Rover.throttle=0
            Rover.steer = 0
            Rover.brake=Rover.brake_set
            return Rover
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
    

    if Rover.found==True:
        Rover.mode='rock'    
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

