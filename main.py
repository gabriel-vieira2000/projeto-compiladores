import re

import ply.lex as lex
import PySimpleGUI as sg


def AnalisadorLexico():
    #Lista de Tokens
    tokens = ('IFSULDEMINAS','TIPO_VAR', 'VAR', 'VAR_SENSOR', 'OPER_RELA', 'OPER_MATEMATICO',
            'OPER_ATRIB','OPER_LOGICO', 'COND_SE', 'COND_SENAO', 'COND_SENAOSE', 'REP_PARA',
            'REP_ENQUANTO', 'TENTAR', 'CASO_ERRO', 'NOME_FUNCAO', 'DEFINE_FUNCAO', 'VALOR_LOGICO',
            'VALOR_TEXTO','VALOR_INTEIRO', 'VALOR_REAL', 'VALOR_PORCENTAGEM', 'VALOR_TEMPERATURA',
            'VALOR_DATA','VALOR_HORARIO', 'ABRE_PARENT', 'FECHA_PARENT', 'ABRE_CHAVES', 'FECHA_CHAVES',
            'ABRE_COMENTARIO', 'FECHA_COMENTARIO', 'FINAL_LINHA', 'VIRGULA')

    # REGEX DE CADA TOKEN
    t_IFSULDEMINAS = r'IFSULDEMINAS'
    t_TIPO_VAR = r'~numero_inteiro | ~texto | ~porcentagem | ~temperatura | ~numero_real | ~booleano | ~lista | ~tempo | ~data'
    t_VAR = r'\#[A-z0-9\_]+'
    t_VAR_SENSOR = r'VELOCIDADE | NIVEL_TANQUE | MARCHA | TEMPERATURA | DISTANCIA_TRAS | DISTANCIA_FRENTE | POSICAO_VIDROS | VIDA_UTIL_PNEUS | ACELERADOR | FREIO | EMBREAGEM | DATA_ATUAL | HORA_ATUAL | POSICAO_DIRECAO'
    t_OPER_RELA = r'< | > | <= | >= | = | !='
    t_OPER_MATEMATICO = r'\+|-|\/|\*'
    t_OPER_ATRIB = r':='
    t_OPER_LOGICO = r'\sE\s | \sOU\s'
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
    t_VALOR_INTEIRO = r'-?(\d+)'
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
    t_FINAL_LINHA = r'\.'
    t_VIRGULA = r','

    # TOKENS que devem ser ignorados
    t_ignore = ' \t'

    def t_error(t):
        print(f'Caractere Proibido na linguagem: {t.value[0]}')
        t.lexer.skip(1)

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    return lex.lex()

sg.ChangeLookAndFeel("Dark")  # Mudança do Tema

WIN_W = 90
WIN_H = 25
filename = None

file_new = "Novo        (CTRL+N)"
file_open = "Abrir      (CTRL+O)"
file_save = "Salvar      (CTRL+S)"

sg.Text()
menu_layout = (
    ["Arquivo", [file_new, file_open, file_save, "---", "Sair"]],
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
    [sg.Output(size=(WIN_W, WIN_H * 0.2), key='_SAIDA_')]
]

window = sg.Window(
    "COMPILADOR - JETTEX",
    layout=layout,
    margins=(0, 0),
    resizable=True,
    return_keyboard_events=True,
    icon="/moonlight_notepad/devaprender.ico",
)
window.read(timeout=1)

window["_ENTRADA_"].expand(expand_x=True, expand_y=True)


def new_file() -> str:
    window["_ENTRADA_"].update(value="")
    filename = None
    return filename


def open_file() -> str:
    try:
        filename: str = sg.popup_get_file("Abrir Arquivo", no_window=True)
    except:
        return "Erro"
    if filename not in (None, "") and not isinstance(filename, tuple):
        with open(filename, "r") as f:
            window["_ENTRADA_"].update(value=f.read())
    return filename


def save_file(filename: str):
    if filename not in (None, ""):
        with open(filename, "w") as f:
            f.write(values.get("_ENTRADA_"))
    else:
        save_file_as()


def save_file_as() -> str:
    try:
        filename: str = sg.popup_get_file(
            "Save File",
            save_as=True,
            no_window=True,
            default_extension=".txt",
            file_types=(("Text", ".txt"),),
        )
    except:
        return
    if filename not in (None, "") and not isinstance(filename, tuple):
        with open(filename, "w") as f:
            f.write(values.get("_ENTRADA_"))
    return filename

def limpar():
    window["__ENTRADA__"].update('')

def exibir_autores():
    sg.PopupNoTitlebar(
        """
        Gabriel Vieira Cardoso
        Matheus Ribeiro da Silva
        """
    )


def executar():
    print("Criando o Analisador Léxico....")
    analisadorLexico = AnalisadorLexico()
    print("Criando o Analisador Léxico....OK")
    print("Inserindo a Entrada no Analisador Léxico....")
    analisadorLexico.input(values.get("_ENTRADA_"))
    print("Inserindo a Entrada no Analisador Léxico....OK")
    print("Iniciando o processo de Tokenizacao....")
    while True:
        token = analisadorLexico.token()
        if not token: 
            break      
        print(f'Linha: {token.lineno} - Coluna: {token.lexpos} - Token: <{token.type},{token.value}>')
    print("Processo de Análise Léxica Concluído com Sucesso")

while True:
    event, values = window.read()

    if event in (None, "Exit"):
        window.close()
        break
    if event in (file_new, "n:78"):
        filename = new_file()
    if event in (file_open, "o:79"):
        filename = open_file()
    if event in (file_save, "s:83"):
        save_file(filename)
    if event in ("Save As",):
        filename = save_file_as()
    if event == "Autores":
        exibir_autores()
    if event == "Executar":
        executar()
    if event == "Limpar":
        window["_SAIDA_"].update('')    

