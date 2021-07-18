from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
)
from time import sleep
from gtts import gTTS
from playsound import playsound
import os
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------funções-------------------------------

def texto_para_fala(texto):
    print("Enviando mensagem...")
    fala = gTTS(texto, lang='pt')
    fala.save('mp3_fp.mp3')
    playsound('mp3_fp.mp3')
    os.remove('mp3_fp.mp3')


def listar_seguidores(browser, quant):
    # Clicando em seguidores
    label_quant_seguidores = '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span'
    wdw.until(element_to_be_clickable((By.CSS_SELECTOR, label_quant_seguidores)))
    seguidores = browser.find_element(By.CSS_SELECTOR, label_quant_seguidores)
    seguidores.click()

    # Entrando no pop-up
    pop_up_window = wdw.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    # Scroll till Followers list is there
    profiles = list()
    print(len(profiles))
    while len(profiles) < quant:
        profiles = browser.find_elements(By.CSS_SELECTOR, 'div.PZuss li')
        browser.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
            pop_up_window)
        sleep(1)

    # Adicionando os perfis a lista
    aux_list = list()
    for profile in profiles:
        aux_list.append(profile.find_element(By.CSS_SELECTOR, 'a.FPmhX').text)

    # Retorno da lista
    return aux_list


def quant_seguidores(browser):
    label_quant_seguidores = '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span'
    wdw.until(element_to_be_clickable((By.CSS_SELECTOR, label_quant_seguidores)))
    seguidores = browser.find_element(By.CSS_SELECTOR, label_quant_seguidores)
    num = int(seguidores.text)
    return num


def esperar(tempo):
    sleep(tempo)

# ---------------------------MAIN----------------------------------

# Dados do usuario
user = str(input("Digite o seu nome de usuario: "))
password = str(input("Digite sua senha: "))
t = int(input("Você quer que o o bot atualize a contagem de seguidores (SE HOUVER) no intervalo de quantos segundos?"))

# Atribuições
url = 'https://www.instagram.com'
url_perfil = f'https://www.instagram.com/{user}'
browser = Chrome()
wdw = WebDriverWait(browser, 10)
list_aux = list()

# Login no Instagram
browser.get(url)

wdw.until(element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
usuario = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
usuario.clear()
usuario.send_keys(user)

wdw.until(element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
senha = browser.find_element(By.CSS_SELECTOR, "input[name='password']")
senha.clear()
senha.send_keys(password)

wdw.until(element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
entrar = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
entrar.click()

sleep(5)

# Navegando ao perfil
browser.get(url_perfil)
quant_seguidores_antes = quant_seguidores(browser)

lista_seguidores_antes = listar_seguidores(browser, quant_seguidores_antes)
print(lista_seguidores_antes)

texto_para_fala(f"Você tem {quant_seguidores_antes} seguidores")

# Entrando no perfil e enalisando o comportamento dos seguidores
comecaram_a_seguir = list()
deixaram_de_seguir = list()
while True:
    browser.get(url_perfil)
    quant_seguidores_depois = quant_seguidores(browser)
    lista_seguidores_depois = listar_seguidores(browser, quant_seguidores_depois)

    # Usuarios que começaram a te seguir
    for nome in lista_seguidores_depois:
        if nome not in lista_seguidores_antes:
            lista_seguidores_antes.append(nome)
            comecaram_a_seguir.append(nome)
            quant_seguidores_antes += 1

    # Usuarios que deixaram de te seguir
    for nome in lista_seguidores_antes:
        if nome not in lista_seguidores_depois:
            list_aux.append(nome)
            quant_seguidores_antes -= 1

    for nome in list_aux:
        lista_seguidores_antes.remove(nome)
        deixaram_de_seguir.append(nome)
    list_aux.clear()

    # Exibindo os usuarios monitorados
    if len(comecaram_a_seguir) > 0:
        if len(comecaram_a_seguir) == 1:
            texto_para_fala("Você ganhou 1 novo seguidor!")
            texto_para_fala(f"{comecaram_a_seguir[0]}")
        else:
            texto_para_fala(f"Você ganhou {len(comecaram_a_seguir)} novos seguidores!")
            for nome in comecaram_a_seguir:
                texto_para_fala(f"{nome}")

    if len(deixaram_de_seguir) > 0:
        if len(deixaram_de_seguir) == 1:
            texto_para_fala("Você perdeu 1 seguidor!")
            texto_para_fala(f"{deixaram_de_seguir[0]}")
        else:
            texto_para_fala(f"Você perdeu {len(deixaram_de_seguir)} seguidores!")
            for nome in deixaram_de_seguir:
                texto_para_fala(f"{nome}")

    if len(deixaram_de_seguir) > 0 or len(comecaram_a_seguir) > 0:
        if len(deixaram_de_seguir) == len(comecaram_a_seguir):
            texto_para_fala(f"Você continua com {quant_seguidores_antes} seguidores")
        else:
            texto_para_fala(f"Agora você está com {quant_seguidores_antes} seguidores")

    # Limpando as listas
    comecaram_a_seguir.clear()
    deixaram_de_seguir.clear()

    # Pausa
    esperar(t)

# Made by Felipe Archanjo
