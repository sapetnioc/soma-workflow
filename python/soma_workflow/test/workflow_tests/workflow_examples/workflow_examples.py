from __future__ import with_statement

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:05:37 2013

@author: jinpeng.li@cea.fr
@author: laure.hugo@cea.fr
@author: Soizic Laguitton
@organization: U{IFR 49<http://www.ifr49.org>}
@license: U{CeCILL version 2<http://www.cecill.info/licences/Licence_CeCILL_V2-en.html>}
"""

import os
import inspect
from abc import abstractmethod
from soma_workflow.client import Group
from soma_workflow.client import Workflow
from soma_workflow.errors import ConfigurationError
import tempfile


class WorkflowExamples(object):

    def __init__(self):
        # Define example directories
        import soma_workflow
        module_file = soma_workflow.__file__
        if module_file.endswith('.pyc') or module_file.endswith('.pyo'):
            module_file = module_file[: -1]
        module_file = os.path.realpath(module_file)
        module_path = os.path.dirname(module_file)
        self.examples_dir = os.path.join(module_path,
                                         "..", "..", "test", "jobExamples")
        tmp = tempfile.mkstemp('', prefix='swf_test_')
        os.close(tmp[0])
        os.unlink(tmp[1])
        self.output_dir = tmp[1]
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)
        if (not os.path.isdir(self.examples_dir) or
                not os.path.isdir(self.output_dir)):
            raise ConfigurationError("%s or %s does not exist." % (
                                     self.examples_dir,
                                     self.output_dir))

    @staticmethod
    def get_workflow_example_list():
        example_names = []
        for example_func in dir(WorkflowExamples):
            prefix = "example_"
            if len(example_func) < len(prefix):
                continue
            if example_func[0: len(prefix)] == prefix:
                example_names.append(example_func)
        return example_names

    def get_workflow_example(self, example_index):
        return self.get_workflows()[example_index]

    def get_workflows(self):
        workflows = []
        example_funcs = WorkflowExamples.get_workflow_example_list()
        for example_func in example_funcs:
            get_example_func = getattr(self, example_func)
            workflow = get_example_func()
            workflows.append(workflow)
        return workflows

    @abstractmethod
    def job1(self):
        pass

    @abstractmethod
    def job2(self):
        pass

    @abstractmethod
    def job3(self):
        pass

    @abstractmethod
    def job4(self):
        pass

    @abstractmethod
    def job_test_command_1(self):
        pass

    @abstractmethod
    def job_test_dir_contents(self):
        pass

    @abstractmethod
    def job_test_multi_file_format(self):
        pass

    @abstractmethod
    def job_sleep(self, period):
        pass

    @abstractmethod
    def job1_exception(self):
        pass

    @abstractmethod
    def job3_exception(self):
        pass

    def example_special_transfer(self):
        # jobs
        test_dir_contents = self.job_test_dir_contents()
        test_multi_file_format = self.job_test_multi_file_format()
        # building the workflow
        jobs = [test_dir_contents, test_multi_file_format]
        dependencies = []
        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs, dependencies, name=function_name)
        return workflow

    def example_special_command(self):
        # jobs
        test_command_job = self.job_test_command_1()
        # building the workflow
        jobs = [test_command_job]

        dependencies = []
        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs, dependencies, name=function_name)
        return workflow

    def example_simple(self):
        # jobs
        job1 = self.job1()
        job2 = self.job2()
        job3 = self.job3()
        job4 = self.job4()
        # building the workflow
        jobs = [job1, job2, job3, job4]

        dependencies = [(job1, job2),
                        (job1, job3),
                        (job2, job4),
                        (job3, job4)]

        group_1 = Group(name='group_1', elements=[job2, job3])
        group_2 = Group(name='group_2', elements=[job1, group_1])

        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs,
                            dependencies,
                            root_group=[group_2, job4],
                            name=function_name)
        return workflow

    def example_wrong_native_spec_pbs(self):
       # jobs
        job1 = self.job1(option="-l walltime=5:00:00, pmem=16gb")
        job2 = self.job1(option="-l walltime=5:00:0")
        job3 = self.job1()
        # building the workflow
        jobs = [job1, job2, job3]

        workflow = Workflow(jobs, dependencies=[],
                            name="jobs with wrong native spec for pbs")
        return workflow

    def example_native_spec_pbs(self):
       # jobs
        job1 = self.job1(option="-l walltime=5:00:00,pmem=16gb")
        job2 = self.job1(option="-l walltime=5:00:0")
        job3 = self.job1()
        # building the workflow
        jobs = [job1, job2, job3]

        workflow = Workflow(jobs, dependencies=[],
                            name="jobs with native spec for pbs")
        return workflow

    def example_simple_exception1(self):
        # jobs
        job1 = self.job1_exception()
        job2 = self.job2()
        job3 = self.job3()
        job4 = self.job4()
        jobs = [job1, job2, job3, job4]

        dependencies = [(job1, job2),
                        (job1, job3),
                        (job2, job4),
                        (job3, job4)]

        group_1 = Group(name='group_1', elements=[job2, job3])
        group_2 = Group(name='group_2', elements=[job1, group_1])

        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs,
                            dependencies,
                            root_group=[group_2, job4],
                            name=function_name)
        return workflow

    def example_simple_exception2(self):
        # jobs
        job1 = self.job1()
        job2 = self.job2()
        job4 = self.job4()
        job3 = self.job3_exception()
        jobs = [job1, job2, job3, job4]

        dependencies = [(job1, job2),
                        (job1, job3),
                        (job2, job4),
                        (job3, job4)]

        group_1 = Group(name='group_1', elements=[job2, job3])
        group_2 = Group(name='group_2', elements=[job1, group_1])

        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs,
                            dependencies,
                            root_group=[group_2, job4],
                            name=function_name)
        return workflow

    def example_multiple(self):
        workflow1 = self.example_simple()
        workflow2 = self.example_simple_exception1()
        workflow3 = self.example_simple_exception2()

        jobs = workflow1.jobs
        jobs.extend(workflow2.jobs)
        jobs.extend(workflow3.jobs)

        dependencies = workflow1.dependencies
        dependencies.extend(workflow2.dependencies)
        dependencies.extend(workflow3.dependencies)

        group1 = Group(name="simple example", elements=workflow1.root_group)
        group2 = Group(name="simple with exception in Job1",
                       elements=workflow2.root_group)
        group3 = Group(name="simple with exception in Job3",
                       elements=workflow3.root_group)

        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs,
                            dependencies,
                            root_group=[group1, group2, group3],
                            name=function_name)
        return workflow

    def example_n_jobs(self, nb=300, time=60):
        jobs = []
        for i in range(0, nb):
            job = self.job_sleep(time)
            jobs.append(job)

        dependencies = []
        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs, dependencies, name=function_name)
        return workflow

    def example_n_jobs_with_dependencies(self, nb=500, time=60):
        dependencies = []
        jobs = []
        intermed_job1 = self.job_sleep(2)
        jobs.append(intermed_job1)
        intermed_job2 = self.job_sleep(2)
        jobs.append(intermed_job2)

        elem_group1 = []
        for i in range(0, nb):
            job = self.job_sleep(time)
            jobs.append(job)
            elem_group1.append(job)
            dependencies.append((job, intermed_job1))
        group1 = Group(name="Group 1", elements=elem_group1)

        elem_group2 = []
        for i in range(0, nb):
            job = self.job_sleep(time)
            jobs.append(job)
            elem_group2.append(job)
            dependencies.append((intermed_job1, job))
            dependencies.append((job, intermed_job2))
        group2 = Group(name="Group 2", elements=elem_group2)

        elem_group3 = []
        for i in range(0, nb):
            job = self.job_sleep(time)
            jobs.append(job)
            elem_group3.append(job)
            dependencies.append((intermed_job2, job))
        group3 = Group(name="Group 3", elements=elem_group3)

        root_group = [group1, intermed_job1, group2, intermed_job2, group3]
        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs, dependencies, root_group, name=function_name)
        return workflow

    def example_serial_jobs(self, nb=5):
        jobs = []
        dependencies = []
        previous_job = self.job_sleep(2)
        jobs.append(previous_job)
        for i in range(0, nb):
            job = self.job_sleep(2)
            jobs.append(job)
            dependencies.append((previous_job, job))
            previous_job = job

        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs, dependencies, name=function_name)
        return workflow

    def example_fake_pipelineT1(self):
        jobs = []
        dependencies = []
        root_group = []
        for i in range(0, 100):
            job1 = self.job_sleep(2)
            job1.name = "Brain extraction"
            jobs.append(job1)

            job11 = self.job_sleep(1)
            job11.name = "test 1"
            jobs.append(job11)
            job12 = self.job_sleep(1)
            job12.name = "test 2"
            jobs.append(job12)
            job13 = self.job_sleep(1)
            job13.name = "test 3"
            jobs.append(job13)

            job2 = self.job_sleep(5)
            job2.name = "Gray/white segmentation"
            jobs.append(job2)
            job3 = self.job_sleep(5)
            job3.name = "Left hemisphere sulci recognition"
            jobs.append(job3)
            job4 = self.job_sleep(5)
            job4.name = "Right hemisphere sulci recognition"
            jobs.append(job4)

            #dependencies.append((job1, job2))
            dependencies.append((job1, job11))
            dependencies.append((job11, job12))
            dependencies.append((job12, job13))
            dependencies.append((job13, job2))
            dependencies.append((job2, job3))
            dependencies.append((job2, job4))

            group_sulci = Group(name="Sulci recognition",
                                elements=[job3, job4])
            group_subject = Group(
                name="sulci recognition -- subject " + repr(i),
                elements=[job1, job11, job12, job13, job2, group_sulci])

            root_group.append(group_subject)
        function_name = inspect.stack()[0][3]
        workflow = Workflow(jobs, dependencies, root_group, name=function_name)
        return workflow


if __name__ == "__main__":
    print WorkflowExamples.get_workflow_example_list()
