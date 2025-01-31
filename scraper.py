import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re  # Para usar expressões regulares

# Configurações do Selenium (rodar em segundo plano)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar sem abrir a janela do navegador
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--log-level=3")  # Suprime logs desnecessários
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Remove logs do ChromeDriver

# Usa o webdriver-manager para instalar automaticamente a versão correta do ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Função para extrair e-mails e telefones de um anúncio
def extrair_dados_anuncio(url):
    driver.get(url)
    time.sleep(2)  # Espera a página carregar

    # Clica no segundo botão "Quero me candidatar" dentro do anúncio
    try:
        botao_candidatar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Quero me candidatar")]'))
        )
        driver.execute_script("arguments[0].click();", botao_candidatar)
        time.sleep(2)  # Espera o popup abrir
    except:
        return None, None

    # Extrai o conteúdo do popup
    try:
        popup_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "elementor-popup-modal")]'))
        )
        popup_text = popup_element.text

        # Procura por e-mails no texto do popup
        email = None
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', popup_text)
        if email_match:
            email = email_match.group(0)

        # Procura por números de telefone no texto do popup
        telefone = None
        telefone_match = re.search(
            r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}', popup_text
        )
        if telefone_match:
            telefone = telefone_match.group(0)

        print(f"E-mail extraído: {email}")
        print(f"Telefone extraído: {telefone}")
    except:
        email, telefone = None, None

    return email, telefone

# Função para processar uma página de anúncios
def processar_pagina(url):
    driver.get(url)
    time.sleep(2)  # Espera a página carregar

    # Extrai o HTML da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Lista para armazenar os dados
    dados = []

    # Encontra todos os anúncios
    anuncios = soup.find_all('header', class_='elementor-element')
    for anuncio in anuncios:
        try:
            # Extrai o nome da empresa
            nome_empresa = anuncio.find('h2', class_='elementor-heading-title').text.strip()
            print(f"Processando anúncio: {nome_empresa}")

            # Extrai o link do anúncio
            link_anuncio = anuncio.find('a')['href']

            # Clica no primeiro botão "Quero me candidatar" na página inicial
            try:
                botao_candidatar_inicial = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Quero me candidatar")]'))
                )
                driver.execute_script("arguments[0].click();", botao_candidatar_inicial)
                time.sleep(2)  # Espera a página do anúncio carregar
            except:
                continue

            # Extrai o e-mail e o telefone do anúncio
            email, telefone = extrair_dados_anuncio(link_anuncio)

            if email or telefone:
                dados.append({"Empresa": nome_empresa, "E-mail": email, "Telefone": telefone})
        except:
            continue

    return dados

# Função para salvar os dados em uma planilha
def salvar_dados(dados, nome_arquivo="vagas.csv"):
    if dados:
        df = pd.DataFrame(dados)
        df.to_csv(nome_arquivo, index=False, sep=';')  # Usa ';' como separador
        print(f"Dados salvos em '{nome_arquivo}'.")
    else:
        print("Nenhum dado foi extraído.")

# Função principal
def main():
    url_base = "https://vagasbauru.com.br/vagas/"
    dados_totais = []

    # Processa todas as páginas até a página 44
    pagina_atual = 1
    while pagina_atual <= 44:  # Limite de páginas
        print(f"Processando página {pagina_atual}...")
        url_pagina = f"{url_base}?e-page-82832da={pagina_atual}" if pagina_atual > 1 else url_base
        dados_pagina = processar_pagina(url_pagina)
        dados_totais.extend(dados_pagina)

        # Verifica se há mais páginas
        try:
            # Tenta encontrar o botão "Próxima"
            proxima_pagina = driver.find_element(By.XPATH, '//a[contains(@class, "page-numbers") and not(contains(@class, "current"))]')
            if not proxima_pagina:
                print("Todas as páginas foram processadas.")
                break
            # Incrementa o número da página
            pagina_atual += 1
        except:
            # Se não encontrar o botão "Próxima", tenta navegar diretamente para a próxima página
            try:
                proxima_url = f"{url_base}?e-page-82832da={pagina_atual + 1}"
                driver.get(proxima_url)
                time.sleep(2)  # Espera a próxima página carregar
                pagina_atual += 1
            except:
                print("Erro ao navegar para a próxima página.")
                break

    # Salva os dados em uma planilha
    salvar_dados(dados_totais)

    # Fecha o navegador
    driver.quit()

if __name__ == "__main__":
    main()