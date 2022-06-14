from ply.lex import lex
from ply.yacc import retornaQuantErros, yacc

g_token_invalido = ''

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

lexer = lex()
parser = yacc()
parser.parse("""
    [&*@&#(*)]
    #soma := 10 + "203".
    #teste := 20*104+(331+10).
    #leandro := 'Ihh loco'.
    #soma2 := #soma1.
    ~numero_inteiro #n := MARCHA.
""")
print('-------------')
parser.parse("""
    define_funcao !eaeboy(#parametro){
        #parametro := 10.
        #soma := 20 + #parametro.
    }
    !eaeboy(#parametro, 10).
    !eaeboy().
""")
print('-----------')
parser.parse("""
    se(#p >= 10 E #p <= 50 OU #t = 10){ 
        se(#p = 10){#soma := 10 + #soma.}
        #soma := 20 + #soma.
    }senaose(#t = 4){ !printa(#t).
    }senaose(#t = 5){ #t := 3. }
    senao { #soma := 10 - 20.}
""")
print('-----------')
parser.parse("""
    para(#i := 10, #i <= 20, #i := #i + 1){
        !printa("Número: ", #i).
    }
    enquanto(#i != 20){
        !printa("Número: ",#i).
        #i := #i + 1.
    }
""")
print('-----------')
parser.parse("""
    tentar{
        !acessarBancoDados(#senha).
    }caso_erro{
        !printaErro("Acesso Negado!")
    }

    tentar{
        !acessarBancoDados(#senha).
    }caso_erro(#erro){
        !printaErro("Erro ao acessar banco de dados: ",#erro).
    }
""")

print(retornaQuantErros())
