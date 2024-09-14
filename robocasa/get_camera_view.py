import robocasa
import robosuite
from robosuite import load_controller_config
import cv2

env = robosuite.make(
    env_name="PnPCounterToCab", # set to your task
    robots="PandaMobile",
    controller_configs=load_controller_config(default_controller="OSC_POSE"),
    # add additional env params here as needed
    
    # rendering settings
    has_renderer=False,
    has_offscreen_renderer=True,
    use_camera_obs=True,
    camera_depths=False, # set to True to also render depth
    camera_names=["robot0_agentview_left", "robot0_agentview_right", "robot0_eye_in_hand"],
)

obs = env.reset()
while True: # continually step
  im = obs["robot0_agentview_left_image"] # returns rgb values represented as numpy array
  # action = policy(obs) # LLM, policy, etc
  # obs, _, _, _ = env.step(action) # step through environment
  im_bgr = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
  cv2.imshow('Agent View Left', im_bgr)
  if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
  