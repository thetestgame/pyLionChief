"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.
"""

from lionchief.protocol import *

class LionChiefMotorController(object):
    """
    Class for controlling the motor functions of a LionChief train
    """

    def __init__(self, train: object) -> None:
        """
        Initialize a LionChiefMotorController object.

        Args:
            train (object): The train object.
        """

        self.train = train

    async def set_speed(self, speed: int) -> None:
        """
        Set the speed of the train.

        Args:
            speed (int): The speed of the train.
        """
        await self.train.send_train_command(LionChiefBluetoothCommands.SetSpeed, [speed])

    async def set_movement_direction(self, forward: bool) -> None:
        """
        Set the state of the train's movement direction.

        Args:
            state (bool): Movement direction value (True for forward, False for reverse).
        """
        await self.train.send_train_command(LionChiefBluetoothCommands.SetMovementDirection, [0x01 if forward else 0x02])

    