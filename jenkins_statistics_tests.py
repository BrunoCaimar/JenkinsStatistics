# coding=utf-8
import unittest
import jenkins_statistics

class JenkinsStatisticsTests(unittest.TestCase):

    def test_gerar_report_com_dados_de_um_mes_e_apenas_um_job_deve_retornar_mes_com_um_registro(self):
        lista = [
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=1),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=2),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=3)]

        report = jenkins_statistics.gerar_summary_report_jobs_por_mes(lista)

        self.assertEqual(1, len(report))
        self.assertEqual([(('09/2015',9,2015), 1)], report)

    def test_gerar_report_com_dados_diversos_deve_retornar_resultado_esperado(
            self):
        lista = [
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=1),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste2",
                 build=2),
            dict(build_date_month=10, build_date_year=2015, job_name="Teste",
                 build=3),
            dict(build_date_month=10, build_date_year=2015,
                 job_name="Teste2", build=3),
            dict(build_date_month=10, build_date_year=2015,
                 job_name="Teste3", build=3)]

        report = jenkins_statistics.gerar_summary_report_jobs_por_mes(lista)

        self.assertEqual(2, len(report))
        self.assertEqual(sorted([(('09/2015', 9, 2015), 2),(('10/2015',10,2015),3)]),
                         sorted(report))

    def test_obter_jobs_no_mes_com_apenas_um_job_deve_retornar_apenas_um_registro(self):
        lista = [dict(build_date_month=9, build_date_year=2015, job_name="Teste", build=1),
                 dict(build_date_month=9, build_date_year=2015, job_name="Teste", build=2),
                 dict(build_date_month=9, build_date_year=2015, job_name="Teste", build=3)]
        jobs = jenkins_statistics.obter_jobs_no_mes_ano(("09/2015",9,2015), lista)
        self.assertEqual(1, len(jobs))
        self.assertEqual(["Teste"], jobs)


    def test_obter_jobs_no_mes_com_mais_de_um_job_deve_retornar_jobs_esperados(
            self):
        lista = [dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                      build=1),
                 dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                      build=2),
                 dict(build_date_month=9, build_date_year=2015, job_name="Teste2",
                      build=3)]

        jobs = jenkins_statistics.obter_jobs_no_mes_ano(("09/2015", 9, 2015), lista)
        self.assertEqual(2, len(jobs))
        self.assertEqual(["Teste", "Teste2"], jobs)

    def test_obter_jobs_no_mes_com_apenas_um_job_no_mes_deve_retornar_apenas_job_esperado(
            self):
        lista = [
            dict(build_date_month=9,
                 build_date_year=2015,
                 job_name="Teste",
                 build=1),
            dict(build_date_month=9,
                 build_date_year=2015,
                 job_name="Teste",
                 build=2),
            dict(build_date_month=10,
                 build_date_year=2015,
                 job_name="Teste2",
                 build=1)]

        jobs = jenkins_statistics.obter_jobs_no_mes_ano(("09/2015", 9, 2015), lista)
        self.assertEqual(1, len(jobs))
        self.assertEqual(["Teste"], jobs)

    def test_agrupamento_com_apenas_um_item_deve_retornar_um_item(self):
        lista = [dict(build_date_month=9, build_date_year=2015)]

        retorno = jenkins_statistics.obter_meses_disponiveis(lista)
        self.assertEqual(1,len(retorno))
        self.assertEqual([("09/2015", 9, 2015)], retorno)

    def test_agrupamento_com_mais_de_um_item_igual_deve_retornar_apenas_um_item(self):
        lista = [dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=9, build_date_year=2015)]

        retorno = jenkins_statistics.obter_meses_disponiveis(lista)
        self.assertEqual(1, len(retorno))
        self.assertEqual([("09/2015", 9, 2015)], retorno)


    def test_agrupamento_com_mais_de_um_item_diferente_deve_retornar_itens_diferentes(
            self):
        lista = [dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=10, build_date_year=2015)]

        retorno = jenkins_statistics.obter_meses_disponiveis(lista)
        self.assertEqual(2, len(retorno))
        self.assertEqual([("10/2015",10,2015),("09/2015", 9, 2015)], retorno)

