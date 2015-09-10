# coding=utf-8
import os
import unittest
import JenkinsStatistics.jenkins_statistics


class JenkinsStatisticsTests(unittest.TestCase):
    def job_info_factory(self,
                         month=9,
                         year=2015,
                         name="Teste",
                         number=1,
                         result="SUCCESS"):
        return dict(build_date_month=month,
                    build_date_year=year,
                    job_name=name,
                    build_number=number,
                    build_result=result)

    def test_obter_builds_por_resultado_no_mes_ano_para_um_build_por_resultado_deve_retornar_um_build_por_resultado(
            self):
        lista = [self.job_info_factory(result="FAILURE"),
                 self.job_info_factory(result="UNSTABLE"),
                 self.job_info_factory(result="ABORTED"),
                 self.job_info_factory()]

        dados = JenkinsStatistics.jenkins_statistics.get_builds_per_result(
            ("09/2015",),
            lista)

        self.assertEqual([('FAILURE', 1),
                          ('UNSTABLE', 1),
                          ('SUCCESS', 1),
                          ('ABORTED', 1)], dados)

    def test_obter_builds_por_resultado_no_mes_ano_para_mais_de_um_resultado_deve_retornar_resultado_com_total_correto(
            self):
        lista = [self.job_info_factory(result="FAILURE"),
                 self.job_info_factory(result="FAILURE"),
                 self.job_info_factory(result="UNSTABLE"),
                 self.job_info_factory(result="ABORTED"),
                 self.job_info_factory(),
                 self.job_info_factory(),
                 self.job_info_factory()]

        dados = JenkinsStatistics.jenkins_statistics.get_builds_per_result(
            ("09/2015",),
            lista)

        self.assertEqual([('FAILURE', 2),
                          ('UNSTABLE', 1),
                          ('SUCCESS', 3),
                          ('ABORTED', 1)], dados)

    def test_obter_builds_por_resultado_no_mes_ano_para_dados_conhecidos_deve_retornar_resultado_conhecido(
            self):
        dir_name = os.path.dirname(__file__)
        file_path = os.path.join(dir_name, "dados.json")
        lista = eval(open(file_path).read())

        dados = JenkinsStatistics.jenkins_statistics.get_builds_per_result(
            ("08/2015",),
            lista)

        self.assertEqual([('FAILURE', 2),
                          ('UNSTABLE', 21),
                          ('ABORTED', 1),
                          ('SUCCESS', 105)], dados)

    def test_gerar_report_com_dados_de_um_mes_e_apenas_um_job_deve_retornar_mes_com_um_registro(
            self):
        lista = [
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=1),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=2),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=3)]

        report = JenkinsStatistics.jenkins_statistics.get_summary_jobs_by_month(lista)

        self.assertEqual(1, len(report))
        self.assertEqual([(('09/2015', 9, 2015), 1)], report)

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

        report = JenkinsStatistics.jenkins_statistics.get_summary_jobs_by_month(lista)

        self.assertEqual(2, len(report))
        self.assertEqual(
            sorted([(('09/2015', 9, 2015), 2), (('10/2015', 10, 2015), 3)]),
            sorted(report))

    def test_obter_jobs_no_mes_com_apenas_um_job_deve_retornar_apenas_um_registro(
            self):
        lista = [
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=1),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=2),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=3)]
        jobs = JenkinsStatistics.jenkins_statistics.get_jobs_by_month_year(("09/2015", 9, 2015), lista)
        self.assertEqual(1, len(jobs))
        self.assertEqual(["Teste"], jobs)

    def test_obter_jobs_no_mes_com_mais_de_um_job_deve_retornar_jobs_esperados(
            self):
        lista = [
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=1),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste",
                 build=2),
            dict(build_date_month=9, build_date_year=2015, job_name="Teste2",
                 build=3)]

        jobs = JenkinsStatistics.jenkins_statistics.get_jobs_by_month_year(("09/2015", 9, 2015), lista)
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

        jobs = JenkinsStatistics.jenkins_statistics.get_jobs_by_month_year(("09/2015", 9, 2015), lista)
        self.assertEqual(1, len(jobs))
        self.assertEqual(["Teste"], jobs)

    def test_agrupamento_com_apenas_um_item_deve_retornar_um_item(self):
        lista = [dict(build_date_month=9, build_date_year=2015)]

        retorno = JenkinsStatistics.jenkins_statistics.get_available_months(lista)
        self.assertEqual(1, len(retorno))
        self.assertEqual([("09/2015", 9, 2015)], retorno)

    def test_agrupamento_com_mais_de_um_item_igual_deve_retornar_apenas_um_item(
            self):
        lista = [dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=9, build_date_year=2015)]

        retorno = JenkinsStatistics.jenkins_statistics.get_available_months(lista)
        self.assertEqual(1, len(retorno))
        self.assertEqual([("09/2015", 9, 2015)], retorno)

    def test_agrupamento_com_mais_de_um_item_diferente_deve_retornar_itens_diferentes(
            self):
        lista = [dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=9, build_date_year=2015),
                 dict(build_date_month=10, build_date_year=2015)]

        retorno = JenkinsStatistics.jenkins_statistics.get_available_months(lista)
        self.assertEqual(2, len(retorno))
        self.assertEqual([("10/2015", 10, 2015), ("09/2015", 9, 2015)], retorno)
