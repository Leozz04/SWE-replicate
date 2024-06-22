import readline
from intercode.assets import bash_build_docker, bash_image_name, bash_test_data
from intercode.envs import BashEnv

if __name__ == '__main__':
    bash_build_docker()
    env = BashEnv(bash_image_name, data_path=bash_test_data, traj_dir="logs/", verbose=True)

    try:
        for idx in range(3):
            env.reset()
            obs, done = env.observation, False
            while not done:
                action = input('> ')
                obs, reward, done, info = env.step(action)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    finally:
        env.close()