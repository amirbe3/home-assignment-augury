import augury_api as api


def main():
    node_uuid = "MOXA_TBCDB1045003"

    node_info = api.api_get_node_by_uuid(node_uuid)
    print("Before:", node_info["version"], "host:", node_info["api_host"])

    channel = node_info["ota_channel"]
    api.api_post_version_to_ota_channel(channel, "moxa_34.swu")

    updated = api.poll_node_for_ota(node_uuid)
    print("Updated:", updated)

    node_info = api.api_get_node_by_uuid(node_uuid)
    print("After:", node_info["version"], "error:", node_info["last_error"])


if __name__ == "__main__":
    main()
