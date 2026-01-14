# main.py
import os
import ollama
from datetime import datetime
from pathlib import Path
# Importamos o build_index e o caminho do arquivo para verificar se ele existe
from src.rag import retrieve, build_index, INDEX_PATH
from few_shot import exemplos

# Model Configuration
CHAT_MODEL = "codellama:7b"

# Output Configuration
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# --- SYSTEM PROMPT ---
SISTEMA_PADRAO = """This model is specialized in assisted programming for developing mobile application interfaces using Jetpack Compose and Material Design 3, with an emphasis on accessibility. It provides clear, precise, and well-structured examples focused on usability best practices, modern design, and compliance with widely recognized accessibility guidelines, such as those from Material Design 3 (https://m3.material.io/foundations/overview/principles) and the official Android documentation (https://developer.android.com/guide/topics/ui/accessibility/apps?hl=en). It helps create screen layouts, custom components, navigation flows, and data integration, ensuring accessible interfaces for all users. It always uses the most up-to-date syntax and avoids obsolete practices. It can suggest improvements, explain code snippets, and adapt solutions according to the project. If there is any doubt about the context, it asks for more details before proceeding. Every time it provides code, it includes all necessary imports, the @OptIn(ExperimentalMaterial3Api::class) annotation when required, a main function with an identifiable placeholder name, a preview function, and also the entry class (Activity or equivalent), so that the generated code can be easily copied, pasted, and executed. Additionally, it automatically adapts accessibility implementations to work correctly in both light and dark themes according to the device settings."""

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def salvar_resposta(texto, prefixo="response"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{prefixo}_{timestamp}.md"
    caminho = OUTPUT_DIR / nome_arquivo
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"✅ Done! Response saved at: {caminho}")

# --- NOVA FUNÇÃO DE AUTO-REPARO ---
def verificar_indice_inicial():
    """Verifica se o índice existe. Se não existir (pq você apagou), cria um novo."""
    if not INDEX_PATH.exists():
        print("\n⚠️  Index file (kb_index.npz) not found.")
        print("⚙️  Building new index from 'kb/' files... Please wait.")
        try:
            qtd = build_index()
            print(f"✅ Index built successfully! ({qtd} chunks processed)")
        except Exception as e:
            print(f"❌ Critical Error building index: {e}")
            exit(1) # Fecha o programa se der erro grave

def modo_rag(pergunta):
    print("\n🔍 Searching in knowledge base (kb/)...")
    hits = retrieve(pergunta, top_k=5)
    contexto_str = "\n\n".join([f"Source: {h['source']}\nContent: {h['text']}" for h in hits])
    print(f"📄 Found {len(hits)} relevant snippets.")

    prompt_usuario = f"Context:\n{contexto_str}\n\n---\nQuestion: {pergunta}"

    print("⏳ Generating response with RAG...")
    fluxo = ollama.chat(
        model=CHAT_MODEL,
        messages=[{'role': 'system', 'content': SISTEMA_PADRAO},
                  {'role': 'user', 'content': prompt_usuario}],
        stream=True,
        options={'temperature': 0.1, 'num_ctx': 4096}
    )
    
    resposta = ""
    for chunk in fluxo:
        pedaco = chunk['message']['content']
        resposta += pedaco
    salvar_resposta(resposta, "RAG")

def modo_few_shot(solicitacao):
    print("\n🎨 Preparing prompt with Few-Shot...")
    prompt_final = f"Examples (Bad vs Good):\n{exemplos}\n\n---\nTask:\n{solicitacao}"

    print("⏳ Generating response with Few-Shot...")
    fluxo = ollama.chat(
        model=CHAT_MODEL,
        messages=[{'role': 'system', 'content': SISTEMA_PADRAO},
                  {'role': 'user', 'content': prompt_final}],
        stream=True,
        options={'temperature': 0.1, 'num_ctx': 4096}
    )

    resposta = ""
    for chunk in fluxo:
        pedaco = chunk['message']['content']
        resposta += pedaco
    salvar_resposta(resposta, "FEW_SHOT")

def main():
    # CHAMA A VERIFICAÇÃO ASSIM QUE O PROGRAMA COMEÇA
    verificar_indice_inicial()

    while True:
        print("\n=== ANDROID ACCESSIBILITY AGENT ===")
        print("1. RAG Mode")
        print("2. Few-Shot Mode")
        print("0. Exit")
        
        opcao = input("\nOption: ")

        if opcao == "1":
            modo_rag(input("\nQuestion: "))
        elif opcao == "2":
            modo_few_shot(input("\nTask: "))
        elif opcao == "0":
            break
        else:
            print("Invalid option.")
        
        input("\nPress ENTER...")
        limpar_tela()

if __name__ == "__main__":
    main()