from sshtunnel import SSHTunnelForwarder


def open_ssh_tunnel(database):
    if database.ssh_method == 'password':
        tunnel = SSHTunnelForwarder(
            (database.ssh_host, database.ssh_port),
            ssh_username=database.ssh_user_name,
            ssh_password=database.ssh_password,
            remote_bind_address=(database.host, database.port),
        )
    else:
        tunnel = SSHTunnelForwarder(
            (database.ssh_host, database.ssh_port),
            ssh_username=database.ssh_user_name,
            ssh_pkey=database.ssh_private_key.path,
            remote_bind_address=(database.host, database.port),
        )
    tunnel.start()
    return tunnel
