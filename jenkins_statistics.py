# coding=utf-8
"""
Jenkins statistics related functions
"""


def get_summary_jobs_by_month(jobs_info):
    """
    Returns jobs per month summary report

    :param jobs_info: Jobs info dictionary, ``dict``
    :return: list with jobs per month summary, ``list``
    """
    meses = get_available_months(jobs_info)
    retorno = [(mes, len(get_jobs_by_month_year(mes, jobs_info)))
               for mes in sorted(meses)]
    return retorno


def get_summary_builds_by_month(jobs_info):
    """
    Return builds per month summary report

    :param jobs_info: Jobs info dictionary, ``dict``
    :return: list with builds per month summary, ``list``
    """
    meses = get_available_months(jobs_info)
    retorno = [(mes, get_builds_per_result(mes, jobs_info))
               for mes in sorted(meses)]
    return retorno


def format_month_year(job_info):
    """
    Returns month/year formatted like MM/YYYY.
    e.g.: 09/2015

    :param job_info: Job info, ``dict``
    :return: Formatted month/year (e.g. 09/2015), ``str``
    """
    return "{0:=02}/{1}".format(job_info['build_date_month'],
                                job_info['build_date_year'])


def get_available_months(jobs_info):
    """
    Return list with tuple with months available.
    e.g:
    ('09/2015', month, year)

    :param jobs_info: Jobs info, ``list``
    :return: list with months, ``list``
    """
    meses = [(format_month_year(item),
              item['build_date_month'],
              item['build_date_year'])
             for item in jobs_info]

    return list(set(meses))


def get_jobs_by_month_year(mes_ano, jobs_info):
    """
    Returns jobs for the informed month/year
    :param mes_ano: Formatted month/year (e.g: '09/2015'), ``str``
    :param jobs_info: Jobs info, ``dict``
    :return: list with jobs, ``list``
    """
    return list(set([job_info['job_name']
                     for job_info in jobs_info
                     if format_month_year(job_info) == mes_ano[0]]))


def get_builds_per_result(mes_ano, jobs_info):
    """
    Returns builds per result for the month/year
    :param mes_ano: Month/year formatted (e.g.: '09/2015'), ``str``
    :param jobs_info: Jobs info, ``dict``
    :return: Builds per result summary, ``list``
    """
    jobs_info_mes_ano = [job_info for job_info in jobs_info
                         if format_month_year(job_info) == mes_ano[0]]

    results = list(set([job_info['build_result']
                        for job_info in jobs_info_mes_ano]))

    builds_por_resultado = []
    for result in results:
        builds_por_resultado.append((
            result,
            sum([1 for item in jobs_info_mes_ano
                 if item['build_result'] == result])))
    return builds_por_resultado
