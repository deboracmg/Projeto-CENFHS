from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from painel_administrativo.models.servicos import (
    Aula,
    Servico,
    Encontro,
    Turma,
    Matricula,
    Frequencia,
    Tratamento,
    Avaliacao
)

from painel_administrativo.models.pessoas import (
    Aluno,
    Parente,
    Parentesco,
    Saude,
    Socioeconomico,
    Profissional,
    Paciente
)

import random


class Command(BaseCommand):
    help = "Cria dados iniciais para testes do sistema"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("Criando dados iniciais...")

        # ==========================================================
        # 1. ENDEREÇOS - 8 registros
        # ==========================================================

        enderecos = [
            ("58400-001", "Rua João Pessoa", "120", "Centro", "Campina Grande", "PB", "URBANA"),
            ("58410-120", "Rua das Acácias", "45", "Catolé", "Campina Grande", "PB", "URBANA"),
            ("58405-230", "Rua José de Alencar", "300", "Prata", "Campina Grande", "PB", "URBANA"),
            ("58415-410", "Rua São José", "78", "Liberdade", "Campina Grande", "PB", "URBANA"),
            ("58420-550", "Sítio Lagoa Seca", "S/N", "Zona Rural", "Lagoa Seca", "PB", "RURAL"),
            ("58430-620", "Rua Nova", "210", "Alto Branco", "Campina Grande", "PB", "URBANA"),
            ("58435-730", "Rua Esperança", "90", "Malvinas", "Campina Grande", "PB", "URBANA"),
            ("58440-840", "Sítio São Pedro", "S/N", "Zona Rural", "Queimadas", "PB", "RURAL"),
        ]

        # ==========================================================
        # 2. ALUNOS - 12 registros
        # ==========================================================

        alunos_dados = [
            ("Ana Beatriz Silva", "11111111101", date(2011, 3, 15), "FEMININO", "PARDA"),
            ("Carlos Eduardo Santos", "11111111102", date(2010, 7, 22), "MASCULINO", "PRETA"),
            ("Maria Vitória Oliveira", "11111111103", date(2012, 1, 10), "FEMININO", "BRANCA"),
            ("João Pedro Lima", "11111111104", date(2009, 11, 5), "MASCULINO", "PARDA"),
            ("Beatriz Souza Costa", "11111111105", date(2013, 5, 18), "FEMININO", "PARDA"),
            ("Lucas Gabriel Ferreira", "11111111106", date(2011, 9, 30), "MASCULINO", "BRANCA"),
            ("Mariana Alves Rocha", "11111111107", date(2010, 2, 14), "FEMININO", "PRETA"),
            ("Pedro Henrique Martins", "11111111108", date(2012, 8, 27), "MASCULINO", "PARDA"),
            ("Laura Fernanda Gomes", "11111111109", date(2013, 12, 3), "FEMININO", "BRANCA"),
            ("Rafael Augusto Nunes", "11111111110", date(2009, 6, 19), "MASCULINO", "PARDA"),
            ("Julia Cristina Barbosa", "11111111111", date(2011, 10, 8), "FEMININO", "AMARELA"),
            ("Mateus Vinicius Araújo", "11111111112", date(2010, 4, 25), "MASCULINO", "PRETA"),
        ]

        alunos = []

        for i, dados in enumerate(alunos_dados):
            numero = random.randint(0, 7)
            aluno = Aluno.objects.create(
                nome=dados[0],
                cpf=dados[1],
                data_nascimento=dados[2],
                genero=dados[3],
                raca=dados[4],
                n_certidao=f"CERT-{10000 + i}",
                telefone=f"(83) 9{90000000 + i:08d}",
                email=f"aluno{i + 1}@exemplo.com",
                cep=enderecos[numero][0],
                rua=enderecos[numero][1],
                numero=enderecos[numero][2],
                bairro=enderecos[numero][3],
                cidade=enderecos[numero][4],
                uf=enderecos[numero][5],
                zona=enderecos[numero][6],
                observacoes="Aluno cadastrado para testes do sistema.",
                autoriza_uso_imagem=i % 2 == 0,
            )
            alunos.append(aluno)

        # ==========================================================
        # 3. PARENTES - 6 registros
        # ==========================================================

        parentes_dados = [
            ("Maria José Silva", "22222222201", "Professora", "Escola Municipal", "SUPERIOR"),
            ("José Carlos Santos", "22222222202", "Comerciante", "Comércio local", "MEDIO"),
            ("Luciana Oliveira", "22222222203", "Costureira", "Autônoma", "MEDIO"),
            ("Roberto Lima", "22222222204", "Motorista", "Empresa de Transporte", "MEDIO"),
            ("Fernanda Costa", "22222222205", "Auxiliar administrativa", "Empresa privada", "SUPERIOR"),
            ("Paulo Ferreira", "22222222206", "Pedreiro", "Autônomo", "FUNDAMENTAL"),
        ]

        parentes = []

        for i, dados in enumerate(parentes_dados):
            parente = Parente.objects.create(
                nome=dados[0],
                cpf=dados[1],
                vivo=True,
                profissao=dados[2],
                local_trabalho=dados[3],
                telefone=f"(83) 9{91000000 + i:08d}",
                escolaridade=dados[4],
            )
            parentes.append(parente)

        # ==========================================================
        # 4. PARENTESCO - 6 registros
        # ==========================================================

        parentescos = [
            ("Mãe", True, True),
            ("Pai", True, True),
            ("Mãe", True, False),
            ("Pai", True, False),
            ("Avó", False, True),
            ("Tia", False, True),
        ]

        for i, dados in enumerate(parentescos):
            Parentesco.objects.create(
                aluno=alunos[i],
                parente=parentes[i],
                parentesco=dados[0],
                responsavel=dados[1],
                contato_emergencia=dados[2],
            )

        # ==========================================================
        # 5. SAÚDE - 8 registros
        # ==========================================================

        problemas = [
            ("Nenhum problema informado.", "", "O+", "", "", "Em dia"),
            ("Asma leve.", "Acompanhamento médico.", "A+", "Poeira", "Bombinha quando necessário", "Em dia"),
            ("Nenhum problema informado.", "", "B+", "", "", "Em dia"),
            ("Rinite.", "Acompanhamento eventual.", "O-", "Poeira", "Antialérgico", "Em dia"),
            ("Nenhum problema informado.", "", "AB+", "", "", "Em dia"),
            ("Nenhum problema informado.", "", "O+", "", "", "Em dia"),
            ("Alergia respiratória.", "Acompanhamento médico.", "A+", "Poeira e mofo", "Antialérgico", "Em dia"),
            ("Nenhum problema informado.", "", "B-", "", "", "Em dia"),
        ]

        for i, dados in enumerate(problemas):
            Saude.objects.create(
                aluno=alunos[i],
                sus=f"70000000000{i + 1}",
                problema_saude=dados[0],
                tratamento=dados[1],
                tipo_sanguineo=dados[2],
                alergia=dados[3],
                medicamento=dados[4],
                vacinas=dados[5],
            )

        # ==========================================================
        # 6. SOCIOECONÔMICO - 8 registros
        # ==========================================================

        situacoes = ["PROPRIA", "ALUGADA", "CEDIDA"]

        for i in range(8):
            Socioeconomico.objects.create(
                aluno=alunos[i],
                n_bolsa_familia=f"BF{100000 + i}",
                nis=f"{12000000000 + i}",
                escola=[
                    "Escola Municipal José Américo",
                    "Escola Estadual Monteiro Lobato",
                    "Escola Municipal Paulo Freire",
                ][i % 3],
                transporte=[
                    "Próprio",
                    "Transporte público",
                    "Transporte escolar",
                ][i % 3],
                renda_familiar=Decimal(
                    ["800", "1200", "1500", "1800"][i % 4]
                ),
                situacao_moradia=situacoes[i % 3],
                qtd_moradores=[4, 5, 3, 6][i % 4],
            )

        # ==========================================================
        # 7. PROFISSIONAIS - 7 registros
        # ==========================================================

        profissionais_dados = [
            ("Carlos Alberto Mendes", "33333333301", date(1985, 2, 10), "Professor de Informática"),
            ("Juliana Martins Silva", "33333333302", date(1990, 6, 21), "Professora de Dança"),
            ("Ricardo Gomes Oliveira", "33333333303", date(1982, 9, 15), "Professor de Esportes"),
            ("Patrícia Fernandes Lima", "33333333304", date(1988, 4, 7), "Assistente Social"),
            ("Marcos Vinicius Costa", "33333333305", date(1979, 12, 19), "Educador"),
            ("Camila Rodrigues Alves", "33333333306", date(1992, 8, 3), "Psicóloga"),
            ("Felipe Andrade Souza", "33333333307", date(1986, 11, 25), "Professor de Música"),
        ]

        profissionais = []

        for i, dados in enumerate(profissionais_dados):
            profissional = Profissional.objects.create(
                nome=dados[0],
                cpf=dados[1],
                data_nascimento=dados[2],
                telefone=f"(83) 9{92000000 + i:08d}",
                email=f"profissional{i + 1}@exemplo.com",
                area_atuacao=dados[3],
            )
            profissionais.append(profissional)

        # ==========================================================
        # 8. PACIENTES - 6 registros
        # ==========================================================

        pacientes_dados = [
            ("Antônio Carlos Silva", "44444444401", date(1972, 3, 12), "MASCULINO"),
            ("Maria de Lourdes Santos", "44444444402", date(1968, 7, 20), "FEMININO"),
            ("José Pereira Oliveira", "44444444403", date(1959, 11, 5), "MASCULINO"),
            ("Francisca Maria Lima", "44444444404", date(1975, 1, 28), "FEMININO"),
            ("Roberto Alves Costa", "44444444405", date(1980, 5, 16), "MASCULINO"),
            ("Sandra Regina Souza", "44444444406", date(1970, 9, 9), "FEMININO"),
        ]

        pacientes = []

        for i, dados in enumerate(pacientes_dados):
            numero = random.randint(0, 7)
            paciente = Paciente.objects.create(
                nome=dados[0],
                cpf=dados[1],
                data_nascimento=dados[2],
                genero=dados[3],
                telefone=f"(83) 9{93000000 + i:08d}",
                nome_mae=f"Maria da Silva {i + 1}",
                nome_pai=f"João da Silva {i + 1}",
                profissao=[
                    "Agricultor",
                    "Doméstica",
                    "Comerciante",
                    "Costureira",
                    "Pedreiro",
                    "Professora",
                ][i],
                cep=enderecos[numero][0],
                rua=enderecos[numero][1],
                numero=enderecos[numero][2],
                bairro=enderecos[numero][3],
                cidade=enderecos[numero][4],
                uf=enderecos[numero][5],
            )
            pacientes.append(paciente)

        # ==========================================================
        # 9. SERVIÇOS - 6 registros
        # ==========================================================

        servicos_dados = [
            ("Informática Básica", "CURSO"),
            ("Iniciação Musical", "CURSO"),
            ("Dança", "ATIVIDADE"),
            ("Futebol", "ATIVIDADE"),
            ("Oficina de Artes", "ATIVIDADE"),
            ("Encontro de Integração", "EVENTO"),
        ]

        servicos = []

        for nome, tipo in servicos_dados:
            servico = Servico.objects.create(
                nome=nome,
                tipo=tipo,
                ativo=True,
            )
            servicos.append(servico)

        # ==========================================================
        # 10. ENCONTROS - 4 registros
        # ==========================================================

        Encontro.objects.create(
            servico=servicos[2],
            responsavel_interno=profissionais[1],
            qtd_participantes=18,
            data_hora=datetime(2026, 10, 5, 14, 0),
            local="Salão",
        )

        Encontro.objects.create(
            servico=servicos[4],
            responsavel_interno=profissionais[5],
            qtd_participantes=15,
            data_hora=datetime(2026, 10, 10, 9, 0),
            local="Sala 03",
        )

        Encontro.objects.create(
            servico=servicos[5],
            responsavel_interno=profissionais[4],
            qtd_participantes=30,
            data_hora=datetime(2026, 10, 15, 15, 0),
            local="Auditório",
        )

        Encontro.objects.create(
            servico=servicos[5],
            responsavel_externo="Mariana Alves",
            qtd_participantes=25,
            data_hora=datetime(2026, 11, 8, 10, 0),
            local="Auditório",
        )

        # ==========================================================
        # 11. TURMAS - 4 registros
        # ==========================================================

        turmas = []

        turmas.append(
            Turma.objects.create(
                servico=servicos[0],
                descricao="Turma de Informática - Manhã",
                dias_semana=["SEG", "QUA", "SEX"],
                hora_inicio=time(8, 0),
                hora_fim=time(10, 0),
                local="Laboratório de Informática",
                responsavel=profissionais[0],
            )
        )

        turmas.append(
            Turma.objects.create(
                servico=servicos[0],
                descricao="Turma de Informática - Tarde",
                dias_semana=["TER", "QUI"],
                hora_inicio=time(14, 0),
                hora_fim=time(16, 0),
                local="Laboratório de Informática",
                responsavel=profissionais[0],
            )
        )

        turmas.append(
            Turma.objects.create(
                servico=servicos[1],
                descricao="Música - Iniciação",
                dias_semana=["SEG", "QUA"],
                hora_inicio=time(15, 0),
                hora_fim=time(17, 0),
                local="Sala de Música",
                responsavel=profissionais[6],
            )
        )

        turmas.append(
            Turma.objects.create(
                servico=servicos[3],
                descricao="Futebol - Infantil",
                dias_semana=["TER", "QUI"],
                hora_inicio=time(16, 0),
                hora_fim=time(18, 0),
                local="Quadra esportiva",
                responsavel=profissionais[2],
            )
        )

        # ==========================================================
        # 12. AULAS - 5 registros
        # ==========================================================

        aulas = []

        datas_aulas = [
            date(2026, 10, 5),
            date(2026, 10, 7),
            date(2026, 10, 9),
            date(2026, 10, 12),
            date(2026, 10, 14),
        ]

        for data_aula in datas_aulas:
            aulas.append(
                Aula.objects.create(
                    turma=turmas[0],
                    data=data_aula,
                )
            )

        # ==========================================================
        # 13. MATRÍCULAS - 5 registros
        # ==========================================================

        matriculas = []

        for i in range(5):
            matriculas.append(
                Matricula.objects.create(
                    aluno=alunos[i],
                    turma=turmas[0],
                    matriculado_por="Administrador",
                )
            )

        # ==========================================================
        # 14. FREQUÊNCIAS - 5 registros
        # ==========================================================

        for i in range(5):
            Frequencia.objects.create(
                matricula=matriculas[i],
                aula=aulas[i],
                presente=i % 3 != 0,
            )

        # ==========================================================
        # 15. TRATAMENTOS - 4 registros
        # ==========================================================

        tratamentos_dados = [
            ("Tratamento oncológico", "Paciente em acompanhamento médico."),
            ("Fisioterapia", "Sessões de fisioterapia."),
            ("Quimioterapia", "Acompanhamento conforme orientação médica."),
            ("Radioterapia", "Tratamento em andamento."),
        ]

        tratamentos = []

        for i, dados in enumerate(tratamentos_dados):
            tratamento = Tratamento.objects.create(
                paciente=pacientes[i],
                data_entrada=date(2026, 9, 1 + i),
                data_saida=None if i < 3 else date(2026, 10, 20),
                tipo_paciente="Paciente adulto",
                tratamento=dados[0],
                n_sessoes=[10, 20, 8, 15][i],
                observacoes=dados[1],
                acompanhante=[
                    "Maria Silva",
                    "João Santos",
                    "Ana Oliveira",
                    "Carlos Lima",
                ][i],
                telefone_acompanhante=f"(83) 9{94000000 + i:08d}",
                registrado_por="Administrador",
            )
            tratamentos.append(tratamento)

        # ==========================================================
        # 16. AVALIAÇÕES - 6 registros
        # ==========================================================

        for i, tratamento in enumerate(tratamentos):
            nota_base = (i % 3) + 3

            Avaliacao.objects.create(
                tratamento=tratamento,
                atendimento=nota_base,
                infraestrutura=4,
                higiene=5,
                alimentacao=4,
                comunicacao=5,
                acolhimento=5,
                organizacao=4,
                gestao=4,
            )

        # ==========================================================
        # TOTAL
        # ==========================================================

        total = (
            + Aluno.objects.count()
            + Parente.objects.count()
            + Parentesco.objects.count()
            + Saude.objects.count()
            + Socioeconomico.objects.count()
            + Profissional.objects.count()
            + Paciente.objects.count()
            + Servico.objects.count()
            + Encontro.objects.count()
            + Turma.objects.count()
            + Matricula.objects.count()
            + Aula.objects.count()
            + Frequencia.objects.count()
            + Tratamento.objects.count()
            + Avaliacao.objects.count()
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeed concluído! Total de registros: {total}"
            )
        )
