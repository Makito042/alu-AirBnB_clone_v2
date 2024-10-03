#!/usr/bin/python3
from fabric import Connection
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz file from the contents of the web_static folder.

    Returns:
        str: The file path of the generated .tgz file if successful, else None.
    """
    
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date_time)
    
    try:
        os.makedirs("versions", exist_ok=True)  # Create versions directory if it doesn't exist
        # Use Connection to execute local commands
        conn = Connection("localhost")  # Using local machine for packing
        
        conn.run("tar -zcvf {} web_static".format(file_name))
        return file_name
    except Exception as err:
        print(f"Error occurred: {err}")
        return None
