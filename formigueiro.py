import random

# Classes de formigas
class Formiga:
    def __init__(self, coleta_diaria, consumo_diario):
        self.coleta_diaria = coleta_diaria
        self.consumo_diario = consumo_diario
    
    def consumir(self):
        return self.consumo_diario

class Operaria(Formiga):
    def __init__(self, coleta_diaria, consumo_diario):
        super().__init__(coleta_diaria, consumo_diario)

class Soldada(Formiga):
    def __init__(self, consumo_diario):
        super().__init__(0, consumo_diario)  # Formigas soldadas não coletam comida

# Classe Ovo
class Ovo:
    def __init__(self, dias_eclodir):
        self.dias_eclodir = dias_eclodir
    
    def passar_dia(self):
        if self.dias_eclodir > 0:
            self.dias_eclodir -= 1
    
    def ovo_pronto(self):
        return self.dias_eclodir == 0

# Classe Rainha
class Rainha:
    def __init__(self, ovos_diarios, dias_eclodir):
        self.ovos_diarios = ovos_diarios
        self.dias_eclodir = dias_eclodir

    def botar_ovos(self):
        return [Ovo(self.dias_eclodir) for _ in range(self.ovos_diarios)]

# Classe Formigueiro
class Formigueiro:
    def __init__(self, comida_total, formigas_totais):
        self.comida_total = comida_total
        self.formigas_totais = formigas_totais

    def tamanho(self):
        return 0.1 * self.comida_total + 3 * self.comida_total

# Classe Status
class Status:
    def __init__(self, formigas_iniciais, comida_inicial, coleta_diaria, consumo_diario, ovos_diarios, dias_eclodir):
        self.formigas = []
        self.rainhas = [Rainha(ovos_diarios, dias_eclodir)]
        self.comida = comida_inicial
        self.dias = 0
        self.ovos = []

        # Proporção de operárias e soldadas
        for _ in range(formigas_iniciais):
            if random.random() < 1/3:
                self.formigas.append(Soldada(consumo_diario))
            else:
                self.formigas.append(Operaria(coleta_diaria, consumo_diario))

    def proximo_dia(self):
        self.dias += 1

        # Coleta de comida
        coleta_do_dia = sum(formiga.coleta_diaria for formiga in self.formigas)
        self.comida += coleta_do_dia

        # Consumo de comida
        consumo_do_dia = sum(formiga.consumo_diario for formiga in self.formigas)
        self.comida -= consumo_do_dia

        # Adicionar novas rainhas se necessário
        if len(self.formigas) >= 200 * len(self.rainhas):
            self.rainhas.append(Rainha(self.rainhas[0].ovos_diarios, self.rainhas[0].dias_eclodir))

        # Botar ovos
        for rainha in self.rainhas:
            novos_ovos = rainha.botar_ovos()
            self.ovos.extend(novos_ovos)

        # Eclodir ovos
        formigas_nascidas = 0
        for ovo in self.ovos:
            ovo.passar_dia()
            if ovo.ovo_pronto():
                formigas_nascidas += 1
        self.ovos = [ovo for ovo in self.ovos if not ovo.ovo_pronto()]

        # Adicionar formigas nascidas
        for _ in range(formigas_nascidas):
            if random.random() < 1/3:
                self.formigas.append(Soldada(self.formigas[0].consumo_diario))
            else:
                self.formigas.append(Operaria(self.formigas[0].coleta_diaria, self.formigas[0].consumo_diario))

        # Conferir se a comida não acabou
        if self.comida <= 0:
            return "FALHA", len(self.formigas), len(self.rainhas), len(self.ovos), self.comida
        
        return "CONTINUAR", len(self.formigas), len(self.rainhas), len(self.ovos), self.comida

    def status_final(self):
        if self.dias >= dias_totais:
            return "SUCESSO"
        else:
            return "FALHA"

# Pedir os parâmetros iniciais para a simulação
print("CONFIGURAÇÃO INICIAL DO FORMIGUEIRO:")
formigas_iniciais = int(input("FORMIGAS INICIAIS: "))
comida_inicial = int(input("COMIDA INICIAL: "))
coleta_diaria = int(input("COLETA DE CADA OPERARIA: "))
consumo_diario = int(input("CONSUMO DAS FORMIGAS: "))
ovos_diarios = int(input("OVOS BOTADOS POR DIA: "))
dias_eclodir = int(input("DIAS PARA ECLODIR OS OVOS: "))
dias_totais = int(input("DIAS DA SIMULAÇÃO: "))

status_iniciais = Status(formigas_iniciais, comida_inicial, coleta_diaria, consumo_diario, ovos_diarios, dias_eclodir)

# Imprimindo os status iniciais do formigueiro
formigas_iniciais = len(status_iniciais.formigas)
rainhas_iniciais = len(status_iniciais.rainhas)
comida_inicial = status_iniciais.comida
tamanho_inicial = Formigueiro(comida_inicial, formigas_iniciais).tamanho()
ovos_iniciais = len(status_iniciais.ovos)

print(f"\nEstado inicial do formigueiro:")
print(f"  - {formigas_iniciais} formigas")
print(f"  - {rainhas_iniciais} rainhas")
print(f"  - {ovos_iniciais} ovos")
print(f"  - Comida inicial: {comida_inicial}")
print(f"  - Tamanho inicial do formigueiro: {tamanho_inicial:.2f} cm\n")

# Simulação dos dias
print("Simulação dos dias:")
print("-------------------")
estado = "CONTINUAR"
for dia in range(1, dias_totais + 1):
    estado, formigas_atuais, rainhas_atuais, ovos_atuais, comida_restante = status_iniciais.proximo_dia()
    tamanho_atual = Formigueiro(comida_restante, formigas_atuais).tamanho()
    print(f"Dia {dia}:")
    print(f"  - {formigas_atuais} formigas")
    print(f"  - {rainhas_atuais} rainhas")
    print(f"  - {ovos_atuais} ovos")
    print(f"  - Comida restante: {comida_restante}")
    print(f"  - Tamanho do formigueiro: {tamanho_atual:.2f} cm")
    print(f"  - Status: {estado}")
    print("-------------------")
    if estado == "FALHA":
        break

# Verificar status final
status_final = status_iniciais.status_final()
print(f"\nSimulação concluída com status: {status_final}")