#Importanto bibliotecas
from ply.lex import lex
from ply.yacc import retornaQuantErros, yacc

import re
import PySimpleGUI as sg

#Variável de Controle do Token Invalido
g_token_invalido = ""

#Lista de Tokens
tokens = ('COMENTARIO', 'VALOR_TEXTO','IFSULDEMINAS','TIPO_VAR', 'VAR', 'VAR_SENSOR', 'OPER_RELA', 'OPER_MATEMATICO',
        'OPER_ATRIB','OPER_LOGICO', 'COND_SE', 'COND_SENAO', 'COND_SENAOSE', 'REP_PARA',
        'REP_ENQUANTO', 'TENTAR', 'CASO_ERRO', 'NOME_FUNCAO', 'DEFINE_FUNCAO', 'VALOR_LOGICO',
        'VALOR_INTEIRO', 'VALOR_REAL', 'VALOR_DATA','VALOR_HORARIO',
        'ABRE_PARENT', 'FECHA_PARENT', 'ABRE_CHAVES', 'FECHA_CHAVES','PONTO_FINAL', 'VIRGULA',
        'TEXTO_MAL_FORMADO')

# REGEX DE CADA TOKEN
t_COMENTARIO = r'(\[[^"]*\])'
t_VALOR_TEXTO = r'("[^"]*")|(\'[^\']*\')'
t_IFSULDEMINAS = r'IFSULDEMINAS'
t_TIPO_VAR = r'~numero_inteiro | ~texto | ~porcentagem | ~temperatura | ~numero_real | ~booleano | ~lista | ~tempo | ~data'
t_VAR = r'\#[A-z0-9\_]+'
t_VAR_SENSOR = r'VELOCIDADE | NIVEL_TANQUE | MARCHA | TEMPERATURA | DISTANCIA_TRAS | DISTANCIA_FRENTE | POSICAO_VIDROS | VIDA_UTIL_PNEUS | ACELERADOR | FREIO | EMBREAGEM | DATA_ATUAL | HORA_ATUAL | POSICAO_DIRECAO'
t_OPER_RELA = r'<= | >= | < | > |  = | !='
t_OPER_MATEMATICO = r'\+|-|\/|\*'
t_OPER_ATRIB = r':='
t_OPER_LOGICO = r'E|OU'
t_COND_SE = r'se'
t_COND_SENAO = r'senao'
t_COND_SENAOSE = r'senaose'
t_REP_PARA = r'para'
t_REP_ENQUANTO = r'enquanto'
t_TENTAR = r'tentar'
t_CASO_ERRO = r'caso_erro'
t_NOME_FUNCAO = r'!([a-zA-Z][a-zA-Z0-9]+)'
t_DEFINE_FUNCAO = r'define_funcao'
t_VALOR_LOGICO = r'Verdadeiro|Falso'
t_VALOR_INTEIRO = r'\b(\d+)\b'
t_VALOR_REAL = r'(\d+)\.(\d+)'
t_VALOR_DATA = r'[0-3][0-9]\/[0-1][0-9]\/[0-9][0-9][0-9][0-9]'
t_VALOR_HORARIO = r'[0-9][0-9]:[0-9][0-9]'
t_ABRE_PARENT = r'\('
t_FECHA_PARENT = r'\)'
t_ABRE_CHAVES = r'\{'
t_FECHA_CHAVES = r'\}'
t_PONTO_FINAL = r'\.'
t_VIRGULA = r','
t_TEXTO_MAL_FORMADO = r'("[^"]*)|(\'[^\']*)'

# TOKENS que devem ser ignorados
t_ignore = ' \t'

def constroiTokenInvalido(token):
    global g_token_invalido
    g_token_invalido = g_token_invalido + token
    
def t_error(token):
    constroiTokenInvalido(token.value[0])
    token.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

###-------#####
# Classe do Analisador Léxico
###-------#####
def AnalisadorLexico():
    return lex()

###-------#####
# Função para Tratar Tokens Inválidos
###-------#####
def verificaErroTokenInvalido(token_invalido):
    if g_token_invalido[0] in ('1','2','3','4','5','6','7','8','9'):
        return (f"Número não identificado! Token: {g_token_invalido}")

    else:
        return (f"Caractere ou sequência de caracteres não reconhecido(s) na linguagem: {g_token_invalido}")    

