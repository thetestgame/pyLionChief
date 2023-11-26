"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.
"""

from lionchief.protocol import *

class LionChiefLightingController(object):
    """
    Class for controlling the lighting functions of a LionChief train
    """

    def __init__(self, train: object) -> None:
        """
        Initialize a LionChiefLightingController object.

        Args:
            train (object): The train object.
        """

        self.train = train

    async def set_lights(self, state: bool) -> None:
        """
        Set the state of the train's lights.

        Args:
            state (bool): The state of the lights (True for on, False for off).
        """

        await self.train.send_train_command(LionChiefBluetoothCommands.SetLightsState, [1 if state else 0])