import os
from dotenv import load_dotenv
import google.generativeai as genai

print("--- INICIANDO TESTE DA IA ---")

# Tenta ler o arquivo .env
load_dotenv()
chave = os.getenv("GEMINI_API_KEY")

if not chave:
    print("ERRO 1: O Python não achou a variável GEMINI_API_KEY dentro do arquivo .env.")
else:
    print(f"Sucesso: Achei a chave! Ela começa com: {chave[:8]}...")
    
    try:
        print("Batendo na porta do Google...")
        genai.configure(api_key=chave)
        model = genai.GenerativeModel('gemini-2.5-flash')
        resposta = model.generate_content("Diga apenas a frase: Estou vivo e funcionando.")
        
        print("\nRESPOSTA DO GEMINI:")
        print(resposta.text)
        print("--- TESTE PERFEITO ---")
        
    except Exception as e:
        print("\n--- DEU ERRO LÁ NO GOOGLE ---")
        print(f"O motivo exato é esse aqui: {e}")