# Scraper de Informações de Empresas

## Descrição
Este projeto é um scraper desenvolvido em Python para coletar informações e dados públicos de empresas de um site específico. Ele extrai dados como nome da empresa, e-mail de contato e telefone, e salva os resultados em um arquivo CSV. O scraper foi desenvolvido para automatizar um processo que seria manual e demorado, facilitando a coleta de informações para prospecção e consultas.

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **Selenium**: Para automação da navegação no site.
- **BeautifulSoup**: Para análise e extração de dados HTML.
- **Pandas**: Para manipulação e salvamento dos dados em CSV.
- **Requests**: Para fazer requisições HTTP.
- **lxml**: Para análise de HTML e XML.

## Funcionalidades Principais
- Navegação automática pelas páginas do site.
- Extração de e-mails e telefones dos anúncios.
- Salvamento dos dados em um arquivo CSV.
- Paginação automática até a última página disponível.
- Tratamento de exceções para garantir a robustez do scraper.
- Configuração de cabeçalhos HTTP para simular um navegador real.

## Contexto
Este scraper foi desenvolvido a partir de uma necessidade de um projeto paralelo para facilitar a coleta de informações para prospecção e consultas, automatizando um processo. Ele foi utilizado para coletar dados de empresas de um site específico, permitindo a análise e o contato direto com as empresas listadas.

### Pré-requisitos
- Python 3.x instalado.
- Gerenciador de pacotes `pip` instalado.
  
### Instalação
1. Clone o repositório:
   ```bash
   git clone [https://github.com/Jzyker/scraper]
   pip install -r requirements.txt
2. Configure
   # Função principal
def main():
    url_base = "WEBSITE HERE"
    dados_totais = []


# Altere as classes e títulos encontrados via HTML.
   ```bash
    anuncios = soup.find_all('header', class_='elementor-element')
    for anuncio in anuncios:
        try:
            # Extrai a info1
            nome_empresa = anuncio.find('h2', class_='elementor-heading-title').text.strip()
            print(f"Processando anúncio: {nome_empresa}")

            # Extrai o link do anúncio
            link_anuncio = anuncio.find('a')['href']

            try:
                botao_candidatar_inicial = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Quero me candidatar")]'))
                )
                driver.execute_script("arguments[0].click();", botao_candidatar_inicial)
                time.sleep(2)  # Espera a página do anúncio carregar
            except:
                continue


    return dados
