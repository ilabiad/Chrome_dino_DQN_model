from stable_baselines3 import DQN
from Custom_Env import ChromeDinoEnv

env = ChromeDinoEnv()

model = DQN("CnnPolicy", env, buffer_size=10**4, verbose=1, tensorboard_log="./TensorBoard")

model.learn(total_timesteps=60000, log_interval=4)

# model.save("./Saved_models/DQN_model")

# del model
# model.load("./Saved_models/DQN_model")

episodes = 5
for episode in range(1, episodes + 1):
    obs = env.reset()
    done = False
    score = 0

    while not done:
        env.render()
        action, _states = model.predict(obs.copy(), deterministic=True)
        obs, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))
env.close()










