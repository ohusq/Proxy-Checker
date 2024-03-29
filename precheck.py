import os

def check_permissions(file_path) -> bool:
    status = True
    if os.access(file_path, os.R_OK):
        pass
    else:
        print(f"Read permission is not granted for {file_path}")
        status = False

    if os.access(file_path, os.W_OK):
        pass
    else:
        print(f"Write permission is not granted for {file_path}")
        status = False
    
    return status

# Example usage
# check_permissions("working.txt")
# check_permissions("google_blocked_proxies.txt")
# check_permissions("ascii.txt")