# coding=utf-8
import os
import jenkins_statistics
from JenkinsStatistics import jenkins_statistics_config


def obter_dados():
    dados = jenkins_statistics.get_jobs_details(
        jenkins_statistics_config.jenkins_url,
        jenkins_statistics_config.jenkins_user,
        jenkins_statistics_config.jenkins_password)
    return dados


def obter_dados_from_disk():
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, "dados.json")
    lista = eval(open(file_path).read())
    return lista


def print_reports(dados):
    print ""
    report_jobs_por_mes(dados)
    print ""
    report_builds_por_mes(dados)


def report_jobs_por_mes(dados):
    jobs_por_mes = jenkins_statistics.gerar_summary_report_jobs_por_mes(dados)

    sorted_data = sorted(jobs_por_mes)

    titulo = [item[0][0]
              for item in sorted_data
              if item[0][2] == 2015]

    detalhe = ["{0:^7}".format(item[1])
               for item in sorted_data
               if item[0][2] == 2015]

    separador = u'{:-^' + str(len(" | ".join(titulo))) + '}'

    print separador.format('')
    print separador.format(u" JOBS EXECUTADOS POR MÊS ")
    print separador.format('')
    print " | ".join(titulo)
    print separador.format('')
    print " | ".join(detalhe)
    print separador.format('')


def report_builds_por_mes(dados):
    builds_por_mes = jenkins_statistics.gerar_summary_report_builds_por_mes(
        dados)

    dados_2015 = [item
                  for item in builds_por_mes
                  if item[0][2] == 2015]

    resultado = []
    for result in [item[1] for item in dados_2015]:
        resultado += [s[0] for s in result]

    resultados_possiveis = sorted(list(set(resultado)))

    print ""

    titulo = u"|  MÊS/ANO  | " + \
             "".join(["{0:^10} | ".format(s) for s in resultados_possiveis])

    separador = u'{:-^' + str(len(titulo)) + '}'

    print separador.format('')
    print separador.format(u" BUILDS EXECUTADOS POR MÊS ")
    print separador.format('')
    print titulo
    print separador.format('')

    for item in dados_2015:
        result = item[1]
        mes_ano = item[0][0]
        detalhe_mes_ano = "| {0:^10}| ".format(mes_ano)

        for resultado in resultados_possiveis:
            qtd_builds = sum([r[1] for r in result if r[0] == resultado])
            detalhe_mes_ano += " {0:^9} | ".format(qtd_builds)
        print detalhe_mes_ano

    print separador.format('')


print_reports(obter_dados())
