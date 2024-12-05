import mysql.connector
from Produto import Produto

user = "root"
senha = ""
host = "localhost"
banco = "lanchonete"

#retorna a conexao
def conectar():
    conexao=None
    try:
        conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=senha,
        database=banco
    )
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o BD:{e}")

    return conexao

def fechar_conecxao(conexao):
    if conexao.is_connected():
        conexao.close()
        print("Conexão com o BD encerrado")

# - Criar um novo registro no banco de dados
def inserir(conexao, produto):

    try:
        cursor = conexao.cursor()
        query = "INSERT INTO produto(descricao, preco, qtd) VALUES(%s, %s, %s)"
        cursor.execute(query,(produto.descricao,produto.preco,produto.qtd))
        conexao.commit()
        print(f"{produto.descricao} Registrado como sucesso!")

    except mysql.connector.Error as e:
        print(f"Erro ao inserir produto:{e}")
    finally:
        cursor.close()

# R - Read listar todas asinfomações da tabela
def listar(conexao): 
    listaProduto=[]
    try:
        cursor = conexao.cursor()
        query = "Select * from produto"
        cursor.execute(query)
        registros = cursor.fetchall()
        for registro in registros:
            objeto = Produto(*registro)
            listaProduto.append(objeto)

    except mysql.connector.Error as e:
        print(f"Erro ao listar produtos:{e}")
    finally:
        cursor.close()
    return listaProduto

#U - update atualizar uma informação de uma linha
def update(conexao, idProduto, preco, qtd):
    try:
        cursor= conexao.cursor() 
        query = "UPDATE produto set preco=%s, qtd=%s WHERE cod=%s"
        cursor.execute(query, (preco, qtd, idProduto))
        conexao.commit()
        print(f"{idProduto} atualizado com sucesso!")
        
    except mysql.connector.Error as e:
        print(f"Erro ao atualizar produto:{e}")
    finally:
        cursor.close()


#deletar uma linha a partir de um id
def delete(conexao,idProduto):
    try:
        cursor= conexao.cursor() 
        query = "DELETE FROM produto WHERE cod=%s"
        cursor.execute(query,(idProduto,))
        conexao.commit()
        print(f"{idProduto} Excluído!")

    except mysql.connector.Error as e:
        print(f"Erro ao excluir produto:{e}")
    finally:
        cursor.close()

#buscar infomaçoes de uma lihna
def buscar(conexao, busca): 
    listaProduto=[]
    try:
        cursor= conexao.cursor() 
        query ="Select * from produto where descricao like %s"
        cursor.execute(query,("%"+busca+"%",))
        registros = cursor.fetchall()
        for produto in registros:
            objeto = Produto(*produto)
            listaProduto.append(objeto)

    except mysql.connector.Error as e:
        print(f"Erro ao buscar produto:{e}")
    finally:
        cursor.close()

    return listaProduto

#Main
conexao = conectar()

if conexao!=None:
    print("Conectado com Banco de Dados")

    novo_produto = Produto(parCod=None,parDescricao="X - Salada",
                            parPreco=15,parQtd=3)
    #inserir(conexao,novo_produto)
    #update(conexao,0,16,2)
    #delete(conexao,0)
    #listar(conexao)
    #buscar(conexao, "X")
    produtos = listar(conexao)
    for produto in produtos:
        produto.listar()

    produtos = buscar(conexao, "mkd")
    if produtos!=[]:
        for produto in produtos:
            produto.listar()
    else:
        print("Nenhum produto encontrado!")

        
    fechar_conecxao(conexao)




