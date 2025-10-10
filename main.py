#    MASMORRAS LIMINARES ver. 0.9.0-beta ~~ Desenvolvido pelo Bandeirinha

import random
import os
import time

from rotas import warrior, wizard, rogue, rogue2
from enemies import goblin, skeleton, skull_archer, warrior_orc, gargula, death_champion, vecnas_eye, vecna_meets, vecna_sees_everything, dracolich
from structures import stairway, statue, wall, dungeon, dungeon2, dungeon3, magic_circle, magic_circle_blink, altar, lost_garden

def escolhe_guerreiro(warrior):
    return random.choice([warrior])

def escolhe_mago(wizard):
    return random.choice([wizard])

def escolhe_ladino(rogue):
    return random.choice([rogue])

def avanca_dungeon(dungeon, dungeon2, dungeon3, lost_garden):
    return random.choice([dungeon, dungeon2, dungeon3, lost_garden])


# ----------------------------- UTILITÁRIOS -----------------------------
def rolar_dado(lados):
    return random.randint(1, lados)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------- CLASSES BASE ----------------------------
class Personagem:
    def __init__(self, nome, hp, ac, ataque_bonus, dano_lados, classe, base_ataque_bonus, base_dano_lados):
        self.nome = nome
        self.hp = self.hp_max = hp
        self.ac = ac
        self.base_ac = ac
        self.base_hp_max = hp
        self.ataque_bonus = ataque_bonus
        self.dano_lados = dano_lados
        self.classe = classe
        self.inventario = ['poção de cura']
        self.arma = None
        self.armadura = None
        self.equipados = []  # até 6 itens
        self.cooldown_magia = 0
        self.bonus_temporario = 0
        self.invisivel = False
        self.pos = (0, 0)
        self.efeitos_ativos = {}  # Ex: {'berserker': 3, 'protecao': 2, 'valor_protecao': 3}
        self.base_ataque_bonus = base_ataque_bonus
        self.base_dano_lados = base_dano_lados

    def atacar(self, alvo):
        rolagem = rolar_dado(20)
        total_bonus = self.ataque_bonus + self.bonus_temporario + (self.arma['bonus'] if self.arma else 0)
        total = rolagem + total_bonus
        print(f"🎲 Rolagem de ataque: {rolagem} + {total_bonus} vs CA {alvo.ac}")

        dano = 0
        if rolagem == 20:
            dano = (rolar_dado(self.dano_lados) + (self.arma['dano'] if self.arma else 0)) * 2
            alvo.hp -= dano
            print(f"💥 ACERTO CRÍTICO! {self.nome} causa {dano} de dano em {alvo.nome}!")
        elif total >= alvo.ac:
            dano = rolar_dado(self.dano_lados) + (self.arma['dano'] if self.arma else 0)
            alvo.hp -= dano
            print(f"💥 {self.nome} acerta {alvo.nome} com {dano} de dano!")
        else:
            print(f"❌ {self.nome} erra o ataque.")
            return  # Se errou, não há dano extra

        # ============================
        # ⚡🔥 EFEITOS ESPECIAIS DE ITENS
        # ============================
        if self.arma:
            # Machado Anão Flamejante — Dano de fogo + DoT
            if self.arma['nome'] == 'Machado Flamejante':
                porcentagem = random.randint(15, 30) / 100
                crit_elemental = random.random() < 0.15  # 15% de crítico elemental
                dano_extra = int(dano * porcentagem * (2 if crit_elemental else 1))
                alvo.hp -= dano_extra
                print(f"🔥 Dano flamejante: +{dano_extra} ({int(porcentagem*100)}% do dano base){' [CRÍTICO ELEMENTAL!]' if crit_elemental else ''}!")
                alvo.efeitos_ativos['fogo'] = {'dano': dano_extra, 'turnos': 1}
                print(f"🔥 {alvo.nome} queimará mais {dano_extra} no próximo turno!")

            # Manoplas do Trovão — Dano elétrico + DoT
            elif self.arma['nome'] == 'Manoplas do Trovão':
                porcentagem = random.randint(15, 30) / 100
                crit_elemental = random.random() < 0.15  # 15% de crítico elemental
                dano_extra = int(dano * porcentagem * (2 if crit_elemental else 1))
                alvo.hp -= dano_extra
                print(f"⚡ Choque elétrico: +{dano_extra} ({int(porcentagem*100)}% do dano base){' [CRÍTICO ELEMENTAL!]' if crit_elemental else ''}!")
                alvo.efeitos_ativos['choque'] = {'dano': dano_extra, 'turnos': 1}
                print(f"⚡ {alvo.nome} sofrerá mais {dano_extra} de choque no próximo turno!")

        # Efeito especial: Arco Élfico com chance de repetir o ataque
        if self.arma and self.arma['nome'] == 'Arco Élfico':
            if self.classe == "Mago":
                chance = 0.2
            elif self.classe == "Guerreiro":
                chance = 0.35
            elif self.classe == "Ladino":
                chance = 0.5
            else:
                chance = 0.25

            if random.random() < chance:
                if self.classe == 'Ladino':
                    time.sleep(1), print(rogue2), time.sleep(1)
                print("🏹 O Arco Élfico dispara uma flecha extra!")
                rolagem_extra = rolar_dado(20)
                total_extra = rolagem_extra + total_bonus
                print(f"🎲 Rolagem extra: {rolagem_extra} + {total_bonus} vs CA {alvo.ac}")
                if rolagem_extra == 20:
                    dano_extra = (rolar_dado(self.dano_lados) + (self.arma['dano'])) * 2
                    alvo.hp -= dano_extra
                    print(f"💥 ACERTO CRÍTICO EXTRA! Causa {dano_extra} de dano em {alvo.nome}!")
                elif total_extra >= alvo.ac:
                    dano_extra = rolar_dado(self.dano_lados) + self.arma['dano']
                    alvo.hp -= dano_extra
                    print(f"💥 Flecha extra acerta e causa {dano_extra} de dano!")
                else:
                    print("❌ A flecha extra erra o alvo.")

        # ⚠️ Mantém o bônus enquanto efeito ativo
        if 'forca' not in self.efeitos_ativos and 'berserker' not in self.efeitos_ativos:
            self.bonus_temporario = 0

    # ==========================================================
    # Funções de uso, efeitos e equipamentos 
    # ==========================================================
    def processar_efeitos(self):
        """Processa DoTs e buffs ativos no início do turno do personagem."""
        remover = []
        for efeito, dados in self.efeitos_ativos.items():
            if isinstance(dados, dict) and 'dano' in dados:
                dano = dados['dano']
                self.hp -= dano
                print(f"☠️ {self.nome} sofre {dano} de dano por efeito de {efeito}!")
                dados['turnos'] -= 1
                if dados['turnos'] <= 0:
                    remover.append(efeito)
        for efeito in remover:
            del self.efeitos_ativos[efeito]

    def usar_magia(self, alvo):
        if self.classe != "Mago":
            print("❌ Apenas magos podem lançar magias!")
            return False
        if self.cooldown_magia > 0:
            print("❌ Magia em recarga!")
            return False

        dist = abs(alvo.pos[0] - self.pos[0]) + abs(alvo.pos[1] - self.pos[1])
        if dist > 3:
            print("❌ Alvo fora do alcance!")
            return False

        print("✨ Míssil Mágico lançado!")

        poder_magico = self.calcular_poder_magico_total()
        print(f"🔮 Poder mágico total: {poder_magico}")

        rolagem = rolar_dado(4) + 3
        print(f"🎲 Rolagem do Míssil Mágico: 1d4 + 3 = {rolagem}")

        dano_total = poder_magico + rolagem
        alvo.hp -= dano_total
        print(f"💥 Míssil Mágico causa {dano_total} de dano mágico em {alvo.nome}!")

        self.cooldown_magia = 5
        return True

    def usar_pocao(self):
        if not self.inventario:
            print("🚫 Sem poções!")
            return
        print("Inventário:")
        for i, item in enumerate(self.inventario):
            print(f"{i+1} - {item}")
        escolha = input("Escolha o número: ")
        try:
            item = self.inventario.pop(int(escolha)-1)
        except:
            print("❌ Escolha inválida.")
            return

        if item == 'poção de cura':
            cura = rolar_dado(8) + 2
            self.hp = min(self.hp + cura, self.hp_max)
            print(f"🧪 Recupera {cura} HP!")
        elif item == 'poção de força':
            forca = rolar_dado(8) + 2
            self.bonus_temporario = forca
            self.efeitos_ativos['forca'] = 6
            print(f"💪 Poção de Força ativa: +{forca} ataque por 6 turnos seus.")
        elif item == 'poção de invisibilidade':
            self.invisivel = True
            self.efeitos_ativos['invisibilidade'] = 3
            print("👻 Invisibilidade ativada por 3 turnos.")
        elif item.startswith('Elixir do Berserker'):
            bonus = int(item.split('+')[1])
            self.bonus_temporario = bonus
            self.efeitos_ativos['berserker'] = 6
            print(f"💢 Berserker ativado: +{bonus} no ataque por 6 turnos seus.")
        elif item.startswith('Orbe de Proteção'):
            bonus = int(item.split('+')[1])
            self.ac += bonus
            self.efeitos_ativos['protecao'] = 6
            self.efeitos_ativos['valor_protecao'] = bonus
            print(f"🛡️ Proteção ativada: +{bonus} CA por 6 rodadas.")
        elif item.startswith('Anel da Vitalidade'):
            self.gerenciar_equipamento(item)
            print(f"💖 Anel da Vitalidade equipado! Aumenta HP máximo enquanto equipado.")
        elif item.startswith('Lâmina Sombria'):
            bonus = int(item.split('+')[1])
            self.arma = {'nome': 'Lâmina Sombria', 'bonus': bonus, 'dano': bonus}
            self.gerenciar_equipamento(item)
            print(f"⚔️ Lâmina Sombria equipada (+{bonus} ataque/dano)!")
        elif item.startswith('Arco Élfico'):
            bonus = int(item.split('+')[1])
            self.arma = {'nome': 'Arco Élfico', 'bonus': bonus, 'dano': bonus // 2}
            self.gerenciar_equipamento(item)
            print(f"🏹 Arco Élfico equipado (+{bonus // 2} ataque/dano)! Tem chance de disparo duplo dependendo da classe.")
        elif item.startswith('Armadura de Mithril'):
            self.gerenciar_equipamento(item)
            print(f"🛡️ Armadura de Mithril equipada! CA aumentada enquanto equipada.")
        elif item.startswith('Machado Anão Flamejante'):
            bonus = int(item.split('+')[1])
            self.arma = {'nome': 'Machado Flamejante', 'bonus': bonus, 'dano': bonus + 2}
            self.gerenciar_equipamento(item)
            print(f"🔥 Machado Flamejante equipado (+{bonus} ataque, +fogo)!")
        elif item.startswith('Elmo da Fúria'):
            bonus = int(item.split('+')[1])
            self.bonus_temporario = bonus
            self.ac -= 1
            self.gerenciar_equipamento(item)
            print(f"🪖 Elmo da Fúria: +{bonus} dano no próximo ataque, -1 CA!")
        elif item == 'Botas do Silêncio':
            self.gerenciar_equipamento(item)
            print("👟 Botas do Silêncio equipadas! Reduzem a chance de engajar em combate.")
        elif item.startswith('Cajado de Gelo'):
            bonus = int(item.split('+')[1])
            if self.classe == 'Mago':
                self.arma = {'nome': 'Cajado de Gelo', 'bonus': bonus, 'dano': bonus // 2}
                self.gerenciar_equipamento(item)
                print(f"🧊 Cajado de Gelo equipado. +{bonus // 2} de dano mágico adicional.")
            else:
                print("❌ Apenas magos podem usar o Cajado de Gelo.")
        elif item == 'Tomo de Sabedoria Antiga':
            self.ac += 3
            print("📘 O conhecimento aumenta sua CA em +3!")
        elif item.startswith('Amuleto de Resistência'):
            self.gerenciar_equipamento(item)
            print("🛡️ Amuleto de Resistência equipado! Bônus aplicados enquanto estiver equipado.")
        elif item.startswith('Anel de Regeneração'):
            self.gerenciar_equipamento(item)
            print("💍 Anel de Regeneração equipado! Restaura 1 HP por turno enquanto estiver equipado.")
        elif item.startswith('Manoplas do Trovão'):
            bonus = int(item.split('+')[1])
            self.arma = {'nome': 'Manoplas do Trovão', 'bonus': bonus, 'dano': bonus + 2 // 2}
            self.gerenciar_equipamento(item)
            print(f"⚡ Manoplas do Trovão equipadas! +{bonus // 2} de ataque + dano elétrico.")
        elif item.startswith('Orbe Mental de Vecna'):
            bonus = int(item.split('+')[1])
            if self.classe == 'Mago':
                self.arma = {'nome': 'Orbe Mental de Vecna', 'bonus': bonus, 'dano': bonus // 2}
                self.gerenciar_equipamento(item)
                print(f"👁️ O Orbe de Vecna pulsa com magia! +{bonus // 2} ataque mágico e +15% de dano em magias enquanto equipado.")
            else:
                print("❌ Apenas magos podem usar o Orbe Mental de Vecna.")
        else:
            print("❓ Item desconhecido.")

    def gerenciar_equipamento(self, item_nome):
        if len(self.equipados) < 6:
            self.equipados.append(item_nome)
        else:
            print("🎒 Você já tem 6 itens equipados.")
            print("Equipados atuais:")
            for i, eq in enumerate(self.equipados, 1):
                print(f"{i} - {eq}")
            escolha = input("Digite o número do item que deseja substituir ou 'n' para cancelar: ")
            if escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(self.equipados):
                    removido = self.equipados.pop(idx)
                    print(f"❌ {removido} foi removido.")
                    self.equipados.append(item_nome)
                    print(f"✅ {item_nome} foi equipado.")
                else:
                    print("❌ Índice inválido.")
                    return
            else:
                print("❌ Equipamento cancelado.")
                return

        # Recalcular bônus após qualquer mudança
        self.atualizar_atributos_equipamento()

    def atualizar_efeitos(self):
        efeitos_para_remover = []

        for efeito, duracao in list(self.efeitos_ativos.items()):
            if isinstance(duracao, int):
                # Só decrementa se ainda houver rodadas
                if duracao > 1:
                    self.efeitos_ativos[efeito] -= 1
                else:
                    # Quando chega a 1, significa que este é o último turno válido
                    efeitos_para_remover.append(efeito)

        for efeito in efeitos_para_remover:
            # Remover o efeito no próximo turno
            if efeito in self.efeitos_ativos:
                del self.efeitos_ativos[efeito]

            # Mensagens uniformizadas
            if efeito in ['berserker', 'forca']:
                if efeito == 'berserker':
                    print("💢 O efeito do Elixir do Berserker acabou!")
                else:
                    print("💪 O efeito da Poção de Força acabou!")
                self.bonus_temporario = 0

            elif efeito == 'protecao':
                bonus = self.efeitos_ativos.pop('valor_protecao', None)
                if bonus:
                    self.ac -= bonus
                    print(f"🛡️ O efeito da Orbe de Proteção acabou (-{bonus} CA).")
                else:
                    print("🛡️ O efeito da Orbe de Proteção acabou.")

            elif efeito == 'invisibilidade':
                self.invisivel = False
                print("👁️ Sua invisibilidade desvaneceu.")

            else:
                print(f"⚠️ O efeito '{efeito}' acabou.")


    # ==========================================================
    # NOVA SEÇÃO — recalculando todos os bônus ofensivos e defensivos
    # ==========================================================
    def atualizar_atributos_equipamento(self):
        # Restaurar os valores base
        self.ac = self.base_ac
        self.hp_max = self.base_hp_max
        self.ataque_bonus = self.base_ataque_bonus
        self.dano_lados = self.base_dano_lados

        hp_bonus = 0
        ca_bonus = 0
        ataque_bonus = 0
        dano_bonus = 0

        for item in self.equipados:
            try:
                if '+' in item:
                    bonus = int(item.split('+')[1])
                else:
                    bonus = 0
            except:
                bonus = 0

            # Armaduras e defensivos
            if 'Armadura de Mithril' in item:
                ca_bonus += bonus
            elif 'Amuleto de Resistência' in item:
                ca_bonus += 1
                hp_bonus += 5
            elif 'Anel da Vitalidade' in item:
                hp_bonus += bonus

            # Itens ofensivos
            elif any(palavra in item for palavra in [
                'Lâmina Sombria', 'Arco Élfico', 'Machado Anão Flamejante', 'Manoplas do Trovão', 'Elmo da Fúria', 
                'Cajado de Gelo', 'Orbe Mental de Vecna'
            ]):
                ataque_bonus += bonus
                dano_bonus += bonus // 2 if bonus > 1 else 1

        self.ac += ca_bonus
        self.hp_max = self.base_hp_max + hp_bonus
        self.ataque_bonus = self.base_ataque_bonus + ataque_bonus
        self.dano_lados = self.base_dano_lados + dano_bonus

        # Garantir que HP atual não ultrapasse o novo máximo
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def turno_magia(self):
        if self.cooldown_magia > 0:
            self.cooldown_magia -= 1

        # Contar quantos Anéis de Regeneração estão equipados
        regeneracao = sum(1 for eq in self.equipados if 'Anel de Regeneração' in eq)
        if regeneracao > 0 and self.hp < self.hp_max:
            cura = min(regeneracao, self.hp_max - self.hp)
            self.hp += cura
            print(f"💖 {regeneracao}x Anel de Regeneração restauram {cura} HP.")

    def esta_vivo(self):
        return self.hp > 0

    def exibir_equipamentos(self):
        return " | Equipados: \n\t" + (', \n\t'.join(self.equipados) if self.equipados else "nenhum")

    def status(self):
        status = f"{self.nome} ({self.classe}) - HP: {self.hp}/{self.hp_max} | CA: {self.ac} \n| Inventário: {', '.join(self.inventario)}\n"
        status += self.exibir_equipamentos()
        if self.invisivel:
            status += " | Invisível"
        efeitos_visiveis = [f"{k}({v})" for k, v in self.efeitos_ativos.items() if not k.startswith('valor_')]
        if efeitos_visiveis:
            status += "\n | Efeitos: " + ', '.join(efeitos_visiveis)
        return status

    def calcular_poder_magico_total(self):
        poder = self.ataque_bonus  # Base de INT simulada
        bonus_temp = self.bonus_temporario
        poder += bonus_temp

    # Mapear bônus de itens mágicos relevantes
        for item in self.equipados:
            if 'Cajado' in item:
                try:
                    poder += int(item.split('+')[1])  # Cajado de Gelo +X
                    poder += 2  # dano fixo do cajado
                except:
                    pass
            elif 'Orbe Mental de Vecna' in item:
                try:
                    poder += int(item.split('+')[1])
                    poder += 1  # dano base do Orbe
                except:
                    pass

        # Amplificação do Orbe de Vecna (15% de bônus final)
        if any('Orbe Mental de Vecna' in eq for eq in self.equipados):
            amplificado = int(poder * 1.15)
            print(f"👁️ O Orbe de Vecna amplifica seu poder mágico em +15%: {poder} ➜ {amplificado}")
            return amplificado
        return poder
           

class Inimigo:
    def __init__(self, nome, hp, ac, ataque_bonus, dano_lados, pos):
        self.nome = nome
        self.hp = self.hp_max = hp
        self.ac = ac
        self.ataque_bonus = ataque_bonus
        self.dano_lados = dano_lados
        self.pos = pos
        self.efeitos_ativos = {}  

    def processar_efeitos(self):
        """Aplica DoTs no início do turno do inimigo."""
        remover = []
        for efeito, dados in list(self.efeitos_ativos.items()):
            if isinstance(dados, dict) and 'dano' in dados:
                dano = dados['dano']
                self.hp -= dano
                print(f"☠️ {self.nome} sofre {dano} de dano por {efeito}!")
                dados['turnos'] -= 1
                if dados['turnos'] <= 0:
                    remover.append(efeito)
        for efeito in remover:
            del self.efeitos_ativos[efeito]

    def atacar(self, alvo):
        if getattr(alvo, 'invisivel', False):
            if getattr(self, 'bloqueia_fuga', False) or self.nome == "Olho de Vecna":
                print(vecna_meets), time.sleep(1)
                print(f"👁️ {self.nome} ignora sua invisibilidade! Ele vê sua alma em chamas.")
            else:
                print(f"🕵️‍♂️ {alvo.nome} está invisível! {self.nome} não ataca.")
                return

        rolagem = rolar_dado(20)
        total = rolagem + self.ataque_bonus
        if rolagem == 20:
            dano = rolar_dado(self.dano_lados) * 2
            alvo.hp -= dano
            print(f"💫 ACERTO CRÍTICO de {self.nome} causando {dano}!")
        elif total >= alvo.ac:
            dano = rolar_dado(self.dano_lados)
            alvo.hp -= dano
            print(f"💫 {self.nome} causa {dano} de dano!")
        else:
            print(f"{self.nome} erra o ataque.")

    def esta_vivo(self):
        return self.hp > 0
    
class InimigoEspecial(Inimigo):
    def __init__(self, nome, hp, ac, ataque_bonus, dano_lados, pos, tipo="comum", magia=False):
        super().__init__(nome, hp, ac, ataque_bonus, dano_lados, pos)
        self.tipo = tipo
        self.magia = magia
        self.efeitos_ativos = {}  # <--- Adicione isso

    def processar_efeitos(self):
        """Aplica DoTs no início do turno do inimigo."""
        remover = []
        for efeito, dados in list(self.efeitos_ativos.items()):
            if isinstance(dados, dict) and 'dano' in dados:
                dano = dados['dano']
                self.hp -= dano
                print(f"☠️ {self.nome} sofre {dano} de dano por {efeito}!")
                dados['turnos'] -= 1
                if dados['turnos'] <= 0:
                    remover.append(efeito)
        for efeito in remover:
            del self.efeitos_ativos[efeito]

    def atacar(self, alvo):
        if getattr(alvo, 'invisivel', False):
            print(f"🕵️‍♂️ {alvo.nome} está invisível! {self.nome} não ataca.")
            return

        if self.magia and random.random() < 0.3:
            dano = rolar_dado(10) + 5
            alvo.hp -= dano
            print(f"🔥 {self.nome} lança uma rajada sombria mágica e causa {dano} de dano!")
        else:
            super().atacar(alvo)

class OlhoDeVecna(InimigoEspecial):
    def __init__(self, pos):
        super().__init__(
            nome="Olho de Vecna",
            hp=250,
            ac=45,
            ataque_bonus=33,
            dano_lados=35,
            pos=pos,
            tipo="lendário",
            magia=True
        )
        self.bloqueia_fuga = True  # Garante que não se pode fugir do combate com ele
        self.efeitos_ativos = {}  

    def processar_efeitos(self):
        """Aplica DoTs no início do turno do inimigo."""
        remover = []
        for efeito, dados in list(self.efeitos_ativos.items()):
            if isinstance(dados, dict) and 'dano' in dados:
                dano = dados['dano']
                self.hp -= dano
                print(f"☠️ {self.nome} sofre {dano} de dano por {efeito}!")
                dados['turnos'] -= 1
                if dados['turnos'] <= 0:
                    remover.append(efeito)
        for efeito in remover:
            del self.efeitos_ativos[efeito]

    def atacar(self, alvo):
        # Ignora invisibilidade completamente
        print(vecnas_eye)
        print(f"👁️ {self.nome} vê através de qualquer ilusão.")
        time.sleep(2)
        dano = max(0, random.randint(1, self.dano_lados) + self.ataque_bonus - alvo.ac)
        alvo.hp -= dano
        print(f"{self.nome} causa {dano} de dano a {alvo.nome}!")
    

def combate(jogador, inimigo, inimigo_iniciou=False):

    print(f"\n⚔️ Combate iniciado contra {inimigo.nome}!")
    time.sleep(2)

    def barra_vida(atual, maximo, tamanho=20):
        proporcao = max(atual, 0) / maximo
        cheios = int(proporcao * tamanho)
        vazios = tamanho - cheios
        return f"[{'█' * cheios}{'-' * vazios}] {max(0, atual)}/{maximo}"

    while jogador.esta_vivo() and inimigo.esta_vivo():
        # Exibe o inimigo a cada turno
        if inimigo.nome == 'Goblin':
            print(goblin)
        elif inimigo.nome == 'Esqueleto Armadurado':
            print(skeleton)
        elif inimigo.nome == 'Arqueiro Sombrio':
            print(skull_archer)
        elif inimigo.nome == 'Gárgula de Pedra':
            print(gargula)
        elif inimigo.nome == 'Orc Guerreiro':
            print(warrior_orc)
        elif inimigo.nome == 'Campeão da Morte':
            print(death_champion)
        elif inimigo.nome == 'Dracolich':
            print(dracolich)

        # =====================================================
        # 🌀 PROCESSAR EFEITOS ATIVOS (Jogador e Inimigo)
        # =====================================================
        if hasattr(jogador, "processar_efeitos"):
            jogador.processar_efeitos()
        if hasattr(inimigo, "processar_efeitos"):
            inimigo.processar_efeitos()

        # Se alguém morreu pelos efeitos, encerrar combate
        if not jogador.esta_vivo():
            print(f"☠️ {jogador.nome} sucumbiu aos efeitos!")
            return
        if not inimigo.esta_vivo():
            print(f"🔥 {inimigo.nome} foi derrotado pelos efeitos!")
            return

        # =====================================================
        # ⚡ Inimigo começa o turno
        # =====================================================
        if inimigo_iniciou:
            print(f"⚠️ {inimigo.nome} te ataca primeiro!")
            inimigo.atacar(jogador)
            inimigo_iniciou = False
            if not jogador.esta_vivo():
                print("☠️ Você foi derrotado antes de agir!")
                return

        # =====================================================
        # ⏳ Turno do jogador
        # =====================================================
        jogador.turno_magia()
        jogador.atualizar_efeitos()

        # =====================================================
        # 📊 Mostrar status atualizado
        # =====================================================
        print(f"\n❤️ {jogador.nome}:  {barra_vida(jogador.hp, jogador.hp_max)}")
        print(f"🛡️  {inimigo.nome}: {barra_vida(inimigo.hp, inimigo.hp_max)}")
        print(f"🎽 Equipamentos: {jogador.exibir_equipamentos()}")

        # =====================================================
        # 🎮 Escolher ação
        # =====================================================
        print("\nAções disponíveis:")
        print("1 - Atacar")
        if jogador.classe == "Mago":
            print("2 - Usar Magia")
        print("3 - Usar Item")
        print("4 - Tentar Fugir")
        acao = input("Escolha sua ação: ")

        if acao == '1':
            jogador.atacar(inimigo)

        elif acao == '2' and jogador.classe == "Mago":
            jogador.usar_magia(inimigo)

        elif acao == '3':
            jogador.usar_pocao()

        elif acao == '4':
            if getattr(inimigo, 'bloqueia_fuga', False):
                print("🧿 A Escadaria Ancestral foi selada! Fugir é impossível!")
                time.sleep(2)
                inimigo.atacar(jogador)
                time.sleep(2)
                continue

            chance_base = 0.3
            if jogador.classe == "Ladino":
                chance_base = 0.5
            elif jogador.classe == "Mago":
                chance_base = 0.3
            elif jogador.classe == "Guerreiro":
                chance_base = 0.2

            rolagem = random.random()
            print(f"🏃 Tentando fugir... (chance de {int(chance_base * 100)}%)")
            time.sleep(1)

            if rolagem < chance_base:
                print("✅ Você conseguiu fugir do combate!")
                time.sleep(1)

                # 33% de chance de ganhar um item
                if random.random() < 0.33:
                    item = random.choice(['poção de cura', 'poção de força', 'poção de invisibilidade'])
                    jogador.inventario.append(item)
                    print(f"🎁 Ao fugir, você encontra um item caído: {item}!")
                    time.sleep(2)

                # 33% de chance de perder um item
                if jogador.inventario and random.random() < 0.33:
                    perdido = random.choice(jogador.inventario)
                    jogador.inventario.remove(perdido)
                    print(f"💨 Na pressa, você perde um item: {perdido}!")
                return  # Fim do combate com sucesso
            else:
                print("❌ Falha na fuga! Você perde seu turno.")
        else:
            print("❌ Ação inválida!")
            continue

        # =====================================================
        # ⚔️ Ataque do inimigo no fim do turno
        # =====================================================
        time.sleep(1)
        if inimigo.esta_vivo():
            inimigo.atacar(jogador)
            time.sleep(1)


# --------------------------- MAPA E GERADOR ----------------------------

class Mapa:
    def __init__(self, largura=4, altura=4, dificuldade=1):
        self.largura = largura
        self.altura = altura
        self.matriz = [['#' for _ in range(largura)] for _ in range(altura)]
        self.inimigos = []
        self.itens = {}
        self.portas = {}         # Novas estruturas
        self.escadas = set()
        self.escada_final = None  # Escada especial que leva ao chefe
        self.estruturas = {}
        self.gerar_labirinto(dificuldade)


    def gerar_labirinto(self, dificuldade):
        # Geração do terreno
        for y in range(self.altura):
            for x in range(self.largura):
                borda = x in [0, self.largura - 1] or y in [0, self.altura - 1]
                if random.random() < (0.30 if borda else 0.12):
                    self.matriz[y][x] = '#'
                else:
                    self.matriz[y][x] = '.'

        tipo_andar = random.choices(
            population=["normal", "vazio", "armadilhas", "elite", "tesouro"],
            weights=[0.6, 0.1, 0.1, 0.1, 0.1],
            k=1
        )[0]

        if tipo_andar == "vazio":
            print("🌫️ Um andar vazio e silencioso...")
            return

        elif tipo_andar == "armadilhas":
            print("⚠️ Armadilhas cobrem o chão desta sala.")
            armadilhas_possiveis = ['espinhos', 'flechas', 'bomba mágica']
            for _ in range(random.randint(3, 6)):
                x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
                if self.matriz[y][x] == '.':
                    tipo = random.choice(armadilhas_possiveis)
                    self.estruturas[(x, y)] = f"armadilha_{tipo}"
            return

        elif tipo_andar == "elite":
            print("👹 Uma presença poderosa domina este andar...")
            x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
            if self.matriz[y][x] == '.':
                if dificuldade >= 23 and random.random() < 0.5:
                    self.inimigos.append(InimigoEspecial(
                        "Dracolich", 32 + dificuldade * 3, 17 + dificuldade,
                        10 + dificuldade // 2, 12, (x, y), tipo='lendário', magia=True
                    ))
                else:
                    if dificuldade >= 13 and random.random() < 0.5:
                        self.inimigos.append(InimigoEspecial(
                            "Campeão da Morte", 27 + dificuldade * 3, 17 + dificuldade,
                            8 + dificuldade // 2, 10, (x, y), tipo="elite", magia=True
                        ))
                return

        elif tipo_andar == "tesouro":
            itens_possiveis = [
                'poção de cura', 'poção de força', 'poção de invisibilidade',
                f'Elixir do Berserker +{1 + dificuldade // 2}',
                f'Orbe de Proteção +{1 + dificuldade // 2}',
                f'Anel da Vitalidade +{1 + dificuldade // 2}',
                f'Lâmina Sombria +{1 + dificuldade // 2}',
                f'Arco Élfico +{1 + dificuldade // 2}',
                f'Armadura de Mithril +{1 + dificuldade // 2}',
                f'Machado Anão Flamejante +{1 + dificuldade // 2}',
                f'Elmo da Fúria +{1 + dificuldade // 2}',
                'Botas do Silêncio',
                f'Cajado de Gelo +{1 + dificuldade // 2}',
                'Tomo de Sabedoria Antiga',
                'chave',
                f'Amuleto de Resistência +{1 + dificuldade // 2}',
                'Anel de Regeneração',
                f'Manoplas do Trovão +{1 + dificuldade // 2}',
                f'Orbe Mental de Vecna + {1 + dificuldade // 2}'
            ]
            
            for _ in range(random.randint(6, 10)):
                x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
                if self.matriz[y][x] == '.' and (x, y) not in self.itens:
                    self.itens[(x, y)] = random.choice(itens_possiveis)
            return

        # Andar normal (inimigos + itens)
        if random.random() < 0.65:
            # A quantidade de inimigos aumenta conforme a dificuldade
            qtd_inimigos = random.randint(1, 2 + dificuldade // 4)

            # Definição de inimigos comuns com pesos
            inimigos_comuns = [
                ("Goblin", 7 + rolar_dado(5) + dificuldade,
                10 + dificuldade // 3, 3 + dificuldade // 2,
                5, 50),  # 50% de chance
                ("Esqueleto Armadurado", 12 + rolar_dado(7) + dificuldade,
                12 + dificuldade, 6 + dificuldade // 2,
                3, 35),  # 35% de chance
                ("Arqueiro Sombrio", 9 + rolar_dado(5) + dificuldade,
                11 + dificuldade // 2, 5 + dificuldade,
                6, 30)   # 30% de chance
            ]

            # Definição de inimigos raros com pesos
            inimigos_raros = [
                ("Orc Guerreiro", 19 + rolar_dado(7) + dificuldade,
                12 + dificuldade // 3, 6 + dificuldade // 2,
                8, 15),  # 15% de chance
                ("Gárgula de Pedra", 22 + rolar_dado(7) + dificuldade * 2,
                14 + dificuldade, 8 + dificuldade // 2,
                4, 10)   # 10% de chance
            ]

            # Escolher inimigos para o andar
            for _ in range(qtd_inimigos):
                x, y = random.randint(0, self.largura - 1), random.randint(0, self.altura - 1)
                if self.matriz[y][x] == '.':
                    # Se a dificuldade for alta, considerar raros
                    if dificuldade >= 15 and random.random() < 0.20:
                        nomes, hps, acs, danos, esquivas, pesos = zip(*inimigos_raros)
                        escolha = random.choices(list(zip(nomes, hps, acs, danos, esquivas)), weights=pesos)[0]
                        nome, hp, ac, dano, esquiva = escolha
                        self.inimigos.append(InimigoEspecial(nome, hp, ac, dano, esquiva, (x, y), tipo='raro'))
                    else:
                        nomes, hps, acs, danos, esquivas, pesos = zip(*inimigos_comuns)
                        escolha = random.choices(list(zip(nomes, hps, acs, danos, esquivas)), weights=pesos)[0]
                        nome, hp, ac, dano, esquiva = escolha
                        self.inimigos.append(Inimigo(nome, hp, ac, dano, esquiva, (x, y)))

        # Itens padrão
        itens_possiveis = [
            'poção de cura', 'poção de força', 'poção de invisibilidade',
            f'Elixir do Berserker +{1 + dificuldade // 2}',
            f'Orbe de Proteção +{1 + dificuldade // 2}',
            f'Anel da Vitalidade +{1 + dificuldade // 2}',
            f'Lâmina Sombria +{1 + dificuldade // 2}',
            f'Arco Élfico +{1 + dificuldade // 2}',
            f'Armadura de Mithril +{1 + dificuldade // 2}',
            f'Machado Anão Flamejante +{1 + dificuldade // 2}',
            f'Elmo da Fúria +{1 + dificuldade // 2}',
            'Botas do Silêncio',
            f'Cajado de Gelo +{1 + dificuldade // 2}',
            'Tomo de Sabedoria Antiga',
            f'Amuleto de Resistência +{1 + dificuldade // 2}',
            'Anel de Regeneração',
            f'Manoplas do Trovão +{1 + dificuldade // 2}',
            f'Orbe Mental de Vecna + {1 + dificuldade // 2}'
        ]

        if random.random() < 0.75:
            quantidade_itens = random.randint(2, 5 + dificuldade)
            for _ in range(quantidade_itens):
                x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
                if self.matriz[y][x] == '.' and (x, y) not in self.itens:
                    self.itens[(x, y)] = random.choice(itens_possiveis)

        # Portas
        if random.random() < 0.6:
            for _ in range(random.randint(1, 2)):
                if random.random() < 0.7:
                    x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
                    if self.matriz[y][x] == '.':
                        self.portas[(x, y)] = random.random() < 0.5

        # Escadas
        if dificuldade >= 33:
            if random.random() < 0.3:  # 30% de chance da escada final surgir em cada andar ≥ 33
                while True:
                    x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
                    if self.matriz[y][x] == '.':
                        self.escada_final = (x, y)
                        break
            else:
                print("⚠️ Você sente que nenhuma saída comum está ativa neste andar...")
        else:
            for _ in range(1):
                x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
                if self.matriz[y][x] == '.':
                    self.escadas.add((x, y))

        # Estruturas especiais e armadilhas visuais
        estruturas_possiveis = ['altar antigo', 'círculo mágico', 'estátua enigmática']
        for _ in range(random.randint(1, 2)):
            x, y = random.randint(1, self.largura - 2), random.randint(1, self.altura - 2)
            if self.matriz[y][x] == '.':
                self.estruturas[(x, y)] = random.choice(estruturas_possiveis)

    def mostrar(self, jogador_pos):
        for y in range(self.altura):
            linha = ''
            for x in range(self.largura):
                if (x, y) == jogador_pos:
                    linha += ' ● '
                elif (x, y) in self.itens:
                    linha += ' ? '
                elif any(i.pos == (x, y) and i.esta_vivo() for i in self.inimigos):
                    linha += ' ! '
                elif (x, y) in self.portas:
                    linha += ' ▓ ' if self.portas[(x, y)] else ' ▒ '
                elif (x, y) == self.escada_final:
                    linha += ' >>'  # Escadaria para o chefe
                elif (x, y) in self.escadas:
                    linha += ' > '
                elif (x, y) in self.estruturas:
                    linha += '+'
                elif self.matriz[y][x] == '#':
                    linha += '███'
                else:
                    linha += ' ▒  '

            print(linha)

    def mover_inimigos(self, jogador_pos, jogador):
        inimigos_que_agiram = set()

        for inimigo in self.inimigos:
            if not inimigo.esta_vivo() or id(inimigo) in inimigos_que_agiram:
                continue

            ix, iy = inimigo.pos
            jx, jy = jogador_pos

            dx = 1 if jx > ix else -1 if jx < ix else 0
            dy = 1 if jy > iy else -1 if jy < iy else 0

            # Primeiro tenta mover na direção mais longa para simular perseguição inteligente
            if abs(jx - ix) > abs(jy - iy):
                novo_x, novo_y = ix + dx, iy
            else:
                novo_x, novo_y = ix, iy + dy

            # Verifica se pode mover e se não colide com o jogador
            if (0 <= novo_x < self.largura and 0 <= novo_y < self.altura and 
                self.matriz[novo_y][novo_x] == '.' and (novo_x, novo_y) != jogador_pos):
                inimigo.pos = (novo_x, novo_y)
                inimigos_que_agiram.add(id(inimigo))

            elif (novo_x, novo_y) == jogador_pos:
                if jogador.invisivel:
                    print(f"👻 {inimigo.nome} parece não notar sua presença.")
                    continue

                print(f"\n⚠️ {inimigo.nome} alcança você!")
                time.sleep(1)
                combate(jogador, inimigo, inimigo_iniciou=True)

                inimigos_que_agiram.add(id(inimigo))

                if not jogador.esta_vivo():
                    return  # jogador morreu, fim da rodada

# ----------------------------- SISTEMA DE JOGO --------------------------

class DungeonGame:
    def __init__(self):
        self.jogador = self.criar_personagem()
        self.andar = 1
        self.mapa = Mapa(dificuldade=self.andar)
        self.x, self.y = self.spawn_jogador()
        self.jogador.pos = (self.x, self.y)

    def spawn_jogador(self):
        while True:
            x, y = random.randint(0, self.mapa.largura - 1), random.randint(0, self.mapa.altura - 1)
            if self.mapa.matriz[y][x] == '.':
                return x, y

    def criar_personagem(self):
        print("\nEscolha sua classe:")
        print("1 - Guerreiro")
        print("2 - Mago")
        print("3 - Ladino")
        while True:
            c = input(">> ")
            if c == '1':
                print(escolhe_guerreiro(warrior)), time.sleep(3)
                return Personagem("Guerreiro", 25, 16, 6, 8, "Guerreiro", 6, 8)
            elif c == '2':
                print(escolhe_mago(wizard)), time.sleep(3)
                return Personagem("Mago", 19, 12, 3, 10, "Mago", 3, 10)
            elif c == '3':
                print(escolhe_ladino(rogue)), time.sleep(3)
                return Personagem("Ladino", 21, 14, 9, 6, "Ladino", 9, 6)

    def jogar(self):
        limpar_tela()
        print("🎮 Bem-vindo à Masmorra do Olho de Vecna!")
        while self.jogador.esta_vivo():
            self.jogador.turno_magia()
            self.jogador.atualizar_efeitos()
            self.mapa.mostrar((self.x, self.y))
            print(self.jogador.status() + f"\n| Nível: {self.andar}")
            cmd = input("\nComando (mover-w/a/s/d/ Inventário-e/ | sair/): ").lower()

            if cmd in ['w', 'a', 's', 'd']:
                dx, dy = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}[cmd]
                nx, ny = self.x + dx, self.y + dy

                if nx < 0 or ny < 0 or nx >= self.mapa.largura or ny >= self.mapa.altura:
                    print(avanca_dungeon(dungeon, dungeon2, dungeon3, lost_garden))
                    print("🕽️ Você avança na masmorra...")
                    time.sleep(2)
                    self.andar += 1
                    nova_mapa = Mapa(dificuldade=self.andar)

                    if dx == -1:
                        new_x = nova_mapa.largura - 1
                        new_y = self.y
                    elif dx == 1:
                        new_x = 0
                        new_y = self.y
                    elif dy == -1:
                        new_y = nova_mapa.altura - 1
                        new_x = self.x
                    elif dy == 1:
                        new_y = 0
                        new_x = self.x
                    else:
                        new_x, new_y = self.spawn_jogador()

                    if nova_mapa.matriz[new_y][new_x] != '.':
                        new_x, new_y = self.spawn_jogador()

                    self.mapa = nova_mapa
                    self.x, self.y = new_x, new_y
                    self.jogador.pos = (self.x, self.y)

                elif (nx, ny) in self.mapa.portas:
                    if self.mapa.portas[(nx, ny)]:
                        if 'chave' in self.jogador.inventario:
                            usar = input("🔐 Porta trancada! Usar chave? (s/n) ").lower()
                            if usar == 's':
                                self.jogador.inventario.remove('chave')
                                self.mapa.portas[(nx, ny)] = False
                                print("✅ Você destranca a porta.")
                                self.x, self.y = nx, ny
                                self.jogador.pos = (self.x, self.y)
                        else:
                            print("🚪 Porta trancada! Você precisa de uma chave.")
                    else:
                        print("🚪 Você atravessa uma porta.")
                        self.x, self.y = nx, ny
                        self.jogador.pos = (self.x, self.y)

                elif self.mapa.matriz[ny][nx] == '.':
                    self.x, self.y = nx, ny
                    self.jogador.pos = (self.x, self.y)

                    if (self.x, self.y) in self.mapa.itens:
                        item = self.mapa.itens.pop((self.x, self.y))
                        self.jogador.inventario.append(item)
                        print(f"🎁 Você encontrou um item: {item}!")

                    for inimigo in self.mapa.inimigos:
                        if inimigo.pos == (self.x, self.y):
                            if self.jogador.invisivel:
                                if isinstance(inimigo, OlhoDeVecna):
                                    print("🧿 O Olho de Vecna ignora sua invisibilidade e a dissipa no mesmo instante!")
                                    self.jogador.invisivel = False
                                else:
                                    print("👻 Você passa despercebido pelo inimigo graças à invisibilidade.")
                                    continue

                            chance_combate = 1.0
                            if 'Botas do Silêncio' in self.jogador.equipados:
                                chance_combate = 0.4  # 60% de chance de evitar combate

                            if random.random() > chance_combate:
                                print("👟 Você passa silenciosamente e evita o combate!")
                                break

                            combate(self.jogador, inimigo)
                            self.mapa.inimigos = [i for i in self.mapa.inimigos if i.esta_vivo()]
                            break

                    if (self.x, self.y) == self.mapa.escada_final:
                        time.sleep(2)
                        print("👁️ A escadaria ancestral treme com energia profana...")
                        time.sleep(4) 
                        print(vecna_sees_everything), time.sleep(4)
                        print(vecna_meets), time.sleep(4)
                        print(vecnas_eye), time.sleep(2)
                        print("💀 No centro da sala flutua o Olho de Vecna, em sua forma mais pura e aterradora!")
                        chefe_final = OlhoDeVecna((self.x, self.y))
                        combate(self.jogador, chefe_final)

                        if self.jogador.esta_vivo():
                            print("\n🌟 Você derrotou o Olho de Vecna!"), time.sleep(3)
                            print("🏆 A maldição que assolava a masmorra começa a se dissipar..."), time.sleep(3)
                            print("🎉 Parabéns, você venceu a aventura!"), time.sleep(3)
                        else:
                            print("\n💀 O Olho de Vecna consome sua alma... o mal prevalece."), time.sleep(3)
                        exit()

                    elif (self.x, self.y) in self.mapa.escadas:
                        if self.andar >= 33:
                            print("🔒 Uma escada antiga... mas parece ter sido destruída. Não leva a lugar algum.")
                            time.sleep(1)
                            return
                        print(stairway)
                        print("🌀 Você encontra uma escada e desce para o próximo andar...")
                        time.sleep(1)
                        self.andar += 1
                        self.mapa = Mapa(dificuldade=self.andar)
                        self.x, self.y = self.spawn_jogador()
                        self.jogador.pos = (self.x, self.y)

                    elif (self.x, self.y) in self.mapa.estruturas:
                        estrutura = self.mapa.estruturas[(self.x, self.y)]

                        if estrutura.startswith("armadilha_"):
                            tipo = estrutura.split('_')[1]
                            dano = random.randint(1, 2)
                            self.jogador.hp = max(0, self.jogador.hp - dano)
                            print(f"⚠️ Você ativou uma armadilha de {tipo} e sofreu {dano} de dano!")
                            del self.mapa.estruturas[(self.x, self.y)]
                            if not self.jogador.esta_vivo():
                                print("☠️ Você foi morto por uma armadilha!")
                                break
                        else:
                            print(f"🔮 Você encontra {estrutura}!")
                            time.sleep(2)
                            if estrutura == 'altar antigo':
                                print(altar)
                                time.sleep(4)
                                cura = rolar_dado(6) + 4
                                self.jogador.hp = min(self.jogador.hp + cura, self.jogador.hp_max)
                                print(f"🧎 Você ora e recupera {cura} HP!")
                            elif estrutura == 'círculo mágico':
                                if self.jogador.classe == "Mago":
                                    self.jogador.cooldown_magia = 0
                                    self.jogador.ataque_bonus += 3
                                    print(magic_circle)
                                    time.sleep(1)
                                    print(magic_circle_blink)
                                    time.sleep(1)
                                    print(magic_circle)
                                    time.sleep(1)
                                    print(magic_circle_blink)
                                    time.sleep(1)
                                    print(magic_circle)
                                    print("✨ Suas energias arcanas são restauradas, e seu poder aumenta +3 INT (ataque mágico)!")
                                else:
                                    print(magic_circle)
                                    print("❓ Você não sabe o que fazer aqui.")
                                    time.sleep(2)
                            elif estrutura == 'estátua enigmática':
                                print(statue), time.sleep(2)
                                if random.random() < 0.5:
                                    print(statue), time.sleep(2)
                                    print("🧿 A estátua o observa... e desaparece. Um item surge!")
                                    time.sleep(2)
                                    item = random.choice(['poção de cura', 'chave'])
                                    self.jogador.inventario.append(item)
                                    print(f"🎁 Você recebe: {item}")
                            del self.mapa.estruturas[(self.x, self.y)]
                else:
                    print(wall)
                    print("🚫 Parede ou fora do mapa!")

            elif cmd == 'e':
                self.jogador.usar_pocao()

            elif cmd == 'sair':
                print("🛑 Fim da aventura.")
                break

            self.mapa.mover_inimigos((self.x, self.y), self.jogador)

        if not self.jogador.esta_vivo():
            print("☠️ Você tombou na masmorra... o Olho de Vecna permanece oculto.")
            time.sleep(3)



# ----------------------------- EXECUÇÃO ----------------------------------
if __name__ == "__main__":
    DungeonGame().jogar()

