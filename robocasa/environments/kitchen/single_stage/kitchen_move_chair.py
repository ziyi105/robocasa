from robocasa.environments.kitchen.kitchen import *


class MoveChair(Kitchen):
    """
    Class encapsulating the atomic pick and place tasks.

    Args:
        obj_groups (str): Object groups to sample the target object from.

        exclude_obj_groups (str): Object groups to exclude from sampling the target object.
    """

    def __init__(self, obj_groups="all", exclude_obj_groups=None, *args, **kwargs):
        self.obj_groups = obj_groups
        self.exclude_obj_groups = exclude_obj_groups

        super().__init__(*args, **kwargs)

    def _get_obj_cfgs(self):
        raise NotImplementedError


class MoveChairSinkToCounter(PnP):
    """
    Class encapsulating the atomic sink to counter move chair task

    Args:
        cab_id (str): The counter fixture id to place the object.

        obj_groups (str): Object groups to sample the target object from.
    """

    def __init__(self, obj_groups="all", *args, **kwargs):

        super().__init__(obj_groups=obj_groups, *args, **kwargs)

    def _setup_kitchen_references(self):
        """
        Setup the kitchen references for the sink to counter move chair task:
        """
        super()._setup_kitchen_references()
        self.sink = self.register_fixture_ref(
            "sink",
            dict(id=FixtureType.SINK),
        )
        self.counter = self.register_fixture_ref(
            "counter",
            dict(id=FixtureType.COUNTER, ref=self.sink),
        )
        self.init_robot_base_pos = self.sink

    def get_ep_meta(self):
        """
        Get the episode metadata for the sink to counter move chair task.
        This includes the language description of the task.
        """
        ep_meta = super().get_ep_meta()
        obj_lang = self.get_obj_lang()
        ep_meta[
            "lang"
        ] = f"move the {obj_lang} from the sink to counter"
        return ep_meta
    
    def _get_obj_cfgs(self):
        """
        Get the object configurations for the sink to counter move chair task.
        Puts the target object in the front area of the sink. Puts a distractor object near the sink
        and the sink.
        """
        cfgs = []
        cfgs.append(
            dict(
                name="obj",
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
        Check if the sink to counter move chair task is successful.
        Checks if the chair is near the counter.

        Returns:
            bool: True if the task is successful, False otherwise
        """
        chair_near_counter = OU.point_in_fixture(self, "obj", self.counter)
        return chair_near_counter
