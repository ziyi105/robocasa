from robocasa.environments.kitchen.kitchen import *


class MoveStool(Kitchen):
    """
    Class encapsulating the atomic pick and place tasks.

    Args:
        obj_groups (str): Object groups to sample the target object from.

        exclude_obj_groups (str): Object groups to exclude from sampling the target object.
    """

    def __init__(self, obj_groups="stool", exclude_obj_groups=None, *args, **kwargs):
        self.obj_groups = obj_groups
        self.exclude_obj_groups = exclude_obj_groups

        super().__init__(*args, **kwargs)

    def _get_obj_cfgs(self):
        raise NotImplementedError


class MoveStoolFromSinkToCounter(MoveStool):
    """
    Class encapsulating the atomic sink to counter move Stool task

    Args:
        cab_id (str): The counter fixture id to place the object.

        obj_groups (str): Object groups to sample the target object from.
    """

    def __init__(self, obj_groups="stool", *args, **kwargs):

        super().__init__(obj_groups=obj_groups, *args, **kwargs)

    def _setup_kitchen_references(self):
        """
        Setup the kitchen references for the sink to counter move Stool task:
        The counter to place object near and the sink to initialize it on
        """
        super()._setup_kitchen_references()
        self.sink = self.register_fixture_ref(
            "sink",
            dict(id=FixtureType.SINK),
        )
        self.counter = self.register_fixture_ref(
            "counter",
            dict(id=FixtureType.COUNTER),
        )
        self.init_robot_base_pos = self.sink

    def get_ep_meta(self):
        """
        Get the episode metadata for the sink to counter move Stool task.
        This includes the language description of the task.
        """
        ep_meta = super().get_ep_meta()
        obj_lang = self.get_obj_lang("stool")
        ep_meta[
            "lang"
        ] = f"move the {obj_lang} from the sink to counter"
        return ep_meta
    
    def _reset_internal(self):
        """
        Resets simulation internal configurations.
        """
        super()._reset_internal()
        # self.cab.set_door_state(min=0.90, max=1.0, env=self, rng=self.rng)
    
    def _get_obj_cfgs(self):
        """
        Get the object configurations for the sink to counter move Stool task.
        Puts the target object in the front area of the sink. Puts a distractor object near the sink
        and the sink.
        """
        cfgs = []
        cfgs.append(
            dict(
                name="stool",
                obj_groups=self.obj_groups,
                exclude_obj_groups=self.exclude_obj_groups,
                graspable=True,
                washable=True,
                placement=dict(
                    fixture=self.sink,
                    sample_region_kwargs=dict(
                        ref=self.counter,
                        loc="left_right",
                    ),
                    size=(0.30, 0.40), # increase the size?
                    pos=("ref", -1.0),
                ),
            )
        )

        return cfgs

    def _check_success(self):
        """
        Check if the sink to counter move Stool task is successful.
        Checks if the Stool is near the counter.

        Returns:
            bool: True if the task is successful, False otherwise
        """
        # Retrieve the position and orientation of the stool
        # print("Available body names:", self.sim.model.body_names)
        stool = self.sim.model.body_name2id("stool_main")
        obj_pos = self.sim.data.body_xpos[stool]
        obj_quat = self.sim.data.body_xquat[stool]

        # Use the fixture properties to get the necessary positions for the counter
        p0, px, py, pz = self.counter.get_ext_sites()  # Get the other bounding box points

        # Use obj_in_region to check if the stool is within this region
        Stool_near_counter = OU.obj_in_region(
            obj=self.objects["stool"],
            obj_pos=obj_pos,
            obj_quat=obj_quat,
            p0=p0,
            px=px,
            py=py,
            pz=pz,
        )

        return Stool_near_counter  # Return the result

