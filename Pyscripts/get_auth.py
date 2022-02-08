import os
import re
import subprocess
from df_logging import logmsg


def get_password(
    api_username,
    system_name,
    account_name,
    identity_file=None,
    reason_code=None,
    reason_text=None,
    ticket_system_name=None,
    ticket_number=None):
    '''
    Retrieves a user and password from system.
    :param api_username:        The password systems CLI API username
    :param system_name:         System name account is in
    :param account_name:        The account name to retrieve the password for
    :param identity_file:       The identity file file SSH uses to authenticate with the password server
    :param reason_code:         The code stored in password server for the retrieval
    :param reason_text:         Text of the reason why the password is being retrieved
    :param ticket_system_name:  Name of ticket system to validate (Example: Health Check)
    :param ticket_number:       Ticket number to validate
    '''

    if identity_file:
        ssh_identity_file = identity_file
        if not os.path.isfile(ssh_identity_file):
            logmsg("ERROR: {}: No such file".format(ssh_identity_file))
            return None
    else:
        if "HOME" in os.environ:
            ssh_identity_file = os.environ["HOME"]
        else:
            ssh_identity_file = "."
            ssh_identity_file += "/.ssh/pass_srv"
        if not os.path.isfile(ssh_identity_file):
            logmsg("ERROR: {}: No such file".format(ssh_identity_file))
            logmsg("ERROR: Create a symbolic link named {} that points to your password server identity")
            return None

    unix_command = [
        "ssh", "-i", ssh_identity_file, api_username + "@server.company.com", "retrieve",
        "--SystemName", system_name,
        "--AccountName", account_name,
        "--TimeRequired", "1"
    ]

    if reason_code:
        unix_command.append("--ReasonCode")
        unix_command.append(reason_code)
    if reason_text:
        unix_command.append("--ReasonText")
        unix_command.append(reason_text)
    if ticket_system_name:
        unix_command.append("--TicketSystemName")
        unix_command.append(ticket_system_name)
    if ticket_number:
        unix_command.append("--TicketNumber")
        unix_command.append(ticket_number)

    returnCode = subprocess.run(
        unix_command,
        universal_newlines=True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    if returnCode and returnCode.stderr.strip():
        logmsg("ERROR: Password Server: {}".format(returnCode.stderr.strip()))
        return None

    if returnCode != 0:
        logmsg("ERROR: {}".format(unix_command))
        logmsg("ERROR: Failed to retrieve credentials from password server")
        return None

    '''
    Password server will sometimes write an error to STDERR and return result code of 0.
    Checking for other potential errors just in case.
    '''
    if not returnCode.stdout or not returnCode.stdout.strip():
        logmsg("ERROR: Blank password retrieved from password server")
        return None

    if returnCode.stdout.strip() == "default initial password":
        logmsg("ERROR: Password has not been initialized")
        return None

    '''
    Passwords should not have blank. If this search for a space is true,
    we may receive a result code of 0 but have an error message as well.
    '''
    if re.search(' ', returnCode.stdout):
        logmsg("ERROR: Password stdout: {}".format(returnCode.stdout))
        return None

    return returnCode.stdout.rstrip()