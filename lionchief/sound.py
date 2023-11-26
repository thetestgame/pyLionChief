"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.
"""

from lionchief.protocol import *

class LionChiefAudioDevices(object):
    """
    Class representing the audio devices used in the LionChief protocol.
    """

    Horn = 0x01
    Bell = 0x02
    Speech = 0x03
    Engine = 0x04

class LionChiefSoundController(object):
    """
    Class for controlling the sound functions of a LionChief train
    """

    def __init__(self, train: object) -> None:
        """
        Initialize a LionChiefSoundController object.

        Args:
            train (object): The train object.
        """

        self.train = train

    async def set_steam_volume(self, volume: int) -> None:
        """
        Set the steam volume of the train.

        Args:
            volume (int): The volume of the steam (0 to 4).
        """

        volumes = [0xfe, 0xff, 0, 1, 2]
        if volume < 0 or volume >= len(volumes):
            raise ValueError("Steam volume must be between 0 and %s" % volume)

        await self.train.send_train_command(LionChiefBluetoothCommands.SetSteamVolume, [volumes[volume]])

    async def set_horn(self, state: bool) -> None:
        """
        Set the state of the train's horn.

        Args:
            state (bool): The state of the horn (True for on, False for off).
        """

        await self.train.send_train_command(LionChiefBluetoothCommands.SetHornState, [1 if state else 0])

    async def set_bell(self, state: bool) -> None:
        """
        Set the state of the train's bell.

        Args:
            state (bool): The state of the bell (True for on, False for off).
        """

        await self.train.send_train_command(LionChiefBluetoothCommands.SetBellState, [1 if state else 0])

    async def set_horn_pitch(self, pitch: int) -> None:
        """
        Set the pitch of the train's horn.

        Args:
            pitch (int): The pitch of the horn (0 to 4).
        """

        pitches = [0xfe, 0xff, 0, 1, 2]
        if pitch < 0 or pitch >= len(pitches):
            raise ValueError("Horn pitch must be between 0 and %s" % pitch)

        await self.train.send_train_command(LionChiefBluetoothCommands.SetEffectVolume, [LionChiefAudioDevices.Horn, 0x0e, pitches[pitch]])

    async def set_bell_pitch(self, pitch: int) -> None:
        """
        Set the pitch of the train's bell.

        Args:
            pitch (int): The pitch of the bell (0 to 4).
        """

        pitches = [0xfe, 0xff, 0, 1, 2]
        if pitch < 0 or pitch >= len(pitches):
            raise ValueError("Bell pitch must be between 0 and %s" % pitch)

        await self.train.send_train_command(LionChiefBluetoothCommands.SetEffectVolume, [LionChiefAudioDevices.Bell, 0x0e, pitches[pitch]])

    async def set_voice_line_volume(self, volume: int) -> None:
        """
        Set the volume of the train's voice lines.

        Args:
            volume (int): The volume of the voice lines (0 to 4).
        """

        volumes = [0xfe, 0xff, 0, 1, 2]
        if volume < 0 or volume >= len(volumes):
            raise ValueError("Voice volume must be between 0 and %s" % volume)

        await self.train.send_train_command(LionChiefBluetoothCommands.SetEffectVolume, [LionChiefAudioDevices.Speech, 0x0e, volumes[volume]])

    async def set_engine_volume(self, volume: int) -> None:
        """
        Set the volume of the train's engine.

        Args:
            volume (int): The volume of the engine (0 to 4).
        """

        volumes = [0xfe, 0xff, 0, 1, 2]
        if volume < 0 or volume >= len(volumes):
            raise ValueError("Voice volume must be between 0 and %s" % volume)

        await self.train.send_train_command(LionChiefBluetoothCommands.SetEffectVolume, [LionChiefAudioDevices.Engine, 0x0e, volumes[volume]])

    async def play_voice_line(self) -> None:
        """
        Play a voice line on the train.
        """

        await self.train.send_train_command(LionChiefBluetoothCommands.PlayVoiceLine, [0, 0])