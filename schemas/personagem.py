def personagemEntidade(db_item) -> dict:
    return {
        "id"    : str(db_item['_id']),
        "nome"  : db_item['nome'],
        "classe": db_item['classe'],
        "raca"  : db_item['raca'],
        "pv_max": db_item['pv_max'],
        "pv_num": db_item['pv_num'],
        "pe_max": db_item['pe_max'],
        "pe_num": db_item['pe_num'],
        "gold"  : db_item['gold']
    }

def listaPersonagensEntidade(db_item_lista) -> list:
    lista_personagens = []
    for item in db_item_lista:
        lista_personagens.append(personagemEntidade(item))
    return lista_personagens