###---------####
# Analisador Sintático
###--------####

# Gramática
def p_statements_multiple(p):
    '''
    statements : statements statement
    '''

def p_statements_single(p):
    '''
    statements : statement
    '''

def p_comentarios(p):
    '''
    statement : COMENTARIO
    '''

def p_regra_ifsuldeminas(p):
    '''
    statement : IFSULDEMINAS PONTO_FINAL
    '''

###-------#####
# Regras para Expressões Matemáticas
###-------#####
def p_expressao_numero(p):
    '''
    expr : VALOR_INTEIRO
        | VALOR_REAL
    '''

def p_expressao_variavel(p):
    '''
    expr : VAR
    '''

def p_expressao_operacao(p):
    '''
    expr : expr OPER_MATEMATICO expr
    '''

def p_expressao_grupo(p):
    '''
    expr : ABRE_PARENT expr FECHA_PARENT
    '''

###-------#####
# Regras para Variáveis
###-------#####
def p_criacaoVariavel(p):
    '''
    statement : TIPO_VAR VAR PONTO_FINAL
            | TIPO_VAR VAR OPER_ATRIB expr PONTO_FINAL
            | TIPO_VAR VAR OPER_ATRIB VALOR_TEXTO PONTO_FINAL
            | TIPO_VAR VAR OPER_ATRIB VAR PONTO_FINAL
            | TIPO_VAR VAR OPER_ATRIB VAR_SENSOR PONTO_FINAL
    '''

def p_atribuicaoValorVariavel(p):
    '''
    statement : VAR OPER_ATRIB expr PONTO_FINAL
            | VAR OPER_ATRIB VALOR_TEXTO PONTO_FINAL
            | VAR OPER_ATRIB VAR PONTO_FINAL
    '''

###-------#####
# Regras para Funções
###-------#####
def p_parametro_vazio(p):
    '''
    param_vazio : 
    '''

def p_parametro_valor(p):
    '''
    param : VALOR_INTEIRO
        | VALOR_REAL
        | VALOR_TEXTO
    '''

def p_parametro_variavel(p):
    '''
    param : VAR
    '''

def p_parametro_grupo(p):
    '''
    param : param VIRGULA param
    '''

def p_regra_funcao(p):
    '''
    funcao : NOME_FUNCAO ABRE_PARENT param_vazio FECHA_PARENT
        | NOME_FUNCAO ABRE_PARENT param FECHA_PARENT
    '''

def p_regra_funcao_invocada(p):
    '''
    statement : funcao PONTO_FINAL
    '''

def p_regra_definir_funcao(p):
    '''
    statement : DEFINE_FUNCAO funcao ABRE_CHAVES statements FECHA_CHAVES
    '''

###-------#####
# Regras para Condicionais
###-------#####
def p_parametro_condicional(p):
    '''
    cond_param : VAR OPER_RELA VALOR_INTEIRO
            | VAR OPER_RELA VALOR_REAL
            | VAR OPER_RELA VALOR_TEXTO
            | VAR OPER_RELA VAR
            | VAR OPER_RELA VALOR_LOGICO
            | VAR OPER_RELA VAR_SENSOR
    '''

def p_parametros_condicionais_grupo(p):
    '''
    cond_param : cond_param OPER_LOGICO cond_param
    '''

def p_senao_se(p):
    '''
    senaose : COND_SENAOSE ABRE_PARENT cond_param FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
    '''

def p_senao_se_grupo(p):
    '''
    senaose : senaose senaose
    '''

def p_regra_condicionais(p): 
    '''
    statement : COND_SE ABRE_PARENT cond_param FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
            | COND_SE ABRE_PARENT cond_param FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES senaose
            | COND_SE ABRE_PARENT cond_param FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES senaose COND_SENAO ABRE_CHAVES statements FECHA_CHAVES
            | COND_SE ABRE_PARENT cond_param FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES COND_SENAO ABRE_CHAVES statements FECHA_CHAVES           
    '''

