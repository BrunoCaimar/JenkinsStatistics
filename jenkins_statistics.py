# coding=utf-8
from datetime import datetime
import jenkins


def get_jobs_info(jenkins_url,
                  jenkins_user=None,
                  jenkins_password=None):
    jenkins_reference = jenkins.Jenkins(jenkins_url,
                                        jenkins_user,
                                        jenkins_password)

    jobs = [job['name'] for job in jenkins_reference.get_jobs()]
    dados_jobs = []

    for job in jobs:
        print job

        details = None

        try:
            details = jenkins_reference.get_job_info(job)
        except KeyError as e:
            print u'Erro ao obter job_info: {0} - {1}'.format(job, e.message)

        builds = []
        if details is not None:
            builds = [d['number'] for d in details['builds']]

        for build_number in builds:
            print u'job: {1} build #{0}'.format(build_number, job)

            try:
                build_info = jenkins_reference.get_build_info(job,
                                                              build_number)
            except KeyError as e:
                print u"Erro ao obter build_info: {0} - {1}".format(job,
                                                                    e.message)

            build_timestamp = build_info['timestamp']

            build_date = datetime.fromtimestamp(build_timestamp / 1000.0)
            build_result = build_info['result']

            print build_result, build_date, build_timestamp
            print "----------------------------------------------------------"

            dados_jobs.append(dict(job_name=job,
                                   build_number=build_number,
                                   build_date=build_date,
                                   build_date_month=build_date.month,
                                   build_date_year=build_date.year,
                                   build_result=build_result))

    return dados_jobs


def gerar_summary_report_jobs_por_mes(jobs_info):
    meses = obter_meses_disponiveis(jobs_info)
    retorno = [(mes, len(obter_jobs_no_mes_ano(mes, jobs_info)))
               for mes in sorted(meses)]
    return retorno


def gerar_summary_report_builds_por_mes(jobs_info):
    meses = obter_meses_disponiveis(jobs_info)
    retorno = [(mes, obter_builds_por_resultado_no_mes_ano(mes, jobs_info))
               for mes in sorted(meses)]
    return retorno


def format_mes_ano(job_info):
    return "{0:=02}/{1}".format(job_info['build_date_month'],
                                job_info['build_date_year'])


def obter_meses_disponiveis(jobs_info):
    meses = [(format_mes_ano(item),
              item['build_date_month'],
              item['build_date_year'])
             for item in jobs_info]

    return list(set(meses))


def obter_jobs_no_mes_ano(mes_ano, jobs_info):
    return list(set([job_info['job_name']
                     for job_info in jobs_info
                     if format_mes_ano(job_info) == mes_ano[0]]))


def obter_builds_por_resultado_no_mes_ano(mes_ano, jobs_info):
    jobs_info_mes_ano = [job_info for job_info in jobs_info
                         if format_mes_ano(job_info) == mes_ano[0]]

    results = list(set([job_info['build_result']
                        for job_info in jobs_info_mes_ano]))

    builds_por_resultado = []
    for result in results:
        builds_por_resultado.append((
            result,
            sum([1 for item in jobs_info_mes_ano
                 if item['build_result'] == result])))
    return builds_por_resultado
