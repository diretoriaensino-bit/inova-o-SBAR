import os, smtplib
import google.generativeai as genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_sbar(s, b, a, r):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Avalie esse SBAR de aluno: S:{s}, B:{b}, A:{a}, R:{r}. Seja técnico e construtivo."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro na IA: {e}")
        return "IA falhou."

def criar_pdf(s, b, a, r, feedback):
    # Cria uma folha A4 em branco
    pdf = FPDF()
    pdf.add_page()
    
    # Se a logo existir na pasta, ele coloca no topo!
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=10, y=8, w=30)
    
    # Título do Documento
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 20, "Relatorio Oficial de Avaliacao SBAR", ln=True, align="C")
    pdf.ln(10) # Pula linha
    
    # Escreve o que o aluno mandou
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Dados Enviados pelo Aluno:", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, f"SITUACAO:\n{s}\n\nHISTORICO:\n{b}\n\nAVALIACAO:\n{a}\n\nRECOMENDACAO:\n{r}\n")
    
    # Escreve a resposta da IA
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Feedback do Preceptor IA:", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, feedback)
    
    # Salva o PDF temporariamente
    caminho_pdf = "resultado_sbar.pdf"
    pdf.output(caminho_pdf)
    return caminho_pdf

def send_email(to_email, feedback, s, b, a, r):
    # 1. Monta o PDF primeiro
    arquivo_pdf = criar_pdf(s, b, a, r, feedback)
    
    # 2. Prepara o envelope que aceita anexos (MIMEMultipart)
    msg = MIMEMultipart()
    msg['Subject'] = "Seu Relatório SBAR com IA"
    msg['From'] = os.getenv("SMTP_USER")
    msg['To'] = to_email
    
    # Texto do corpo do e-mail
    corpo = "Ola! Segue em anexo o PDF com a analise do seu SBAR."
    msg.attach(MIMEText(corpo, 'plain'))
    
    # 3. Anexa o PDF no e-mail
    with open(arquivo_pdf, "rb") as f:
        anexo = MIMEApplication(f.read(), _subtype="pdf")
        anexo.add_header('Content-Disposition', 'attachment', filename="Avaliacao_SBAR.pdf")
        msg.attach(anexo)
    
    # 4. Envia pelo Correio (Gmail)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(msg['From'], os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)
        server.quit()
        print("E-mail com PDF enviado com sucesso!")
    except Exception as e:
        print(f"Erro no e-mail: {e}")