###-------#####
# Regras para Laços de Repetições
###-------#####
def p_regra_para(p):
    '''
    statement : REP_PARA ABRE_PARENT VAR OPER_ATRIB VALOR_INTEIRO VIRGULA cond_param VIRGULA VAR OPER_ATRIB VAR OPER_MATEMATICO VALOR_INTEIRO  FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
            | REP_PARA ABRE_PARENT VAR OPER_ATRIB VAR VIRGULA cond_param VIRGULA VAR OPER_ATRIB VAR OPER_MATEMATICO VALOR_INTEIRO  FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
            | REP_PARA ABRE_PARENT VAR OPER_ATRIB VAR_SENSOR cond_param VIRGULA VAR OPER_ATRIB VAR OPER_MATEMATICO VALOR_INTEIRO  FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
            | REP_PARA ABRE_PARENT VAR cond_param VIRGULA VAR OPER_ATRIB VAR OPER_MATEMATICO VALOR_INTEIRO  FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
    '''

def p_regra_enquanto(p):
    '''
    statement : REP_ENQUANTO ABRE_PARENT cond_param FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
    '''

###-------#####
# Regra para Tentar/Caso_Erro
###-------#####
def p_regra_tentar_caso_erro(p):
    '''
    statement : TENTAR ABRE_CHAVES statements FECHA_CHAVES CASO_ERRO ABRE_CHAVES statements FECHA_CHAVES
            | TENTAR ABRE_CHAVES statements FECHA_CHAVES CASO_ERRO ABRE_PARENT VAR FECHA_PARENT ABRE_CHAVES statements FECHA_CHAVES
    '''



###-------#####
# Interface Gráfica
###-------#####
sg.ChangeLookAndFeel("Dark")  # Mudança do Tema

WIN_W = 90
WIN_H = 25
arquivo = None

menu_novo_arquivo = "Novo        "
menu_abrir_arquivo = "Abrir      "
menu_salvar_arquivo = "Salvar      "

sg.Text()
menu_layout = (
    ["Arquivo", [menu_novo_arquivo, menu_abrir_arquivo, menu_salvar_arquivo]],
    ["Tabela de Tokens", ["Consultar Tabela"]],
    ["Sobre", ["Autores"]],
)

layout = [
    [sg.MenuBar(menu_layout)],
    [
        sg.Multiline(
            font=("Consolas", 12), text_color="white", size=(WIN_W, WIN_H * 0.7), key="_ENTRADA_"
        )
    ],
    [sg.Button('Executar'), sg.Button('Limpar')],
    [sg.Output(font=("Consolas", 12) ,size=(WIN_W, WIN_H * 0.2), key='_SAIDA_')]
]

window = sg.Window(
    "COMPILADOR - JETTEX",
    layout=layout,
    margins=(0, 0),
    resizable=True,
    return_keyboard_events=True,
)
window.read(timeout=1)

window["_ENTRADA_"].expand(expand_x=True, expand_y=True)
window["_SAIDA_"].expand(expand_x=True, expand_y=True)


def novo_arquivo() -> str:
    window["_ENTRADA_"].update(value="")
    arquivo = None
    return arquivo


def abrir_arquivo() -> str:
    try:
        arquivo: str = sg.popup_get_file("Abrir Arquivo", no_window=True)
    except:
        return "Erro"
    if arquivo not in (None, "") and not isinstance(arquivo, tuple):
        with open(arquivo, "r") as f:
            window["_ENTRADA_"].update(value=f.read())
    return arquivo


def salvar_arquivo(arquivo: str):
    if arquivo not in (None, ""):
        with open(arquivo, "w") as f:
            f.write(values.get("_ENTRADA_"))
    else:
        salvar_como()


def salvar_como() -> str:
    try:
        arquivo: str = sg.popup_get_file(
            "Salvar Arquivo",
            save_as=True,
            no_window=True,
            default_extension=".jtx",
            file_types=(('ALL Files', '*.* *'),),
        )
    except:
        return
    
    if arquivo not in (None, "") and not isinstance(arquivo, tuple):
        with open(arquivo, "w") as f:
            f.write(values.get("_ENTRADA_"))
    return arquivo

def limpar():
    window["__ENTRADA__"].update('')

def exibir_autores():
    sg.PopupNoTitlebar(
        """
        Autores:
        Gabriel Vieira Cardoso
        Matheus Ribeiro da Silva
        Disciplina: Compiladores
        """
    )

