import numpy as np
from neuronav.utils import onehot, twohot
from neuronav.envs.graph_env import GraphEnv, GraphObservation
from neuronav.envs.grid_env import GridEnv, GridSize, GridObservation, GridOrientation
from neuronav.envs.graph_templates import GraphTemplate
from neuronav.envs.grid_templates import GridTemplate


def test_one_hot():
    a = onehot(1, 5)
    assert a.all() == np.array([0, 1, 0, 0, 0]).all()


def test_two_hot():
    a = twohot([1, 1], 3)
    assert a.all() == np.array([0, 1, 0, 0, 1, 0]).all()


def test_objects_graph():
    objects = {"rewards": {0: 1}}
    env = GraphEnv()
    env.reset(objects=objects)
    env.step(env.action_space.sample())


def test_objects_grid():
    objects = {
        "rewards": {(1, 1): 1, (2, 2): [1, True, False]},
        "markers": {(1, 1): (1, 0, 0)},
        "doors": {(3, 3): "v"},
        "keys": [[4, 4]],
    }
    env = GridEnv()
    env.reset(objects=objects)
    env.step(env.action_space.sample())


def test_graph_obs():
    for obs_type in GraphObservation:
        env = GraphEnv(obs_type=obs_type)
        obs = env.reset()
        env.step(env.action_space.sample())
        if obs_type != GraphObservation.index:
            assert obs.shape == env.obs_space.shape


def test_graph_templates():
    for template in GraphTemplate:
        env = GraphEnv(template=template)
        env.reset()


def test_grid_orient():
    for obs_type in GridObservation:
        env = GridEnv(orientation_type=GridOrientation.variable, obs_type=obs_type)
        obs = env.reset()
        env.step(env.action_space.sample())
        if obs_type != GridObservation.index:
            assert obs.shape == env.obs_space.shape


def test_grid_obs():
    for obs_type in GridObservation:
        env = GridEnv(obs_type=obs_type)
        obs = env.reset()
        # check that obs is not none. Output the obs_type if it is
        assert obs is not None, obs_type
        env.step(env.action_space.sample())
        if obs_type != GridObservation.index:
            assert obs.shape == env.obs_space.shape


def test_grid_templates():
    for template in GridTemplate:
        for size in GridSize:
            env = GridEnv(template=template, size=size)
            env.reset()


def test_seed_gridenv():
    env = GridEnv(seed=0, obs_type=GridObservation.symbolic)
    env.reset(stochasticity=1.0)
    obs_a, rew, don, _ = env.step(env.action_space.sample())
    env = GridEnv(seed=0, obs_type=GridObservation.symbolic)
    env.reset(stochasticity=1.0)
    obs_b, rew, don, _ = env.step(env.action_space.sample())
    assert obs_a.all() == obs_b.all()


def test_seed_graphenv():
    env = GraphEnv(seed=0, obs_type=GraphObservation.onehot)
    env.reset(stochasticity=1.0)
    obs_a, rew, don, _ = env.step(env.action_space.sample())
    env = GraphEnv(seed=0, obs_type=GraphObservation.onehot)
    env.reset(stochasticity=1.0)
    obs_b, rew, don, _ = env.step(env.action_space.sample())
    assert obs_a.all() == obs_b.all()


def test_gridenv_stochasticity():
    env = GridEnv(seed=0, obs_type=GridObservation.symbolic)
    action = 0
    env.reset(stochasticity=1.0)
    env.step(action)
    pos_a = env.agent_pos
    env.reset(stochasticity=0.0)
    env.step(action)
    pos_b = env.agent_pos
    assert pos_a != pos_b


def test_grid_visible_walls():
    env = GridEnv(obs_type=GridObservation.visual)
    obs_a = env.reset(visible_walls=True)
    obs_b = env.reset(visible_walls=False)
    assert not np.array_equal(obs_a, obs_b)
