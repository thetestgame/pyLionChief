"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.
"""

import asyncio
import logging
from time import sleep
from threading import Thread
from bleak import BleakScanner, BleakClient
from lionchief.protocol import *

class LionChiefConnection(object):
    """
    Represents a connection to a LionChief train.
    """

    LionChiefServiceId = 'e20a39f4-73f5-4bc4-a12f-17d1ad07a961'

    def __init__(self, profile: str, manufacturer_data):
        """
        Initialize a LionChiefConnection object.

        Args:
            profile (str): The BLE profile of the train.
            manufacturer_data: The manufacturer data of the train.
        """
        
        self.profile = profile
        self.train = None
        self.manufacturer_data = manufacturer_data

    async def connect(self, silent: bool = False) -> None:
        """
        Connect to the LionChief train using BLE.
        """

        timeout = 0.0
        self.train = BleakClient(self.profile)
        await self.train.connect()

    async def disconnect(self, silent: bool = False) -> None:
        """
        Disconnect from the train.
        """

        if not self.train.is_connected:
            return

        logging.info("Disconnecting from train...")
        await self.train.disconnect()

        if self.heartbeat_loop != None:
            self.heartbeat_loop.stop()

    async def send_train_command(self, command_id: int, values: list = []) -> None:
        """
        Send a command to the train.

        Args:
            command_id (int): The ID of the command.
            values (list): The values to be sent along with the command.
        """
        values.insert(0, command_id)

        checksum = 256
        for v in values:
            checksum -= v

        while checksum < 0:
            checksum += 256

        values.insert(0, 0)
        values.append(checksum)

        command = bytes(values)
        print('Sending command: %s' % command.hex())
        await self.train.write_gatt_char(LionChiefBluetoothCharacteristics.LionChiefWriteCharacteristic, command)

    async def set_horn(self, state: bool) -> None:
        """
        Set the state of the train's horn.

        Args:
            state (bool): The state of the horn (True for on, False for off).
        """
        await self.send_train_command(0x48, [1 if state else 0])

    async def set_bell(self, state: bool) -> None:
        """
        Set the state of the train's bell.

        Args:
            state (bool): The state of the bell (True for on, False for off).
        """
        await self.send_train_command(0x47, [1 if state else 0])

    async def set_bell_pitch(self, pitch: int) -> None:
        """
        Set the pitch of the train's bell.

        Args:
            pitch (int): The pitch of the bell (0 to 4).
        """
        pitches = [0xfe, 0xff, 0, 1, 2]
        if pitch < 0 or pitch >= len(pitches):
            raise ValueError("Bell pitch must be between 0 and %s" % pitch)

        await self.send_train_command(0x44, [0x02, 0x0e, pitches[pitch]])

    async def play_voice_line(self) -> None:
        """
        Play a voice line on the train.
        """
        await self.send_train_command(0x4d, [0, 0])

    async def set_speed(self, speed: int) -> None:
        """
        Set the speed of the train.

        Args:
            speed (int): The speed of the train.
        """
        await self.send_train_command(0x45, [speed])

    async def set_reverse(self, state: bool) -> None:
        """
        Set the state of the train's reverse.

        Args:
            state (bool): The state of the reverse (True for on, False for off).
        """
        await self.send_train_command(0x46, [0x02 if state else 0x01])

async def discover_trains(retry: bool = False) -> list:
    """
    Scans for nearby Bluetooth devices with the LionChief service id and returns if found. If retry is True, the function will
    converted to a DroidConnection and added to a list to return. If retry is False, the function will out after a set
    period of time and return without discovering any trains.

    Args:
        retry (bool): whether or not to continue scanning until a device is found or the function is interrupted

    Returns:
        a list of LionChiefConnection objects representing the discovered train Bluetooth devices if any. Otherwise an empty list
    """

    async with BleakScanner() as scanner:      
        await scanner.start()

        train_connections = []
        trains = []
        while True:
            possible_trains = scanner.discovered_devices_and_advertisement_data
            if len(possible_trains) == 0:
                await asyncio.sleep(5)
                continue

            for possible_train_address in possible_trains:
                ble_device, advertising_data = possible_trains[possible_train_address]
                manufacturer_ids = list(advertising_data.manufacturer_data.keys()) if advertising_data.manufacturer_data != None else []

                if LionChiefConnection.LionChiefServiceId in advertising_data.service_uuids:
                    trains.append((ble_device, advertising_data.manufacturer_data))
                    
            if len(trains) == 0:
                if not retry:
                    logging.error("Train discovery failed. Retrying...")
                    await asyncio.sleep(5)
                    continue
                else:
                    logging.warning("Train discovery failed. Retrying...")
                    await asyncio.sleep(5)
                    continue
            else:
                for discovered_train in trains:
                    logging.info(f"Train successfully discovered: [ {discovered_train[0]} ]")
                    train_connections.append(LionChiefConnection(*discovered_train))
                break
    
    return train_connections

async def discover_train(retry: bool = False) -> LionChiefConnection:
    """
    Scans for nearby Bluetooth devices with the LionChief service id and returns if found. If retry is True, the function will
    continue scanning until it finds a device or is interrupted. If retry is False, the function will time out after a
    set period of time and return without discovering a device.

    Args:
        retry (bool): whether or not to continue scanning until a device is found or the function is interrupted

    Returns:
        a LionChiefConnection object representing the discovered train Bluetooth device if any. Otherwise None
    """

    discovered_trains = await discover_trains(retry)
    return None if len(discovered_trains) == 0 else discovered_trains[0]