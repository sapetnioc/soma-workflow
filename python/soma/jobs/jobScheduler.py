'''
The L{JobScheduler} allows to submit jobs to predefined sets of machines
linked together via a distributed resource management systems (DRMS) like 
Condor, SGE, LSF, etc. It requires a instance of L{JobServer} to be available.

@author: Yann Cointepas
@author: Soizic Laguitton
@organization: U{IFR 49<http://www.ifr49.org>}
@license: U{CeCILL version 2<http://www.cecill.info/licences/Licence_CeCILL_V2-en.html>}
'''
__docformat__ = "epytext en"

class JobScheduler( object ):
  '''
  Instances of this class give access to a set of machines linked together
  via a distributed resource management system (DRMS) like Condor, SGE, LSF,
  etc. A L{JobScheduler} allows to submit, monitor, control, and manage $
  information related to submitted jobs: id, author and associated files 
  (stdin, stdout, stderr, input and output files) for example.
  The use of L{JobScheduler} requires a L{JobServer} to be available.
  Job submissions and file transfers are registered on the server l{JobServer}. 
  Job information and temporary files are automatically disposed after a 
  timeout which is set a priori by the user. The user can also dispose the jobs 
  himself calling the L{dispose} or L{cancelTransfer} methods. 
 
  In case of the implementation of L{JobScheduler} using the DRMAA API: 
  JobScheduler must be created on one of the machines which is allowed to 
  submit jobs by the DRMS.
  '''
  def __init__( self ):
   '''
   Opens a connection to the pool of machines and to the data server L{JobServer}.
   In case of the implementation using the DRMAA API: A L{JobScheduler} instance 
   can only be created from a machine that is allowed to submit jobs by the 
   underlying DRMS.
   '''

  def __del__( self ):
     '''
     Closes the connection with the pool and the data server L{JobServer}. 
     It doesn't have any impact on the submitted jobs or file transfer. 
     Job and transfer information remains stored on the data server.
     '''
  

  ########## FILE TRANSFER ###############################################
  
  '''
  The main purpose of file transfer is the submission of job from a remote 
  machine. However it can also be used by user who has access to directory 
  shared by the machine of the pool, to make sure that all the machine of 
  the pool will have access to his files and take advantage of the file life 
  management services.
  
  For the following methods:
    Local means that it is located on a directory shared by the machine of the pool
    Remote means that it is located on a remote machine or on any directory 
    owned by the user. 
    A transfer will associate remote file path to unique local file path.
  '''

  
  def transferInputFile(self, remote_input_file, disposal_timeout=168):
    '''
    For each remote input file, an unique local path is generated 
    and associated with the remote path. 
    Each remote files is copied to its associated local location.
    When the disposal timout will be past, and no exisiting job will 
    declare using the file as input, the files will be disposed. 
    
    @type  remote_input_file: string or sequence of string
    @param remote_input_file: remote path(s) of input file(s)
    @type  disposalTimeout: int
    @param disposalTimeout: Number of hours before each local file is considered 
    to have been forgotten by the user. Passed that delay, and if no existing job 
    declares using the file as input, the local file and information 
    related to the transfer are disposed. 
    Default delay is 168 hours (7 days).
    @rtype: string or sequence of string
    @return: local file path(s) where the file(s) were copied 
    '''

  def allocateLocalOutputFile(self, remote_output_file_path, disposal_timeout=168):
    '''
    For each remote output file path, an unique local path is generated and 
    associated with the remote path. 
    When the disposal timout will be past, and no exisiting job will declare using 
    the file as output or input, the files will be disposed. 
    Once created and filled by a job, the local file can be transfered to the
    remote machine via the L{transferOutputFile} method
    
    @type  remote_output_file_paths: string of sequence of string
    @param remote_output_file_paths: remote path for output file.
    @type  disposalTimeout: int
    @param disposalTimeout: Number of hours before each local file is considered 
    to have been forgotten by the user. Passed that delay, and if no existing job 
    declares using the file as output or input, the local file and information 
    related to the transfer are disposed. 
    Default delay is 168 hours (7 days).
    @rtype: string or sequence of string
    @return: local file path(s) associated to specified the remote file path(s).
    
    '''

  def transferOutputFile(self, local_file);
    '''
    Copy the local file to the associated remote file path. 
    The local file path must belong to the user's transfered files (ie belong to 
    the sequence returned by the L{getTransfers} method). 
    
    @type  local_file: string or sequence of string
    @param local_file: local file path(s) 
    '''

  def cancelTransfer(self, local_file_path):
    '''
    Delete each specified local file unless a job has declared to use it as input 
    or output. In the former case, the file will only be deleted after all its 
    associated jobs are disposed. (set its disposal date to now).
    
    @type local_file_path: string or sequence of string
    @param local_file_path: local file path(s) associated with a transfer (ie 
    belong(s) to the list returned by L{getTransfers}    
    '''

  ########## JOB SUBMISSION ##################################################

  '''
  L{submit}, L{customSubmit} and L{submitWithTransfer} methods submit a 
  job for execution to the DRMS. A job identifier is returned. 
  This private structure must be used to inspect and control the job via 
  L{JobScheduler} methods.
  
  Example::
    from soma.jobs import jobScheduler
      
    jobScheduler = JobScheduler()
    job_id = jobScheduler.submit( ( 'python', '/somewhere/something.py' ), stdout=True, stderr='stdout' )
    jobScheduler.wait( job_id )
    file = jobScheduler.jobStdout( job_id )
    jobScheduler.dispose( job_id )
    for line in file:
      print line,
  '''

  def customSubmit( self,
              command,
              workingDirectory,
              stdoutPath,
              stderrPath,
              jointStdErrOut=False,
              stdin=None,
              disposalTimeout=168):
    '''
    Customized submission. All the files involved belong to the user and must 
    be specified. They are never disposed automatically and are not deleted when 
    using the L{kill} or L{dispose} methods.
    All the path must refer to shared files or directory on the pool.
    
    @type  command: sequence
    @param command: The command to execute
    @type  workingDirectory: string
    @param workingDirectory: path to a directory where the job will be executed.
    @type  stdout: string
    @param stdout: the job's standard output will be directed to this file. 
    @type  stderr: string 
    @param stderr: the job's standard error will be directed to this file. 
    @type  stdin: string
    @param stdin: job's standard input as a path to a file. C{None} if the 
    job doesn't require an input stream.
    @type  disposalTimeout: int
    @param disposalTimeout: Number of hours before the job is considered to have been 
      forgotten by the submitter. Passed that delay, the job is destroyed and its
      resources released as if the submitter had called L{kill} and L{dispose}.
      Default delay is 168 hours (7 days).
    @rtype:   C{JobIdentifier}
    @return:  the identifier of the submitted job 
    '''

  def submit( self,
              command,
              workingDirectory=None,
              stdout=False, 
              stderr=False, 
              stdin=None,
              disposalTimeout=168):
    '''
    Regular submission. If stdout and stderr are set to C{True}, the standard output 
    and error files are created on a directory shared by the machine of the pool. 
    These files will be deleted when the job will be disposed (after the disposal 
    timeout or when calling the L{kill} and L{dispose} methods).  
    All the path must refer to shared files or directory on the pool.
    
    @type  command: sequence
    @param command: The command to execute
    @type  workingDirectory: string
    @param workingDirectory: path to a directory where the job will be executed.
    If C{None}, a default working directory will be used (its value depends on 
    the DRMS installed on the pool).
    @type  stdout: bool
    @param stdout: C{True} if the job's standard output stream must be recorded.
    @type  stderr: bool or string
    @param stderr: C{True} if the job's standard output stream must be recorded. 
      The error output stream will be stored in the same file as the standard 
      output stream.
    @type  stdin: string
    @param stdin: job's standard inpout as a path to a file. C{None} if the 
    job doesn't require an input stream.
    @type  disposalTimeout: int
    @param disposalTimeout: Number of hours before the job is considered to have been 
      forgotten by the submitter. Passed that delay, the job is destroyed and its
      resources released (including standard output and error files) as if the 
      user had called L{kill} and L{dispose}.
      Default delay is 168 hours (7 days).
    @rtype:   C{JobIdentifier} 
    @return:  the identifier of the submitted job
    '''

  def submitWithTransfer( self,
                          command,
                          required_local_input_files,
                          required_local_output_file,
                          stdout=False, 
              	          stderr=False, 
	  		  stdin=None,
                          disposalTimeout=168):
    '''
    Submission with file transfer (well suited for remote submission). Submission 
    of a job for which all input files (stdin and input files) were already copied 
    to the pool shared directory using the L{transferInputFile} method. A local path
    for output file were also obtained via the L{allocateLocalOutputFile} method.
    Once the job will have run, it will be possible to transfer the files back to the
    remote machine using the L{transferOutputFile} method.
    The list of involved local input and output file must be specified here to 
    guarantee that the files will exist during the whole job life. 
    All the path must refer to shared files or directory on the pool.
    
    @type  command: sequence
    @param command: The command to execute
    @type  required_local_input_file: sequence of string
    @param required_local_input_file: local files which are required for the job to run 
    @type  required_local_output_file: sequence of string
    @param required_local_output_file: local files the job will created and filled
    @type  stdout: bool
    @param stdout: C{True} if the job's standard output stream must be recorded.
    @type  stderr: bool or string
    @param stderr: C{True} if the job's standard output stream must be recorded. 
      The error output stream will be stored in the same file as the standard output 
      stream.
    @type  stdin: string
    @param stdin: job's standard inpout as a path to a file. C{None} if the 
    job doesn't require an input stream.
    @type  disposalTimeout: int
    @param disposalTimeout: Number of hours before the job is considered to have been 
      forgotten by the submitter. Passed that delay, the job is destroyed and its
      resources released as if the submitter had called L{kill} and L{dispose}.
      Default delay is 168 hours (7 days). 
      The local files associated with the job won't be deleted unless their own 
      disposal timeout is past and no other existing job has declared to use them 
      as input or output.
    @rtype:   C{JobIdentifier}
    @return:  the identifier of the submitted job 
    ''' 


  def dispose( self, job_id ):
    '''
    Frees all the resources allocated to the submitted job on the data server
    L{JobServer}. After this call, the C{job_id} becomes invalid and
    cannot be used anymore. 
    To avoid that jobs create non handled files, L{dispose} kills the job if 
    it's running.

    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{jobs} or the submission 
    methods L{submit}, L{customSubmit} or L{submitWithTransfer})
    '''


  ########## SERVER STATE MONITORING ########################################


  def jobs( self, all=False ):
    '''
    Returns the identifier of the submitted and not diposed jobs.

    @type  all: bool
    @param all: If C{all=False} (the default), only the jobs submitted by the
      current user are returned. If C{all=True} all jobs are returned.
    @rtype:  sequence of C{JobIdentifier}
    @return: series of job identifiers
    '''

 def getJobsBindToLocalFile(self, local_file_path):
    '''
    Returns a sequence of the the jobs which have declare to user the local file
    as input or output.  
    The local file path must belong to the user's transfered files (ie belong to 
    the sequence returned by the L{getTransfers} method).
    
    @type local_file_path: string
    @param local_file_path: local file path 
    @rtype: sequence of tuple (C{JobIdentifier}, isInput)
    @return: sequence of jobs using the local file associated to C{True} 
    if the job uses it as input or C{False} if it uses it as output.
    '''
    
    
  def getTransfers( self ):
    '''
    Returns the information related to the user's file transfers created via the 
    L{transferInputFile} and L{allocateFilesForTransfer} methods

    @rtype: sequence of tuple (local_file_path, remote_file_path, expiration_date)
    @return: For each transfer
        -local_file_path: path of the file on the directory shared by the machines
        of the pool
	-remote_file_path: path of the file on the remote machine 
	-expiration_date: after this date the local file will be deleted, unless an
	existing job has declared this file as output or input.
    '''


  
  ########### DRMS MONITORING ################################################

  def status( self, job_id ):
    '''
    Returns the status of a submitted job.
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    @rtype:  C{JobStatus}
    @return: the status of the job.
    '''

  def returnValue( self, job_id ):
    '''
    Gives the value returned by the job if it has finished normally. In case
    of a job running a C program, this value is typically the one given to the
    C{exit()} system call.
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    @rtype:  int or None
    @return: job exit value, it may be C{None} if the job is not finished or
    exited abnormally (for instance on a signal).
    '''

  def output( self, job_id ):
    '''
    Opens a file containing what had been written on the job standard 
    output stream. It may return C{None} if the process is not terminated
    or if recording of standard output had not been requested by the 
    submission methods (L{customSubmit}, L{submit} or L{submitWithTransfer}).
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    @rtype:  file object or None
    @return: file object containing the job's output.
    '''

  def errorOutput( self, job_id ):
    '''
    Opens a file containing what had been written on the job error 
    output stream. It may return C{None} if the process is not terminated,
    if recording of standard output had not been requested by L{submit} or
    L{submitWithTransfer}, or if the user has specified his own standard 
    output files using L{customSubmit}.
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    @rtype:  file object or None
    @return: file object containing the job's error output.
    '''

  ########## JOB CONTROL VIA DRMS ########################################
  
  
  def wait( self, job_ids ):
    '''
    Waits for all the specified jobs to finish execution or fail. 
    
    @type job_ids: set of C{JobIdentifier}
    @param job_ids: Set of jobs to wait for
    '''

  def stop( self, job_id ):
    '''
    Temporarily stops the job until the method L{restart} is called. The job 
    is held if it was waiting in a queue and suspended if was running. 
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    '''
  
  def restart( self, job_id ):
    '''
    Restarts a job previously stopped by the L{stop} method.
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    '''

  def kill( self, job_id ):
    '''
    Definitely terminates a job execution. After a L{kill}, a job is still in
    the list returned by L{jobs} and it can still be inspected by methods like
    L{status} or L{output}. To completely erase a job, it is necessary to call
    the L{dispose} method.
    
    @type  job_id: C{JobIdentifier}
    @param job_id: The job identifier (returned by L{submit} or L{jobs})
    '''

