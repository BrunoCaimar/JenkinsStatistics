# coding=utf-8


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
