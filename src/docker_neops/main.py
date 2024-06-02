import argparse
from dataclasses import dataclass
from typing import List, Optional

import docker
from termcolor import colored


@dataclass
class Container:
    ID: str
    Image: str
    Command: str
    CreatedAt: str
    Status: str
    Ports: Optional[str]
    Names: str
    Networks: Optional[str]


def get_docker_client():
    try:
        client = docker.from_env()
        return client
    except Exception as e:
        print(f"Error creating Docker client: {str(e)}")
        return None


def get_containers(client) -> List[Container]:
    containers = []
    try:
        container_list = client.containers.list(all=True)
        for container in container_list:
            container_info = container.attrs
            ports = container_info["NetworkSettings"]["Ports"]
            port_str = ", ".join(
                [
                    f"{k.split('/')[0]}->{v[0]['HostPort']}"
                    if v
                    else k.split("/")[0]
                    for k, v in ports.items()
                    if v
                ]
            )
            container_obj = Container(
                ID=container_info["Id"][:12],
                Image=container_info["Config"]["Image"],
                Command=" ".join(container_info["Config"]["Cmd"])
                if container_info["Config"]["Cmd"]
                else "N/A",
                CreatedAt=container_info["Created"],
                Status=container_info["State"]["Status"],
                Ports=port_str,
                Names=container_info["Name"],
                Networks=", ".join(
                    container_info["NetworkSettings"]["Networks"].keys()
                ),
            )
            containers.append(container_obj)
    except Exception as e:
        print(f"Error retrieving containers: {str(e)}")
    return containers


def process_ports(port_string: Optional[str]) -> str:
    if not port_string:
        return colored("No Ports", "green")

    ports = port_string.split(", ")
    processed_ports = []
    for port in ports:
        if "->" in port:
            host_port = port.split("->")[1]
            processed_ports.append(colored(host_port, "red"))
        else:
            container_port = port.split("/")[0]
            processed_ports.append(colored(container_port, "green"))

    return ", ".join(processed_ports)


def display_containers(containers: List[Container], compact: bool) -> None:
    total_containers = len(containers)
    for index, container in enumerate(containers):
        container_id = colored(container.ID, "cyan")
        image = colored(container.Image, "green")
        command = colored(container.Command, "yellow")
        created = colored(container.CreatedAt, "magenta")
        status = colored(
            container.Status,
            "red" if "exited" in container.Status.lower() else "green",
        )
        ports = process_ports(container.Ports)
        names = colored(container.Names, "blue")
        network = colored(container.Networks or "No Network", "yellow")

        if compact:
            ports_list = [port.split(" ")[-1] for port in ports.split(", ")]
            ports_str = ",".join(ports_list)
            line = f"{names}-{container_id}-{network}-[{ports_str}]"
            print(line)
        else:
            print(f"Container {index + 1}/{total_containers}")
            print(f"ID: {container_id}")
            print(f"Image: {image}")
            print(f"Command: {command}")
            print(f"Created: {created}")
            print(f"Status: {status}")
            print(f"Ports: {ports}")
            print(f"Names: {names}")
            print(f"Network: {network}")
            print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Docker Container Info Display"
    )
    parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        help="Enable super compact mode",
    )
    args = parser.parse_args()

    client = get_docker_client()
    if client:
        containers = get_containers(client)
        display_containers(containers, args.compact)
    else:
        print("Failed to create Docker client.")


if __name__ == "__main__":
    main()
