import gymnasium as gym

from . import agents

gym.register(
    id="Isaac-Nonapod-Direct-v0",
    entry_point=f"{__name__}.nonapod_env:NonapodEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.nonapod_env:NonapodEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:NonapodPPORunnerCfg",
    },
)

gym.register(
    id="Isaac-Nonapod-Direct-Play-v0",
    entry_point=f"{__name__}.nonapod_env:NonapodEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.nonapod_env:NonapodEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:NonapodPPORunnerCfg",
    },
)
