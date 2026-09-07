import sqlite3

DB = "database.db"

links = {
    "Cuscuizeiro": "https://shopee.com.br/Cuscuzeiro-Crema-16cm-i.210928301.18293019283",

    "Descanso Tampas de Panela": "https://shopee.com.br/Descanso-De-Panela-Suporte-Tampas-De-Panelas-Talheres-E-Acess%C3%B3rios-Organizador-Porta-Tempero-Cozinha-i.1131571856.23198681301",

    "Escorredor de Louça": "https://shopee.com.br/Escorredor-de-Lou%C3%A7a-Duplo-Multifuncional-Suporte-para-Pratos-Talheres-e-T%C3%A1bua-de-Corte-i.1601750095.23794415375",

    "Garrafa Térmica": "https://shopee.com.br/Garrafa-T%C3%A9rmica-N%C3%B3rdica-1-Litro-Caf%C3%A9-Ch%C3%A1-Bule-Cabo-Madeira-Mesa-Posta-Bot%C3%A3o-Fixa-Temperatura-Wood-1L-i.625510592.22493251687",

    "Garrafas de Vidro": "https://shopee.com.br/search?keyword=2%20garrafas%20de%20vidro%201L",

    "Geladeira": "https://shopee.com.br/search?keyword=geladeira",

    "Ilha Bancada": "https://shopee.com.br/search?keyword=ilha%20bancada%20cozinha",

    "Jogo de Copos": "https://shopee.com.br/Jogo-6-Copos-Luxo-Suco-Agua-Refrigerante-Aruba-Fum%C3%AA-465ml-i.618718566.22698032343",

    "Jogo de Pratos": "https://shopee.com.br/Kit-6-Pratos-Rasos-de-Porcelana-Branca-26-5cm-Germer-Mesa-Posta-Diamante-i.1284860786.18299590094",

    "Jogo Faqueiro": "https://shopee.com.br/search?keyword=jogo%20faqueiro%2025%20pecas%20nude",

    "Kit de Panelas": "https://shopee.com.br/Jogo-de-Panelas-Antiaderente-13-Pe%C3%A7as-Preto-com-Teflon-Tampa-de-Vidro-com-Op%C3%A7%C3%B5es-cor-Vermelho-Preto-i.1669534330.58200516233",

    "Liquidificador": "https://shopee.com.br/Liquidificador-Mondial-Turbo-Power-L-99-3-Velocidades-550W-220V-i.1078343995.22297014624",

    "Panela de Pressão": "https://shopee.com.br/Panela-de-Press%C3%A3o-4-5L-Cer%C3%A2mica-Moderna-Fog%C3%A3o-Indu%C3%A7%C3%A3o-Antiaderente-Fechamento-Externo-i.958447403.44760160595",

    "Porta Temperos": "https://shopee.com.br/search?keyword=porta%20temperos%205%20pecas",

    "Pote Dispenser": "https://shopee.com.br/Pote-Dispenser-Multiuso-1200ml-sabao-em-po-liquido-plastico-i.369179570.22998781654",

    "Potes de Vidro": "https://shopee.com.br/Kit-3-Potes-de-Vidro-Herm%C3%A9tico-com-Trava-Metal-750ml-1-33L-1-78L-i.384207446.53055642480",

    "Potes Organizadores": "https://shopee.com.br/Kit-Organizadores-Potes-Herm%C3%A9ticos-Acr%C3%ADlico-Livre-BPA-Para-Mantimentos-Cozinha-Geladeira-Arm%C3%A1rio-i.577692913.23096097453",

    "Sanduicheira": "https://shopee.com.br/search?keyword=sanduicheira%20britania%20antiaderente",

    "Tábua de Churrasco": "https://shopee.com.br/Tabua-de-Carne-Churrasco-Grande-i.225023451.23591170856",

    "Taça de Sobremesa": "https://shopee.com.br/Ta%C3%A7a-de-Sobremesa-Vidro-Canelado-Coupe-Kit-6-Ta%C3%A7as-para-Sorvete-Mousse-Pav%C3%AA-Cheesecake-i.1360529796.58256634767",

    "Triturador de Alho": "https://shopee.com.br/search?keyword=triturador%20de%20alho",

    # SALA
    "Cortina": "https://shopee.com.br/Cortina-Luxo-Para-Sala-4-00m-X-2-60m-em-Voil-com-Forro-de-Microfibra-Para-Var%C3%A3o-Simples-Decorativa-i.380127357.8069947197",

    "Painel Sala": "https://shopee.com.br/search?keyword=painel%20sala%20tv%2050",

    "Suporte Controle": "https://shopee.com.br/Suporte-Para-Controle-Remoto-Transparente-acrilico-i.456992476.23893571893",

    "Tapete Sala": "https://shopee.com.br/Tapete-Sala-2-00-x-1-50-F%C3%A1cil-de-limpar-i.296363855.7097861670",

    # QUARTO
    "Edredom": "https://shopee.com.br/Edredom-Casal-Queen-400-Fios-Dupla-Face-2-40x2-20-Tecido-Liso-Varias-Cores-i.410424657.28564207442",

    "Guarda Roupas": "https://shopee.com.br/search?keyword=guarda%20roupas",

    "Jogos de Lençóis": "https://shopee.com.br/Jogo-de-lencol-Casal-Padr%C3%A3o-Box-400-fios-Macio-i.313660590.20498131325",

    "Sapateira": "https://shopee.com.br/search?keyword=sapateira%20buenos%20aires%203%20portas",

    # BANHEIRO
    "Gabinete Armário Banheiro": "https://shopee.com.br/search?keyword=gabinete%20armario%20banheiro",

    "Jogo de Toalhas": "https://shopee.com.br/Jogo-de-Toalha-4-Pe%C3%A7as-Karsten-100-Algod%C3%A3o-2-Banho-2-Rosto-Excelente-Absor%C3%A7%C3%A3o-Felpuda-Macia-i.322387387.58200167629",

    "Kit Banheiro": "https://shopee.com.br/Kit-Banheiro-4-Pecas-Luxo-Aco-Inox-Quadrado-Preto-Fosco-i.733802613.22692673303",

    "Tapete para Banheiro": "https://shopee.com.br/Jogo-de-Tapete-Para-Banheiro-Kit-com-3-Pe%C3%A7as-Antiderrapante-Emborrachado-Resistente-i.1408279146.23593597115",

    # LAVANDERIA
    "Kit Organizador": "https://shopee.com.br/Kit-Organizadores-Potes-Herm%C3%A9ticos-Acr%C3%ADlico-Livre-BPA-Para-Mantimentos-Cozinha-Geladeira-Arm%C3%A1rio-i.577692913.23096097453",

    "Varal de Chão": "https://shopee.com.br/Varal-de-Ch%C3%A3o-3-Andares-Dobr%C3%A1vel-com-Rodinhas-i.1489462783.23799133359",

    "Vassoura Mágica": "https://shopee.com.br/Vassoura-Magica-Rodo-MOP-2-em-1-Vassoura-Rodo-M%C3%A1gico-Multifuncional-i.329256756.18036405157",
}


conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("\nATUALIZANDO LINKS...\n")

atualizados = 0
nao_encontrados = 0

for nome, link in links.items():

    cursor.execute(
        "SELECT id, nome FROM presentes WHERE nome = ?",
        (nome,)
    )

    produto = cursor.fetchone()

    if produto:
        cursor.execute(
            """
            UPDATE presentes
            SET link = ?
            WHERE id = ?
            """,
            (link, produto[0])
        )

        print(f"OK: {nome}")
        atualizados += 1

    else:
        print(f"NAO ENCONTRADO NO BANCO: {nome}")
        nao_encontrados += 1


conn.commit()
conn.close()

print("\n--------------------------------")
print(f"Links atualizados: {atualizados}")
print(f"Produtos não encontrados: {nao_encontrados}")
print("--------------------------------")
print("\nPronto!")