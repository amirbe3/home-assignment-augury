# Basic data models for the simulated IoT system.

class Endpoint:
    """
    Represents a sensor endpoint and its current state.
    """

    def __init__(
        self,
        serial_number: str,
        hardware_type: str,
        version: int,
        battery: int,
        backlog: int,
        node_uuid: str,
    ):
        self.serial_number = serial_number
        self.hardware_type = hardware_type  # EP1 / EP2 / CANARY
        self.version = version
        self.battery = battery
        self.backlog = backlog
        self.node_uuid = node_uuid

        self.last_error = None  # str | None

    def battery_threshold(self) -> int:
        # Thresholds from the assignment rules:
        # EP1/EP2: 2500, CANARY: 3600
        if self.hardware_type.upper() == "CANARY":
            return 3600
        return 2500

    def apply_dfu_update(self, artifact: str) -> bool:
        """
        Apply a DFU update using an artifact name (example: ep1_11.swu).

        Returns True if the endpoint version was updated.
        """
        self.last_error = None

        if not artifact:
            self.last_error = "EMPTY_ARTIFACT"
            return False

        if self.backlog > 0:
            self.last_error = "BACKLOG_NOT_EMPTY"
            return False

        if self.battery < self.battery_threshold():
            self.last_error = "LOW_BATTERY"
            return False

        expected_prefix = self.hardware_type.lower() + "_"
        if not artifact.lower().startswith(expected_prefix):
            self.last_error = "BAD_FIRMWARE"
            return False

        try:
            # ep1_11.swu -> "11"
            version_part = artifact.split("_", 1)[1]
            version_str = version_part.split(".", 1)[0]
            new_version = int(version_str)
        except Exception:
            self.last_error = "BAD_ARTIFACT_FORMAT"
            return False

        if new_version <= self.version:
            self.last_error = "VERSION_NOT_NEWER"
            return False

        self.version = new_version
        return True


class Node:
    """
    Represents a gateway (node) that manages multiple endpoints.
    """

    def __init__(self, name: str, uuid: str, version: int):
        self.name = name  # AHN2 / CASSIA / MOXA
        self.uuid = uuid
        self.version = version
        self.endpoints = []

        self.last_error = None  # str | None

    def add_endpoint(self, endpoint: Endpoint) -> None:
        self.endpoints.append(endpoint)

    def api_host(self) -> str:
        # AHN2 & CASSIA -> buildroot_api.azure, MOXA -> moxa_api.azure
        if self.name.upper() == "MOXA":
            return "moxa_api.azure"
        return "buildroot_api.azure"

    def apply_ota_update(self, artifact: str) -> bool:
        """
        Apply an OTA update using an artifact name (example: moxa_34.swu).

        Returns True if the node version was updated.
        """
        self.last_error = None

        if not artifact:
            self.last_error = "EMPTY_ARTIFACT"
            return False

        expected_prefix = self.name.lower() + "_"
        if not artifact.lower().startswith(expected_prefix):
            self.last_error = "BAD_FIRMWARE"
            return False

        try:
            version_part = artifact.split("_", 1)[1]
            version_str = version_part.split(".", 1)[0]
            new_version = int(version_str)
        except Exception:
            self.last_error = "BAD_ARTIFACT_FORMAT"
            return False

        if new_version <= self.version:
            self.last_error = "VERSION_NOT_NEWER"
            return False

        self.version = new_version
        return True
