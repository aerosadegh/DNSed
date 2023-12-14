import subprocess


def run_command(command, capture_output=False):
    """
    Runs a command using subprocess.

    Args:
        command (str): The command to run.
    """
    return subprocess.run(
        command,
        shell=True,
        check=True,
        capture_output=capture_output,
    )


def change_dns(network_interface, primary_dns, secondary_dns=None):
    """
    Changes the DNS settings of a network interface.

    Args:
        network_interface (str): The name of the network interface to change.
        primary_dns (str): The primary DNS server to set.
        secondary_dns (str, optional): The secondary DNS server to set. Defaults to None.
    """
    command = f'netsh interface ip set dns "{network_interface}" static {primary_dns}'
    if secondary_dns:
        command += f' primary && netsh interface ip add dns "{network_interface}" {secondary_dns} index=2'
    run_command(command)


def clear_dns(network_interface):
    """
    Clears the DNS settings of a network interface, setting them back to automatic.

    Args:
        network_interface (str): The name of the network interface to clear.
    """
    command = f'netsh interface ip set dns "{network_interface}" dhcp'
    run_command(command)


def parse_interfaces(output):
    """
    Parses the output of 'netsh interface ipv4 show interfaces' and returns a list of active, external interface names.

    Args:
        output (str): The output from 'netsh interface ipv4 show interfaces'.

    Returns:
        list: A list of active, external network interface names.
    """
    lines = output.split("\n")
    interfaces = []
    for line in lines[4:-1]:  # Skip the header lines and the last empty line
        parts = line.split()
        if len(parts) >= 5:  # Ensure the line has enough parts
            state = parts[-2]
            name = parts[-1]
            if (
                state == "connected"
                and not name.startswith("Loopback")
                and not name.startswith("vEthernet")
            ):
                interfaces.append(name)
    return interfaces


def get_network_interfaces():
    """
    Retrieves a list of network interfaces.

    Returns:
        str: The stdout from the 'netsh interface ipv4 show interfaces' command.
    """
    command = "netsh interface ipv4 show interfaces"
    result = run_command(
        command,
        capture_output=True,
    )
    return parse_interfaces(result.stdout.decode("utf-8"))


def get_dns(network_interface):
    command = f'netsh interface ip show config name="{network_interface}"'
    result = run_command(command, capture_output=True)
    lines = result.stdout.decode("utf-8").split("\n")
    for line in lines:
        if "Statically Configured DNS Servers" in line:
            return line.split(": ")[-1].strip()
    return "Empty DNS"
