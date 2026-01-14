# 📱 Android Accessibility AI Agent (Local RAG)

Este é um assistente de programação inteligente que roda localmente na sua máquina. Ele utiliza **SLMs (Small Language Models)** para gerar código **Android Jetpack Compose** com foco estrito em **Acessibilidade (WCAG & Material Design 3)**.

O projeto utiliza uma arquitetura híbrida:
1.  **RAG (Retrieval-Augmented Generation):** Consulta uma base de conhecimento local (`kb/`) com documentações que servem de base de conhecimento externo.
2.  **Few-Shot Learning:** Utiliza exemplos de código "Ruim vs Bom" para ensinar padrões de acessibilidade ao modelo.

---

## ✅ Pré-requisitos

Antes de começar, você precisa ter instalado:

* [Python 3.10+](https://www.python.org/downloads/)
* [Ollama](https://ollama.com/) (Para rodar o modelo de IA localmente)

---

## ⚙️ Configuração do Ollama (Passo Obrigatório)

O script depende do Ollama rodando em segundo plano.

### 1. Instalar e Rodar
1.  Baixe e instale o Ollama: [ollama.com](https://ollama.com).
2.  **Abra o Ollama** (verifique se o ícone da lhama aparece perto do relógio no Windows ou rode `ollama serve` no terminal).

### 2. Baixar os Modelos
Abra seu terminal e execute os comandos abaixo para baixar o cérebro da IA e o modelo de leitura de arquivos:

```bash
ollama pull codellama:7b
ollama pull nomic-embed-text

```

---

## 🚀 Instalação e Execução

### 1. Iniciar o Agente

Com o Ollama rodando, execute o comando abaixo no terminal para iniciar a conversa:

```bash
python main.py

```

---

## 📖 Como Usar o Menu

Ao iniciar, você verá as seguintes opções:

* **1. RAG Mode:** Use para pedir código. O sistema lê os arquivos da pasta `kb/` para responder.
* **2. Few-Shot Mode:** Use para pedir código. O sistema usa o arquivo `few_shot.py` para encorpar o seu prompt com exemplos positivos e negativos.
* **3. End Seasson:** Use esta opção para encerrar a conversa com o modelo.


## 🛠 Solução de Problemas

**Erro: "Connection refused"**

* O Ollama não está rodando. Abra o aplicativo ou execute `ollama serve`.
