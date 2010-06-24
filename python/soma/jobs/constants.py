'''
@author: Soizic Laguitton
@organization: U{IFR 49<http://www.ifr49.org>}
@license: U{CeCILL version 2<http://www.cecill.info/licences/Licence_CeCILL_V2-en.html>}
'''

'''
Job status:
'''
UNDETERMINED="undetermined"
QUEUED_ACTIVE="queued_active"
SYSTEM_ON_HOLD="system_on_hold"
USER_ON_HOLD="user_on_hold"
USER_SYSTEM_ON_HOLD="user_system_on_hold"
RUNNING="running"
SYSTEM_SUSPENDED="system_suspended"
USER_SUSPENDED="user_suspended"
USER_SYSTEM_SUSPENDED="user_system_suspended"
DONE="done"
FAILED="failed"
JOB_STATUS = [UNDETERMINED, 
              QUEUED_ACTIVE,
              SYSTEM_ON_HOLD,
              USER_ON_HOLD,
              USER_SYSTEM_ON_HOLD,
              RUNNING,
              SYSTEM_SUSPENDED,
              USER_SUSPENDED,
              USER_SYSTEM_SUSPENDED,
              DONE,
              FAILED]

'''
Exit job status:
'''
EXIT_UNDETERMINED="exit_status_undetermined"
EXIT_ABORTED="aborted"
FINISHED_REGULARLY="finished_regularly"
FINISHED_TERM_SIG="finished_signal"
FINISHED_UNCLEAR_CONDITIONS="finished_unclear_condition"
USER_KILLED="killed_by_user"
JOB_EXIT_STATUS= [EXIT_UNDETERMINED,
                  EXIT_ABORTED,
                  FINISHED_REGULARLY,
                  FINISHED_TERM_SIG,
                  FINISHED_UNCLEAR_CONDITIONS,
                  USER_KILLED]


'''
Soma job configuration items
CFG => Mandatory items
OCFG => Optional
'''
CFG_SUBMITTING_MACHINES = 'submitting_machines'
OCFG_DRMS = 'drms'

#Job server

CFG_DATABASE_FILE = 'database_file'
CFG_TMP_FILE_DIR_PATH = 'tmp_file_dir_path'
CFG_JOB_SERVER_NAME = 'job_server_name'
CFG_NAME_SERVER_HOST ='name_server_host'

OCFG_JOB_SERVER_LOG_FILE = 'job_server_log_file'
OCFG_JOB_SERVER_LOG_LEVEL = 'job_server_logging_level'
OCFG_JOB_SERVER_LOG_FORMAT = 'job_server_logging_format'

#User local process

CFG_SRC_LOCAL_PROCESS = 'src_local_process'

OCFG_LOCAL_PROCESSES_LOG_DIR = 'job_processes_log_dir_path'
OCFG_LOCAL_PROCESSES_LOG_LEVEL = 'job_processes_logging_level'
OCFG_LOCAL_PROCESSES_LOG_FORMAT = 'job_processes_logging_format'

# Parallel job configuration :
# DRMAA attributes used in parallel job submission (their value depends on the cluster and DRMS) 
OCFG_PARALLEL_COMMAND = "drmaa_native_specification"
OCFG_PARALLEL_JOB_CATEGORY = "drmaa_job_category"
PARALLEL_DRMAA_ATTRIBUTES = [OCFG_PARALLEL_COMMAND, OCFG_PARALLEL_JOB_CATEGORY]
# kinds of parallel jobs (items can be added by administrator)
OCFG_PARALLEL_PC_MPI="MPI"
OCFG_PARALLEL_PC_OPEN_MP="OpenMP"
PARALLEL_CONFIGURATIONS = [OCFG_PARALLEL_PC_MPI, OCFG_PARALLEL_PC_OPEN_MP]
# parallel job environment variables for the execution machine (items can be added by administrators) 
OCFG_PARALLEL_ENV_MPI_BIN = 'SOMA_JOB_MPI_BIN'
OCFG_PARALLEL_ENV_NODE_FILE = 'SOMA_JOB_NODE_FILE'
PARALLEL_JOB_ENV = [OCFG_PARALLEL_ENV_MPI_BIN, OCFG_PARALLEL_ENV_NODE_FILE]

# client section

OCFG_SECTION_CLIENT = 'CLIENT'
OCFG_CLIENT_LOG_FILE = 'client_log_file'
OCFG_CLIENT_LOG_FORMAT = 'client_log_format'
OCFG_CLIENT_LOG_LEVEL = 'client_log_level'