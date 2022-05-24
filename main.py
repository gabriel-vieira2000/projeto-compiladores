import re

import ply.lex as lex
import PySimpleGUI as sg

#Variável de Controle do Token Invalido
g_token_invalido = ""

###-------#####
# Classe do Analisador Léxico
###-------#####
def AnalisadorLexico():

    #Lista de Tokens
    tokens = ('IFSULDEMINAS','TIPO_VAR', 'VAR', 'VAR_SENSOR', 'OPER_RELA', 'OPER_MATEMATICO',
            'OPER_ATRIB','OPER_LOGICO', 'COND_SE', 'COND_SENAO', 'COND_SENAOSE', 'REP_PARA',
            'REP_ENQUANTO', 'TENTAR', 'CASO_ERRO', 'NOME_FUNCAO', 'DEFINE_FUNCAO', 'VALOR_LOGICO',
            'VALOR_TEXTO','VALOR_INTEIRO', 'VALOR_REAL', 'VALOR_PORCENTAGEM', 'VALOR_TEMPERATURA',
            'VALOR_DATA','VALOR_HORARIO', 'ABRE_PARENT', 'FECHA_PARENT', 'ABRE_CHAVES', 'FECHA_CHAVES',
            'ABRE_COMENTARIO', 'FECHA_COMENTARIO', 'PONTO_FINAL', 'VIRGULA', 'ESPACO')

    # REGEX DE CADA TOKEN
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
    t_VALOR_TEXTO = r'"[a-zA-Z0-9áàâãéèêíïóôõöúçÁÀÂÃÉÈÍÏÓÔÕÖÚ\.\s\_,\?!@\#$%&\|\*\(\)]*"'
    t_VALOR_INTEIRO = r'\b-?(\d+)\b'
    t_VALOR_REAL = r'-?(\d+)\.(\d+)'
    t_VALOR_PORCENTAGEM = r'/(\d+(\.\d+)?%)'
    t_VALOR_TEMPERATURA = r'-?(\d+)\.(\d+)C'
    t_VALOR_DATA = r'[0-3][0-9]\/[0-1][0-9]\/[0-9][0-9][0-9][0-9]'
    t_VALOR_HORARIO = r'[0-9][0-9]:[0-9][0-9]'
    t_ABRE_PARENT = r'\('
    t_FECHA_PARENT = r'\)'
    t_ABRE_CHAVES = r'\{'
    t_FECHA_CHAVES = r'\}'
    t_ABRE_COMENTARIO = r'\['
    t_FECHA_COMENTARIO = r'\]'
    t_PONTO_FINAL = r'\.'
    t_VIRGULA = r','
    t_ESPACO = r'\s'

    # TOKENS que devem ser ignorados
    t_ignore = '\t'

    def constroiTokenInvalido(token):
        global g_token_invalido
        g_token_invalido = g_token_invalido + token
        
    def t_error(token):
        constroiTokenInvalido(token.value[0])
        token.lexer.skip(1)

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    return lex.lex()


###-------#####
# Função para Tratar Tokens Inválidos
###-------#####
def verificaErroTokenInvalido(token_invalido):
    if g_token_invalido != '':
        if (g_token_invalido[0] == '"' and g_token_invalido[-1] != '"') or (g_token_invalido[0] != '"' and g_token_invalido[-1] == '"'):
            return (f"Erro Léxico! - String mal formada - Token: {g_token_invalido}")

        elif g_token_invalido[0] in ('1','2','3','4','5','6','7','8','9'):
            return (f"Erro Léxico! - Número não identificado! Token: {g_token_invalido}")

        else:
            return (f"Erro Léxico! Caractere ou sequência de caracteres não reconhecido(s) na linguagem: {g_token_invalido}")


###-------#####
# Interface Gráfica
###-------#####
sg.ChangeLookAndFeel("Dark")  # Mudança do Tema

WIN_W = 90
WIN_H = 25
arquivo = None

file_new = "Novo        (CTRL+N)"
file_open = "Abrir      (CTRL+O)"
file_save = "Salvar      (CTRL+S)"

sg.Text()
menu_layout = (
    ["Arquivo", [file_new, file_open, file_save, "---", "Sair"]],
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
            file_types=(("Text", ".txt"),),
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
        Gabriel Vieira Cardoso
        Matheus Ribeiro da Silva
        Trabalho Desenvolvido para a disciplina de compiladores!
        """
    )

def exibir_tabela_tokens():
    cabecalho_tabela = ["NOME_TOKEN", "LEXEMA", "EXPRESSÃO REGULAR", "DESCRIÇÃO"]
    tokens_registrados = [
        ["IFSULDEMINAS", "IFSULDEMINAS", "IFSULDEMINAS", "Palavra reservada IFSULDEMINAS."],
        ["VALOR_INTEIRO", "1, 123, 1919", "VELOCIDADE | NIVEL_TANQUE | MARCHA | TEMPERATURA | DISTANCIA_TRAS | DISTANCIA_FRENTE | POSICAO_VIDROS | VIDA_UTIL_PNEUS | ACELERADOR | FREIO | EMBREAGEM | DATA_ATUAL | HORA_ATUAL | POSICAO_DIRECAO", "Valores Inteiros da Linguagem"]    
    ]

    layout = [[sg.Table(
        values=tokens_registrados,
        headings=cabecalho_tabela,
        auto_size_columns=True,
        max_col_width=50,
        justification='center',
        num_rows=2,
        key="_TABELATOKENS_",
        row_height=15
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

    analisadorLexico = AnalisadorLexico()
    analisadorLexico.input(values.get("_ENTRADA_"))

    while True:
        token = analisadorLexico.token()
        
        if not token:
            break 

        if token.type == "ESPACO":
            continue
        
        elif token.type == "VALOR_INTEIRO" and len(token.value) > 20:
            print(f"Erro Léxico! - Linha:", token.lineno," - Coluna: ", token.lexpos," - Número excede o tamanho permitido (20 caracteres)! - Valor inserido:", token.value)      
            continue

        elif token.type == "VAR" and len(token.value) > 20:
            print("Erro Léxico! - Linha:", token.lineno, " - Coluna:", token.lexpos, " - Nome da Variável excede o tamanho máximo permitido (20 caracteres)! - Valor inserido:", token.value)      
            continue

        elif g_token_invalido != '':
            print('Erro Léxico! - Linha:', token.lineno, ' - Coluna: ', token.lexpos,' - ',verificaErroTokenInvalido(g_token_invalido))
            g_token_invalido = ''
            continue
        
        print(f'Linha: {token.lineno} - Coluna: {token.lexpos} - Token: <{token.type},{token.value}>')

    if g_token_invalido != '':
        print(verificaErroTokenInvalido(g_token_invalido),"Linha:", {token.lineno})
        g_token_invalido = ''

    print("Processo de Análise Léxica Concluído com Sucesso")

###-------#####
# Definindo as chamadas de funções a partir dos eventos na interface (clique em botões e no menu)
###-------#####
while True:
    event, values = window.read()

    if event in (None, "Exit"):
        window.close()
        break
    if event in (file_new, "n:78"):
        arquivo = novo_arquivo()
    if event in (file_open, "o:79"):
        arquivo = abrir_arquivo()
    if event in (file_save, "s:83"):
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
        window["_SAIDA_"].update('')    

