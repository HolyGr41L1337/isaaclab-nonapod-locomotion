# Nonapod Isaac Lab

`Nonapod Isaac Lab` is a small external project for NVIDIA Isaac Lab that provides a custom trainable nine-legged robot.

The project is designed as a starting point for experimentation with custom legged locomotion tasks. It includes a generated URDF robot, an Isaac Lab direct reinforcement learning environment, and an RSL-RL PPO training setup.

## Overview

This repository includes:

- A custom `nonapod` robot with `9 legs` and `18 actuated joints`
- A reusable URDF generator script for changing robot dimensions and joint settings
- A direct-workflow Isaac Lab locomotion environment
- An `RSL-RL` PPO configuration for training
- Utility scripts for listing environments, training, and policy playback

## Robot Design

- Body: rectangular central chassis
- Leg layout: `3 x 3`
- Total legs: `9`
- Degrees of freedom per leg: `2`
- Total action dimension: `18`

The goal of this design is not to perfectly model a real-world commercial robot, but to provide a clean custom embodiment that can be extended for locomotion research and learning experiments.

## Requirements

This project is intended for use with `NVIDIA Isaac Lab` and `Isaac Sim`.

You will need:

- A supported `Ubuntu` or `Windows` environment for Isaac Sim / Isaac Lab
- An `NVIDIA RTX GPU`
- A working Isaac Lab installation

Note: this repository can be edited on macOS, but training must be run on a supported Isaac Lab machine.

## Installation

Clone or copy this repository outside your Isaac Lab source tree, then install it in the Isaac Lab Python environment:

```bash
python -m pip install -e source/nonapod_lab
```

## Available Environment

The main task registered by this project is:

```bash
Isaac-Nonapod-Direct-v0
```

You can list registered project environments with:

```bash
python scripts/list_envs.py
```

## Training

Run PPO training with:

```bash
python scripts/rsl_rl/train.py --task Isaac-Nonapod-Direct-v0 --headless
```

You can also override the number of environments or training iterations if needed:

```bash
python scripts/rsl_rl/train.py --task Isaac-Nonapod-Direct-v0 --headless --num_envs 512 --max_iterations 1000
```

## Playing a Trained Policy

After training, you can load and play the latest checkpoint with:

```bash
python scripts/rsl_rl/play.py --task Isaac-Nonapod-Direct-v0 --num_envs 1
```

## Customizing the Robot

If you want to change the robot size, leg spacing, masses, or joint limits, edit:

```bash
scripts/generate_nonapod_urdf.py
```

Then regenerate the URDF:

```bash
python scripts/generate_nonapod_urdf.py
```

The generated robot file is stored at:

```bash
source/nonapod_lab/nonapod_lab/assets/robots/nonapod/nonapod.urdf
```

## Project Structure

- `scripts/generate_nonapod_urdf.py` - Generates the nine-legged robot URDF
- `scripts/list_envs.py` - Lists registered Isaac Lab environments from this project
- `scripts/rsl_rl/train.py` - Launches PPO training with RSL-RL
- `scripts/rsl_rl/play.py` - Plays a trained checkpoint
- `source/nonapod_lab/nonapod_lab/assets/nonapod_cfg.py` - Isaac Lab articulation configuration for the robot
- `source/nonapod_lab/nonapod_lab/tasks/direct/nonapod/nonapod_env.py` - Environment configuration
- `source/nonapod_lab/nonapod_lab/tasks/direct/nonapod/locomotion_env.py` - Locomotion task logic
- `source/nonapod_lab/nonapod_lab/tasks/direct/nonapod/agents/rsl_rl_ppo_cfg.py` - PPO runner configuration

## Future Improvements

Possible next steps for this project include:

- Better contact and stability rewards
- Velocity-command tracking instead of fixed forward-target locomotion
- Additional observations such as IMU or contact sensors
- Domain randomization for more robust training
- More advanced leg geometry and gait tuning

## License

This project is provided as a custom Isaac Lab example project. Add your preferred license here before publishing if needed.
UU i love u