def exibir_tabela_tokens():
    cabecalho_tabela = ["NOME_TOKEN", "LEXEMA", "EXPRESSÃO REGULAR", "DESCRIÇÃO"]
    tokens_registrados = [
        ["IFSULDEMINAS", "IFSULDEMINAS", "IFSULDEMINAS", "Palavra reservada IFSULDEMINAS."],
        ["tipo_var", "~numero_inteiro, ~texto, ~porcentagem, ~temperatura, ~numero_real, ~booleano, ~lista, ~tempo, ~data", "~numero_inteiro | ~texto | ~porcentagem | ~temperatura | ~numero_real | ~booleano | ~lista | ~tempo | ~data", "Tipos de variáveis que a linguagem poderá aceitar."],
        ["var", "#velocidade_anterior, #nome_condutor, #marcha2, etc.","\#[A-z0-9\_]+","Variável quando declarada ou invocada."],
        ["var_sensor", "NIVEL_TANQUE, MARCHA, TEMPERATURA, VELOCIDADE, DISTANCIA_TRAS, DISTANCIA_FRENTE, POSICAO_VIDROS, VIDA_UTIL_PNEUS, ACELERADOR, FREIO, EMBREAGEM, DATA_ATUAL e HORA_ATUAL, POSICAO_DIRECAO", "VELOCIDADE | NIVEL_TANQUE | MARCHA | TEMPERATURA | DISTANCIA_TRAS | DISTANCIA_FRENTE | POSICAO_VIDROS | VIDA_UTIL_PNEUS | ACELERADOR | FREIO | EMBREAGEM | DATA_ATUAL | HORA_ATUAL | POSICAO_DIRECAO", "Palavras reservadas que conterão valores lidos nos sensores do carro."],
        ["oper_rela", "<, >, <=, >=, =, !=", "<= | >= | < | > |  = | !=", "Operadores que permitem a comparação e relação entre variáveis."],
        ["oper_matematico", '+, -, /, *', '\+|-|\/|\*', "Operadores para realizar cálculos matemáticos."],
        ["oper_atrib", ":=", ":=", "Operadores que permitem a atribuição de um valor a uma variável ou de uma variável a outra."],
        ["oper_logico", "E, OU", "E|OU", "Operadores lógicos para concatenar comparações."],
        ["cond_se","se","se","Palavra reservada se para estrutura condicional: se."],
        ["cond_senao", "senao", "senao", "Palavra reservada para estrutura condicional: senao."],
        ["cond_senaose", "cond_senaose", "cond_senaose", "Palavra reservada para estrutura condicional: senaose."],
        ["rep_para","para","para","Palavra reservada para estrutura de repetição: para."],
        ["rep_enquanto", "enquanto", "enquanto", "Palavra reservada para estrutura de repetição: enquanto."],
        ["tentar","tentar","tentar","Palavra reservada para tratamento de erros: tentar."],
        ["caso_erro", "caso_erro", "caso_erro", "Palavra reservada para tratamento de erros: caso_erro"],
        ["nome_funcao","!exibeMensagemPainel, !trocaMarcha, !acelera, !desacelera, etc.","!([a-zA-Z][a-zA-Z0-9]+)","Declaração ou invocação de funções permitida na linguagem."],
        ["define_funcao","define_funcao","define_funcao","alavra reservada para a criação de funções dentro da linguagem."],
        ["valor_logico","Verdadeiro,Falso","Verdadeiro|Falso","Valor booleano de falsidade ou negativo ou vazio a ser exibido, processado ou armazenado em uma variável do tipo ~booleano."],
        ["valor_texto",'“Olá”, “Seu nome”, “Nome do Carro”, “Placa do Carro”, etc.','(\"[^\"]*")|(\\\'[^\\\']*\\\')',"Valor de qualquer texto a ser exibido, processado ou armazenado em uma variável do tipo ~texto."],
        ["valor_inteiro","10, 1, 0, -3, 1239123, etc.","\b(\d+)\b","Valor de qualquer número inteiro a ser exibido, processado ou armazenado em uma variável do tipo ~numero_inteiro."],
        ["valor_real","0.5,0.674","(\d+)\.(\d+)","Valor de qualquer número real a ser exibido, processado ou armazenado em uma variável do tipo ~numero_real."],
        ["valor_data","20/10/2010, etc","[0-3][0-9]\/[0-1][0-9]\/[0-9][0-9][0-9][0-9]","Valor de qualquer número real a ser exibido, processado ou armazenado em uma variável do tipo ~data."],
        ["valor_horario","18:13, 08:45, etc","[0-9][0-9]:[0-9][0-9]","Valor de qualquer número real a ser exibido, processado ou armazenado em uma variável do tipo ~horario."],
        ["abre_parent","(","\(","Identificador de abrir parênteses."],
        ["fecha_parent",")","\)","Identificador de fechar parênteses."],
        ["abre_chaves","{","\{","Identificador de abrir de chaves."],
        ["fecha_chaves","}","\}","Identificador de fechar de chaves."],
        ["comentario","[qualquer caracter]",'(\"[^\"]*\")|(\\\'[^\\\']*\\\')',"Identificador de abrir comentário."],
        ["ponto_final",".","\.","Identificador de final de linha."],
        ["virgula",",",",","Identificador de virgula no código"],   
    ]

    layout = [[sg.Table(
        values=tokens_registrados,
        headings=cabecalho_tabela,
        auto_size_columns=True,
        max_col_width=40,
        justification='center',
        num_rows=32,
        key="_TABELATOKENS_",
        row_height=16
    )]]
    janela = sg.Window("Tabela de Tokens", layout=layout, resizable=True)
    event, values = janela.read()
    janela.close()
    return None

