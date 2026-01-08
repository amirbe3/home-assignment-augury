from models import Node, Endpoint

# In-memory "database"
_NODES = {}         # uuid -> Node
_ENDPOINTS = {}     # serial -> Endpoint

# OTA channel storage: { "OTA_<uuid>": ["moxa_34.swu", ...] }
_OTA_CHANNELS = {}

# DFU channel storage: { "DFU_<serial>": ["ep1_11.swu", ...] }
_DFU_CHANNELS = {}


def init_default_data() -> None:
    """
    Create 3 nodes and 3 endpoints per node (EP1, EP2, CANARY).
    Node versions start at 33 (for OTA test).
    """
    _NODES.clear()
    _ENDPOINTS.clear()
    _OTA_CHANNELS.clear()
    _DFU_CHANNELS.clear()

    def add_node(name: str, uuid: str, version: int) -> Node:
        node = Node(name=name, uuid=uuid, version=version)
        _NODES[uuid] = node
        return node

    def add_endpoint(
        node: Node,
        serial: str,
        hw: str,
        version: int,
        battery: int,
        backlog: int,
    ) -> Endpoint:
        ep = Endpoint(
            serial_number=serial,
            hardware_type=hw,
            version=version,
            battery=battery,
            backlog=backlog,
            node_uuid=node.uuid,
        )
        node.add_endpoint(ep)
        _ENDPOINTS[serial] = ep
        return ep

    n1 = add_node("AHN2", "AHN2_TBCDB1045001", 33)
    n2 = add_node("CASSIA", "CASSIA_TBCDB1045002", 33)
    n3 = add_node("MOXA", "MOXA_TBCDB1045003", 33)

    for n in (n1, n2, n3):
        add_endpoint(n, f"{n.name}-EP1-0001", "EP1", 10, 3000, 0)
        add_endpoint(n, f"{n.name}-EP2-0001", "EP2", 10, 3000, 0)
        add_endpoint(n, f"{n.name}-CANARY-0001", "CANARY", 5, 4000, 0)


# ---------- API functions (as requested in the assignment) ----------

def api_get_endpoint_by_serial(serial_number: str) -> dict:
    ep = _ENDPOINTS[serial_number]
    return {
        "serial_number": ep.serial_number,
        "battery": str(ep.battery),
        "hardware_type": ep.hardware_type,
        "uuid": ep.node_uuid,           # required by assignment
        "version": str(ep.version),
        # extra useful fields (not harmful):
        "backlog": str(ep.backlog),
        "last_error": ep.last_error,
    }


def api_get_node_by_uuid(uuid: str) -> dict:
    node = _NODES[uuid]
    return {
        "uuid": node.uuid,
        "ota_channel": f"OTA_{node.uuid}",
        "version": str(node.version),
        # extra info from spec (host per node type)
        "api_host": node.api_host(),
        # include error so Robot can assert "report an error"
        "last_error": node.last_error,
        "Endpoints": [
            {
                "serial_number": ep.serial_number,
                "hardware_type": ep.hardware_type,
                "version": str(ep.version),
                "battery": str(ep.battery),
                "backlog": str(ep.backlog),
            }
            for ep in node.endpoints
        ],
    }


def api_post_version_to_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Always accept and store; validation happens on poll/apply
    _OTA_CHANNELS.setdefault(ota_channel, []).append(version_artifact)
    return 200


def api_clear_ota_channel(ota_channel: str, version_artifact: str) -> int:
    if ota_channel not in _OTA_CHANNELS:
        return 400
    if version_artifact not in _OTA_CHANNELS[ota_channel]:
        return 400
    _OTA_CHANNELS[ota_channel].remove(version_artifact)
    return 200


# ---------- Helpers for tests (Robot will love these) ----------

def poll_node_for_ota(uuid: str) -> bool:
    node = _NODES[uuid]
    ota_channel = f"OTA_{node.uuid}"
    artifacts = _OTA_CHANNELS.get(ota_channel, [])

    if not artifacts:
        node.last_error = "NO_ARTIFACT"
        return False

    latest_artifact = artifacts[-1]
    ok = node.apply_ota_update(latest_artifact)
    return ok


def api_post_version_to_dfu_channel(dfu_channel: str, version_artifact: str) -> int:
    _DFU_CHANNELS.setdefault(dfu_channel, []).append(version_artifact)
    return 200


def poll_endpoint_for_dfu(serial_number: str) -> bool:
    ep = _ENDPOINTS[serial_number]
    dfu_channel = f"DFU_{ep.serial_number}"
    artifacts = _DFU_CHANNELS.get(dfu_channel, [])

    if not artifacts:
        ep.last_error = "NO_ARTIFACT"
        return False

    latest_artifact = artifacts[-1]
    ok = ep.apply_dfu_update(latest_artifact)
    return ok


def set_endpoint_backlog(serial_number: str, backlog: int) -> None:
    _ENDPOINTS[serial_number].backlog = backlog


def set_endpoint_battery(serial_number: str, battery: int) -> None:
    _ENDPOINTS[serial_number].battery = battery


# Initialize default data on import
init_default_data()
