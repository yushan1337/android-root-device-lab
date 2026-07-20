import pytest
from android_device_lab.models import DeviceState, ConnectedDevice
from android_device_lab.adb import select_device
from android_device_lab.exceptions import AdbDeviceError

def test_select_device_auto_selects_single_available_device() -> None:
    devices = [
        ConnectedDevice(serial="ABC123", state=DeviceState.DEVICE),
    ]

    selected = select_device(devices, requested_serial=None)

    assert selected.serial == "ABC123"


def test_select_device_requires_serial_for_multiple_available_devices() -> None:
    devices = [
        ConnectedDevice(serial="ABC123", state=DeviceState.DEVICE),
        ConnectedDevice(serial="XYZ999", state=DeviceState.DEVICE),
    ]

    with pytest.raises(AdbDeviceError):
        select_device(devices, requested_serial=None)


def test_select_device_uses_requested_serial() -> None:
    devices = [
        ConnectedDevice(serial="ABC123", state=DeviceState.DEVICE),
        ConnectedDevice(serial="XYZ999", state=DeviceState.DEVICE),
    ]

    selected = select_device(devices, requested_serial="XYZ999")

    assert selected.serial == "XYZ999"


def test_select_device_rejects_unknown_serial() -> None:
    devices = [
        ConnectedDevice(serial="ABC123", state=DeviceState.DEVICE),
    ]

    with pytest.raises(AdbDeviceError):
        select_device(devices, requested_serial="NOPE")


def test_select_device_rejects_unauthorized_device() -> None:
    devices = [
        ConnectedDevice(serial="ABC123", state=DeviceState.UNAUTHORIZED),
    ]

    with pytest.raises(AdbDeviceError):
        select_device(devices, requested_serial=None)