# coding=utf-8
"""
Helper functions to access Jenkins using jenkins library
"""

from datetime import datetime
import multiprocessing as mp
import jenkins


def __get_builds_list(jenkins_reference, job_name):
    """
    Get builds list (for the job_name)

    :param job_name: Job Name, ``str``
    :param jenkins_reference: Jenkins handler, ``jenkins.Jenkins``
    :return: Build List, ``list``
    """
    builds = []

    try:
        job_info = jenkins_reference.get_job_info(job_name)

        if job_info is not None:
            builds = [d['number'] for d in job_info['builds']]

    except KeyError as exception:
        print u'Erro ao obter job_info: {0} - {1}'.format(job_name, exception.message)

    return builds


def __get_build_info(jenkins_url,
                     jenkins_username,
                     jenkins_password,
                     job_name,
                     build_number):
    """
    Get build info ( for the params job_name and build_number )

    :param jenkins_url: Jenkins server url, ``str``
    :param jenkins_username: Username to access Jenkins server or None, ``str``
    :param jenkins_password: Password to access Jenkins server or None, ``str``
    :param job_name: Job Name, ``str``
    :param build_number: Build Number, ``int``
    :return: dictionary of build information, ``dict``
    """
    build_info = None

    try:
        #  Tem que iniciar uma nova instancia pois esse metodo
        #  está rodando em modo paralelo
        ref = jenkins.Jenkins(jenkins_url,
                              jenkins_username,
                              jenkins_password)
        build_info = ref.get_build_info(job_name,
                                        build_number)
    except Exception as exception:
        print u"Erro ao obter build_info: {0} - {1}".format(job_name,
                                                            exception.message)
    return build_info


def __convert_build_info(job_name, build_number, build_info):
    """
    Convert build info in a dictionary like the example bellow:

        dict(job_name=job_name,
                build_number=build_number,
                build_date=build_date,
                build_date_month=build_date.month,
                build_date_year=build_date.year,
                build_result=build_result)

    :param job_name: Job Name, ``str``
    :param build_number: Build Number, ``int``
    :param build_info: Build info dictionary, ``dict``
    :return: Build info, ``dict``
    """
    build_timestamp = build_info['timestamp']
    build_result = build_info['result']
    build_date = datetime.fromtimestamp(build_timestamp / 1000.0)

    return dict(job_name=job_name,
                build_number=build_number,
                build_date=build_date,
                build_date_month=build_date.month,
                build_date_year=build_date.year,
                build_result=build_result)


def get_jobs_details(jenkins_url,
                     jenkins_user=None,
                     jenkins_password=None):
    """
    Get jobs details - Return all jobs details from the informed server

    :param jenkins_url: Jenkins server url, ``str``
    :param jenkins_user: Jenkins user name, ``str``
    :param jenkins_password: Jenkins password, ``str``
    :return: Job details, ``dict``
    """
    jenkins_reference = jenkins.Jenkins(jenkins_url,
                                        jenkins_user,
                                        jenkins_password)

    jobs = [job['name'] for job in jenkins_reference.get_jobs()]
    dados_jobs = []

    for job in jobs:
        print job

        builds = __get_builds_list(jenkins_reference, job)

        print 'builds:', len(builds)

        pool = mp.Pool(processes=mp.cpu_count())

        results = [pool.apply_async(__get_build_info,
                                    args=(jenkins_url,
                                          jenkins_user,
                                          jenkins_password,
                                          job,
                                          build_number,))
                   for build_number in builds]

        for result in results:
            build_info = result.get()
            if build_info is not None:
                dados_jobs.append(__convert_build_info(job,
                                                       0,
                                                       build_info))

    return dados_jobs
