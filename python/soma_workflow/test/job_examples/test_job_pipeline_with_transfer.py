# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:07:28 2013

@author: laure.hugo@cea.fr
"""
import os
import sys

import soma_workflow.constants as constants
from soma_workflow.test.utils import check_files
from soma_workflow.test.job_examples.jobs_test import JobsTest


class JobPipelineWithTransfer(JobsTest):
    '''
    Submission of a job pipeline with transfer
    '''
    def setUp(self):
        self.my_jobs = []
        self.my_transfers = []
        self.client_files = []
        self.output_files = []

        # Job1
        info1 = JobsTest.job_examples.submit_job1()
        self.my_jobs.append(info1[0])
        self.output_files.extend(info1[1])

        JobsTest.wf_ctrl.wait_job(self.my_jobs)
        status = JobsTest.wf_ctrl.job_status(self.my_jobs[0])
        self.failUnless(status == constants.DONE,
                        'Job %s status after wait: %s' %
                        (self.my_jobs[0], status))
        job_termination_status = JobsTest.wf_ctrl.job_termination_status(
            self.my_jobs[0])
        exit_status = job_termination_status[0]
        self.failUnless(exit_status == constants.FINISHED_REGULARLY,
                        'Job %s exit status: %s' %
                        (self.my_jobs[0], exit_status))
        exit_value = job_termination_status[1]
        self.failUnless(exit_value == 0,
                        'Job exit value: %d' % exit_value)

        # Job2 & 3
        info2 = JobsTest.job_examples.submit_job2()
        self.my_jobs.append(info2[0])
        self.output_files.extend(info2[1])

        info3 = JobsTest.job_examples.submit_job3()
        self.my_jobs.append(info3[0])
        self.output_files.extend(info3[1])

        JobsTest.wf_ctrl.wait_job(self.my_jobs)
        status = JobsTest.wf_ctrl.job_status(self.my_jobs[1])
        self.failUnless(status == constants.DONE,
                        'Job %s status after wait: %s' %
                        (self.my_jobs[1], status))
        job_termination_status = JobsTest.wf_ctrl.job_termination_status(
            self.my_jobs[1])
        exit_status = job_termination_status[0]
        self.failUnless(exit_status == constants.FINISHED_REGULARLY,
                        'Job %s exit status: %s' %
                        (self.my_jobs[1], exit_status))
        exit_value = job_termination_status[1]
        self.failUnless(exit_value == 0,
                        'Job exit value: %d' % exit_value)

        status = JobsTest.wf_ctrl.job_status(self.my_jobs[2])
        self.failUnless(status == constants.DONE,
                        'Job %s status after wait: %s' %
                        (self.my_jobs[2], status))
        job_termination_status = JobsTest.wf_ctrl.job_termination_status(
            self.my_jobs[2])
        exit_status = job_termination_status[0]
        self.failUnless(exit_status == constants.FINISHED_REGULARLY,
                        'Job %s exit status: %s' %
                        (self.my_jobs[2], exit_status))
        exit_value = job_termination_status[1]
        self.failUnless(exit_value == 0,
                        'Job exit value: %d' % exit_value)

        # Job 4
        info4 = JobsTest.job_examples.submit_job4()
        self.my_jobs.append(info4[0])
        self.output_files.extend(info4[1])

    def tearDown(self):
        JobsTest.tearDown(self)
        for file in self.client_files:
            if os.path.isfile(file):
                os.remove(file)

    def test_result(self):
        jobid = self.my_jobs[len(self.my_jobs) - 1]
        JobsTest.wf_ctrl.wait_job(self.my_jobs)
        status = JobsTest.wf_ctrl.job_status(jobid)
        self.failUnless(status == constants.DONE,
                        'Job %s status after wait: %s' % (jobid, status))
        job_termination_status = JobsTest.wf_ctrl.job_termination_status(jobid)
        exit_status = job_termination_status[0]
        self.failUnless(exit_status == constants.FINISHED_REGULARLY,
                        'Job %s exit status: %s' % (jobid, exit_status))
        exit_value = job_termination_status[1]
        self.failUnless(exit_value == 0,
                        'Job exit value: %d' % exit_value)

        # checking output files
        for file in self.output_files:
            client_file = JobsTest.wf_ctrl.transfers([file])[file][0]
            self.failUnless(client_file)
            JobsTest.wf_ctrl.transfer_files(file)
            self.failUnless(os.path.isfile(client_file),
                            'File %s doesn t exit' % file)
            self.client_files.append(client_file)

        models = (JobsTest.job_examples.job1_output_file_models +
                  JobsTest.job_examples.job2_output_file_models +
                  JobsTest.job_examples.job3_output_file_models +
                  JobsTest.job_examples.job4_output_file_models)
        (correct, msg) = check_files(self.client_files, models)
        self.failUnless(correct, msg)

        # checking stdout and stderr
        for i in range(0, 4):
            client_stdout = os.path.join(JobsTest.job_examples.output_dir,
                                         "stdout_pipeline_job" + str(i+1))
            client_stderr = os.path.join(JobsTest.job_examples.output_dir,
                                         "stderr_pipeline_job" + str(i+1))
            JobsTest.wf_ctrl.retrieve_job_stdouterr(self.my_jobs[i],
                                                    client_stdout,
                                                    client_stderr)
            self.client_files.append(client_stdout)
            self.client_files.append(client_stderr)

#        client_stdout = os.path.join(JobsTest.job_examples.output_dir,
#                                     "stdout_pipeline_job2")
#        client_stderr = os.path.join(JobsTest.job_examples.output_dir,
#                                     "stderr_pipeline_job2")
#        JobsTest.wf_ctrl.retrieve_job_stdouterr(self.my_jobs[1],
#                                                client_stdout,
#                                                client_stderr)
#        self.client_files.append(client_stdout)
#        self.client_files.append(client_stderr)
#
#        client_stdout = os.path.join(JobsTest.job_examples.output_dir,
#                                     "stdout_pipeline_job3")
#        client_stderr = os.path.join(JobsTest.job_examples.output_dir,
#                                     "stderr_pipeline_job3")
#        JobsTest.wf_ctrl.retrieve_job_stdouterr(self.my_jobs[2],
#                                                client_stdout,
#                                                client_stderr)
#        self.client_files.append(client_stdout)
#        self.client_files.append(client_stderr)
#
#        client_stdout = os.path.join(JobsTest.job_examples.output_dir,
#                                     "stdout_pipeline_job4")
#        client_stderr = os.path.join(JobsTest.job_examples.output_dir,
#                                     "stderr_pipeline_job4")
#        JobsTest.wf_ctrl.retrieve_job_stdouterr(self.my_jobs[3],
#                                                client_stdout,
#                                                client_stderr)
#        self.client_files.append(client_stdout)
#        self.client_files.append(client_stderr)

        models = (JobsTest.job_examples.job1_stdouterr_models +
                  JobsTest.job_examples.job2_stdouterr_models +
                  JobsTest.job_examples.job3_stdouterr_models +
                  JobsTest.job_examples.job4_stdouterr_models)
        (correct, msg) = check_files(self.client_files[5:13], models)
        self.failUnless(correct, msg)


if __name__ == '__main__':
    JobPipelineWithTransfer.run_test(debug=True)
    sys.exit(0)
