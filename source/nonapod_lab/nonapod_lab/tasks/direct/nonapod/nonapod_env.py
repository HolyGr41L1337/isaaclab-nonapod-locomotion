from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg
from isaaclab.envs import DirectRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils import configclass

from nonapod_lab.assets import NONAPOD_CFG

from .locomotion_env import LocomotionEnv


@configclass
class NonapodEnvCfg(DirectRLEnvCfg):
    episode_length_s = 20.0
    decimation = 4
    action_scale = 1.0
    action_space = 18
    observation_space = 66
    state_space = 0

    sim: SimulationCfg = SimulationCfg(dt=1 / 120, render_interval=decimation)
    terrain = TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="plane",
        collision_group=-1,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="average",
            restitution_combine_mode="average",
            static_friction=1.2,
            dynamic_friction=1.0,
            restitution=0.0,
        ),
        debug_vis=False,
    )

    scene: InteractiveSceneCfg = InteractiveSceneCfg(
        num_envs=1024,
        env_spacing=3.0,
        replicate_physics=True,
        clone_in_fabric=True,
    )

    robot: ArticulationCfg = NONAPOD_CFG.replace(prim_path="/World/envs/env_.*/Robot")
    joint_gears: list[float] = [20.0, 28.0] * 9

    heading_weight: float = 0.8
    up_weight: float = 0.2
    energy_cost_scale: float = 0.04
    actions_cost_scale: float = 0.01
    alive_reward_scale: float = 0.5
    dof_vel_scale: float = 0.05

    death_cost: float = -2.5
    termination_height: float = 0.12
    angular_velocity_scale: float = 0.25
    contact_force_scale: float = 0.0


@configclass
class NonapodEnvCfg_PLAY(NonapodEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 32
        self.scene.env_spacing = 3.5


class NonapodEnv(LocomotionEnv):
    cfg: NonapodEnvCfg

    def __init__(self, cfg: NonapodEnvCfg, render_mode: str | None = None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)
