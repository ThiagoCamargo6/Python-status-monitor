# StatusMonitor ✨

### 🤔 Por que usar o StatusMonitor?

Você é um desenvolvedor, um entusiasta de tecnologia ou apenas alguém que depende de vários serviços online? Se sim, o StatusMonitor foi feito para você. Ele elimina a necessidade de abrir múltiplos terminais ou abas no navegador para verificar se tudo está funcionando.

**Este painel é especialmente útil para:**

Manter um olho em APIs e microserviços locais (`localhost`) durante o desenvolvimento.
Monitorar a saúde de endpoints de produção ou de testes de forma rápida e visual.
Acompanhar o status de APIs públicas que você usa em seus projetos (previsão do tempo, finanças, etc.).

---

### ✨ Funcionalidades Principais

* **Monitoramento em Tempo Real:** Verifica periodicamente o status dos serviços.
* **Interface Limpa e Moderna:** Construído com CustomTkinter para um visual agradável que se adapta ao modo Claro/Escuro do seu sistema.
* **Configuração Externa:** Adicione, remova ou edite serviços facilmente através do arquivo `config.json`, sem precisar alterar o código.
* **Métricas Relevantes:** Veja rapidamente o status (`UP`, `DOWN`, `OFFLINE`), o código de resposta HTTP e o tempo de resposta (latência) de cada serviço.
* **Interativo e Prático:**
    * Clique em qualquer serviço para abri-lo diretamente no seu navegador.
    * Recarregue todos os status manualmente com um único botão.
    * Ícones e emojis para uma leitura rápida e intuitiva da informação.
* **Leve e Multiplataforma:** Por ser feito em Python, roda em Windows, macOS e Linux.

---

![image](https://github.com/user-attachments/assets/5f981e72-01c1-4bc5-a336-30ca39cdd3d9)


### 🛠️ Instalação e Execução

Siga os passos abaixo para ter seu StatusMonitor rodando em menos de 2 minutos.

**1. Pré-requisitos:**
* **Python 3.8** ou superior instalado.

**2. Clone o Repositório:**
Abra seu terminal ou prompt de comando e execute:
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```
*(Substitua `seu-usuario/seu-repositorio` pelo seu usuário e nome do repositório no GitHub)*

**3. (Opcional, mas recomendado) Crie um Ambiente Virtual:**
Isso mantém as dependências do projeto isoladas do seu sistema.
```bash
python -m venv venv
```
Para ativar o ambiente:
* No **Windows**: `venv\Scripts\activate`
* No **macOS/Linux**: `source venv/bin/activate`

**4. Instale as Dependências:**
O arquivo `requirements.txt` cuida de tudo para você.
```bash
pip install -r requirements.txt
```

**5. Configure seus Serviços:**
* Abra o arquivo `config.json` com um editor de texto.
* Edite a lista de `services` para incluir os nomes e URLs que você deseja monitorar.

**6. Execute a Aplicação:**
```bash
python monitor_app.py
```
Pronto! Seu painel de monitoramento deve aparecer na tela.

---

### ⚙️ Configuração

Toda a configuração é feita no arquivo `config.json`.

```json
{
  "settings": {
    "refresh_interval_seconds": 60
  },
  "services": [
    {
      "name": "Nome do Seu Serviço",
      "url": "[https://url.do.servico.com](https://url.do.servico.com)"
    },
    {
      "name": "API Local",
      "url": "http://localhost:8000"
    }
  ]
}
```

* `refresh_interval_seconds`: O intervalo, em segundos, para a atualização automática dos status.
* `services`: Uma lista de objetos, onde cada um representa um serviço a ser monitorado. Adicione quantos quiser!

---

### 👨‍💻 Tecnologias Utilizadas

* **Python:** A linguagem base do projeto.
* **CustomTkinter:** Para a criação da interface gráfica moderna.
* **Requests:** Para fazer as requisições HTTP e verificar os serviços.

---

### 📄 Licença

Este projeto está sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
