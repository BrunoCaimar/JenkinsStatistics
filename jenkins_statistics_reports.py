# coding=utf-8
"""
Jenkins statistics reports generator

Run it in command line after adjust configuration on jenkins_statistics_config.py file

Generates a report in following format:

---------------------------------------------------------------------------------------
------------------------------- JOBS EXECUTADOS POR MÊS -------------------------------
---------------------------------------------------------------------------------------
01/2015 | 02/2015 | 03/2015 | 04/2015 | 05/2015 | 06/2015 | 07/2015 | 08/2015 | 09/2015
---------------------------------------------------------------------------------------
   8    |    7    |   15    |   12    |   12    |   15    |   16    |   31    |   30
---------------------------------------------------------------------------------------


-------------------------------------------------------------------------------
-------------------------- BUILDS EXECUTADOS POR MÊS --------------------------
-------------------------------------------------------------------------------
|  Month/Year  |    None    |  ABORTED   |  FAILURE   |  SUCCESS   |  UNSTABLE  |
-------------------------------------------------------------------------------
|  01/2015  |      0     |      0     |     12     |      7     |     10     |
-------------------------------------------------------------------------------


"""
import datetime
from jenkins_date_range_functions import get_months_array, get_starting_month

import jenkins_api_functions
import jenkins_statistics
import jenkins_statistics_config


def get_data_from_jenkins():
    """
    Get job details from Jenkins server

    :return: Job details, ``list(dict)``
    """
    inicio = datetime.datetime.now()
    print "start gettting data: ", inicio

    dados = jenkins_api_functions.get_jobs_details(
        jenkins_statistics_config.JENKINS_URL,
        jenkins_statistics_config.JENKINS_USER,
        jenkins_statistics_config.JENKINS_PASSWORD)

    print u"finish getting data: ", inicio, datetime.datetime.now()
    print u"elapsed time: {0}".format(datetime.datetime.now() - inicio)
    return dados


def print_reports(jobs_details):
    """

    Print reports: Jobs by month/year and Builds by month/year
    :param jobs_details: Job details, ``list``
    """
    date_range = get_months_array(get_starting_month(jenkins_statistics_config.NUMBER_OF_MONTHS_TO_GET_DATA,
                                                    jenkins_statistics_config.INCLUDE_ACTUAL_MONTH),
                                  jenkins_statistics_config.NUMBER_OF_MONTHS_TO_GET_DATA)

    print ""
    summary_jobs_by_month(jobs_details, date_range)
    print ""
    summary_builds_by_month(jobs_details, date_range)
    print ""

    date_range.reverse()
    for item in range(2):
        print top_jobs(jobs_details, date_range[item][1], date_range[item][0])
        print ""

def top_jobs(jobs_details, year, month):
    """
    Print top jobs by year/month
    :param jobs_details: Jobs
    :param year: Year
    :param month: Month
    """
    titulo = u"|  TOP JOBS BY BUILDS: {0}  |".format(jenkins_statistics.get_formatted_month_year(month, year))

    separador = u'{:-^' + str(len(titulo) + 40) + '}'
    separador_detalhe = u'| {:^' + str(len(titulo) + 40 - 4) + '} |'

    print separador.format('')
    print titulo
    print separador.format('')

    tops = jenkins_statistics.top_jobs_by_builds(jobs_details, year, month)
    for job in tops:
        print separador_detalhe.format("{0}: {1}".format(job[1], job[0]))

    print separador.format('')


def summary_jobs_by_month(jobs_details, date_range):
    """
    Print report jobs by month
    :param date_range: Date range to report
    :param jobs_details: Jobs details, ``list``
    """
    jobs_por_mes = jenkins_statistics.get_summary_jobs_by_month(jobs_details)

    sorted_data = sorted(jobs_por_mes)

    titulo = [item[0][0]
              for item in sorted_data
              if (item[0][1], item[0][2]) in date_range]

    if len(titulo) == 0:
        return

    detalhe = ["{0:^7}".format(item[1])
               for item in sorted_data
               if (item[0][1], item[0][2]) in date_range]

    separador = u'{:-^' + str(len(" | ".join(titulo))) + '}'

    print separador.format('')
    print separador.format(u" ACTIVE JOBS BY MONTH/YEAR (Active = at least one build) ")
    print separador.format('')
    print " | ".join(titulo)
    print separador.format('')
    print " | ".join(detalhe)
    print separador.format('')


def summary_builds_by_month(jobs_details, date_range):
    """
    Print report builds by month/year
    :param year: Date Range to select data
    :param jobs_details: Jobs details, ``list``
    """
    builds_por_mes = jenkins_statistics.get_summary_builds_by_month(jobs_details)

    selected_data = [item
                     for item in builds_por_mes
                     if (item[0][1], item[0][2]) in date_range]

    resultado = []
    for result in [item[1] for item in selected_data]:
        resultado += [s[0] for s in result]

    resultados_possiveis = sorted(list(set(resultado)))

    print ""

    titulo = u"|  Month/Year  | " + \
             "".join(["{0:^10} | ".format(s) for s in resultados_possiveis])

    separador = u'{:-^' + str(len(titulo)) + '}'

    print separador.format('')
    print separador.format(u" BUILDS BY MONTH ")
    print separador.format('')
    print titulo
    print separador.format('')

    for item in selected_data:
        result = item[1]
        mes_ano = item[0][0]
        detalhe_mes_ano = "| {0:^13}| ".format(mes_ano)

        for resultado in resultados_possiveis:
            qtd_builds = sum([r[1] for r in result if r[0] == resultado])
            detalhe_mes_ano += " {0:^9} | ".format(qtd_builds)
        print detalhe_mes_ano

    print separador.format('')


if __name__ == '__main__':
    print_reports(get_data_from_jenkins())