###-------#####
# Função principal que executa o Analisador Léxico quando o evento "Executar" ocorre
###-------#####
def executar():
    global g_token_invalido
    g_token_invalido = ""

    window["_SAIDA_"].update('') 

    print("ANÁLISE LÉXICA: ")
    analisadorLexico = AnalisadorLexico()
    analisadorLexico.input(values.get("_ENTRADA_"))

    #while True:
        #token = analisadorLexico.token()
    for token in analisadorLexico:
        if not token:
            break 

        elif token.type == "COMENTARIO":
            print("Comentário de Código Ignorado! - Linha: ",token.lineno," - ", token.value.replace("\n",""))
            continue
        
        elif token.type == "VALOR_INTEIRO" and len(token.value) > 20:
            print(f"Erro Léxico! - Linha:", token.lineno," - Coluna: ", token.lexpos," - Número excede o tamanho permitido (20 caracteres)! - Valor inserido:", token.value)      
            continue

        elif token.type == "VAR" and len(token.value) > 20:
            print("Erro Léxico! - Linha:", token.lineno, " - Coluna:", token.lexpos, " - Nome da Variável excede o tamanho máximo permitido (20 caracteres)! - Valor inserido:", token.value)      
            continue

        elif token.type == "TEXTO_MAL_FORMADO":
            print("Erro Léxico! - Linha:", token.lineno, " - Texto Mal Formado: ", token.value.replace("\n",""))
            continue

        elif g_token_invalido != '':
            print('Erro Léxico! - Linha:', token.lineno, ' - Coluna: ', token.lexpos,' - ',verificaErroTokenInvalido(g_token_invalido))
            g_token_invalido = ''
            continue
        
        print('Linha:',token.lineno, ' - Coluna:',token.lexpos,' - Token: <',token.type,',',token.value.replace("\n",""),'>')

    if g_token_invalido != '':
        print('Erro Léxico! Última Linha!', verificaErroTokenInvalido(g_token_invalido))
        g_token_invalido = ''

    print("Processo de Análise Léxica Concluído com Sucesso")
    print("-------------")
    print("ANÁLISE SINTÁTICA:")
    lexer = lex()
    parser = yacc()
    parser.parse(values.get("_ENTRADA_"))
    if retornaQuantErros() == 0:
        print("Compilação Sem Erros!!!")
    print("Processo de Análise Sintática Concluído com Sucesso")

###-------#####
# Definindo as chamadas de funções a partir dos eventos na interface (clique em botões e no menu)
###-------#####
while True:
    event, values = window.read()

    if event in (None, "Exit"):
        window.close()
        break
    if event in (menu_novo_arquivo, "n:78"):
        arquivo = novo_arquivo()
    if event in (menu_abrir_arquivo, "o:79"):
        arquivo = abrir_arquivo()
    if event in (menu_salvar_arquivo, "s:83"):
        salvar_arquivo(arquivo)
    if event in ("Save As",):
        arquivo = salvar_como()
    if event == "Consultar Tabela":
        exibir_tabela_tokens()
    if event == "Autores":
        exibir_autores()
    if event == "Executar":
        executar()
    if event == "Limpar":
        print("Clicou em Limpar")
        window["_SAIDA_"].update('')    
