# coding=utf-8

from datetime import datetime
import multiprocessing as mp
import jenkins


def __get_builds_list(jenkins_reference, job_name):
    builds = []

    try:
        job_info = jenkins_reference.get_job_info(job_name)

        if job_info is not None:
            builds = [d['number'] for d in job_info['builds']]

    except KeyError as e:
        print u'Erro ao obter job_info: {0} - {1}'.format(job_name, e.message)

    return builds


def __get_build_info(jenkins_url,
                     jenkins_username,
                     jenkins_password,
                     job_name,
                     build_number):
    build_info = None

    try:
        #  Tem que iniciar uma nova instancia pois esse metodo
        #  está rodando em modo paralelo
        ref = jenkins.Jenkins(jenkins_url,
                              jenkins_username,
                              jenkins_password)
        build_info = ref.get_build_info(job_name,
                                        build_number)
    except Exception as e:
        print u"Erro ao obter build_info: {0} - {1}".format(job_name,
                                                            e.message)
    return build_info


def __converter_build_info(job_name, build_number, build_info):
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
                dados_jobs.append(__converter_build_info(job,
                                                         0,
                                                         build_info))

    return dados_jobs
