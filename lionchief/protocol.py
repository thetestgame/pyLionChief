"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.
"""

class LionChiefBluetoothCharacteristics(object):
    """
    Class representing the Bluetooth characteristics used in the LionChief protocol.
    """

    LionChiefReadCharacteristic = "00002902-0000-1000-8000-00805f9b34fb"
    LionChiefWriteCharacteristic = "08590f7e-db05-467e-8757-72f6faeb13d4"

class LionChiefBluetoothCommands(object):
    """
    Class representing the Bluetooth commands used in the LionChief protocol.
    """

    SetHornState = 0x48
    SetBellState = 0x47
    SetBellPitch = 0x44
    PlayVoiceLine = 0x4d
    SetSpeed = 0x45
    SetMovementDirection = 0x46
    Disconnect = 0x4b
    SetSteamVolume = 0x4c
    SetEffectVolume = 0x44
    SetLightsState = 0x51
