import pysftp

myHostname = "fierro.ing.puc.cl"
myUsername = "grupo6_dev"
myPassword = "hhqC9wWbKyIMjPX"


def printear():
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection succesfully stablished ... ")

        # Switch to a remote directory
        sftp.cwd('/pedidos')

        # Obtain structure of the remote directory '/var/www/vhosts'
        directory_structure = sftp.listdir_attr()

        # Print data
        for attr in directory_structure:
            print(attr.filename, attr)
