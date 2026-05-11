# Horus

O mal uso desse sistema para obter informações com fins fraudulentos ou maliciosos não são de minha responsabilidade, use por sua conta e risco. Todas as informações providenciadas pelo programa são de fontes públicas, apenas a busco e por fim indexamos.

O propósito do sistema é aos poucos ser evoluido, adicionando fontes novas e validando, evitando muitos falsos-positivos. 


### Como funciona?

No momento, você precisará baixar todas as dependências de `requirements.txt` usando o seguinte método:

> python3 -m venv env              # Cria ambiente virtual

> source env/bin/activate          # Ativa o ambiente virtual

> pip3 install -r requirements.txt # Instala todas as dependências

Após a instalação de todas as dependências, será necessário criar um arquivo chamado `settings.py` no mesmo diretório onde se encontra o arquivo `main.py`. Nele, você deve criar uma variável chamada `VT_API_KEY=""` onde receberá a chave de API da plataforma Vírus Total (utilizada para fazer consultas de informações de um endereço IP). Você deve criar uma conta na plataforma Vírus Total (É gratuito).

Além disso, você deve ter o TOR (The Onion Router) que servirá de proxy, funcionando em sua máquina, a porta que deve ser liberada em `/etc/tor/torrc` é a porta `9060` (Sinta-se livre para usar qual quiser, somente não esqueça de modificar o arquivo `main.py` após alterações). A seguinte linha dentro do arquivo suprecitado contém o suficiente para o funcionamento dessa porta:

> SocksPort 9060

Salve o arquivo e reinicie o Daemon do Tor.

- Debian/Ubuntu/Arch based
> sudo systemctl restart tor
-  Void Linux
> sudo sv restart tor

### Necessidades extras

Caso queira utilizar a busca de nicknames, você precisará do programa chamado `proxychains`, você pode encontrá-lo como `proxychains4` ou `proxychains-ng` em sua distribuição Linux. Para o correto funcionamento, altere as seguintes linhas no arquivo `/etc/proxychains.conf`:

Comente a linha 

> # strict_chain

E descomente a linha

> random_chain

E por fim, adicione na última linha do arquivo o seguinte conteúdo:

> socks5    127.0.0.1 9050

No lugar de `9050` você deve colocar qual porta você abriu no arquivo de configuração `/etc/tor/torrc`.

# Licença

GNU GPL-3

# Capacidades atuais

1. Consulta de dados de endereço IP usando a api do Vírus Total.
2. Pesquisa de nomes de usuários usando a ferramenta Sherlock.
3. uso de proxying em operações de rede.
