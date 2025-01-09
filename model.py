from pymongo import MongoClient
from xhtml2pdf import pisa
import os
import webbrowser
import hashlib



def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['curriculumDB']
    return db

class UserModel:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username, password):
        db = get_db()
        users = db['users']

        if users.find_one({"username": username}):
            return False  # Usuário já existe

        hashed_password = UserModel.hash_password(password)
        users.insert_one({"username": username, "password": hashed_password})
        return True

    @staticmethod
    def authenticate_user(username, password):
        db = get_db()
        users = db['users']

        hashed_password = UserModel.hash_password(password)
        user = users.find_one({"username": username, "password": hashed_password})

        return user is not None


class ResumeModel:
    @staticmethod
    def generate_html(data):
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background-color: #ecf0f1;
                    width: 100%; 
                    height: 100%;
                }}
                .container {{
                    width: 80%;
                    height: 100%;
                    margin: auto;
                    padding: 10px;  /* Reduzindo o padding */
                    box-sizing: border-box;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);                }}
                .header {{
                    text-align: center;
                    margin-bottom: 5px;                 
                }}
                .header h1 {{
                    font-size: 24px;  /* Tamanho da fonte ajustado */
                    color: #2c3e50;
                    margin: 0;
                }}
                .header p {{
                    font-size: 14px;
                    color: #7f8c8d;
                    margin: 5px 0;
                }}
                .contact-info {{
                    display: flex;
                    justify-content: center;
                    gap: 10px;  /* Diminuindo o espaço */
                    margin-top: 5px;                
                }}
                .contact-info p {{
                    font-size: 12px;
                    color: #34495e;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .section h2 {{
                    font-size: 18px;  /* Ajuste no tamanho do título */
                    color: #000;
                    border-bottom: 2px solid #000;
                    padding-bottom: 5px;
                    margin-bottom: 10px;                }}
                .card {{
                    background-color: #f4f4f4;
                    border: 1px solid #dcdcdc;
                    border-radius: 10px;
                    padding: 10px;  /* Ajuste no padding */
                    margin-bottom: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);                }}
                .card p {{
                    font-size: 12px;  /* Ajuste no tamanho da fonte */
                    line-height: 1.4;
                    margin: 5px 0;
                    color: #34495e;                }}
                .footer {{
                    text-align: center;
                    font-size: 10px;  /* Ajuste no tamanho da fonte */
                    color: #7f8c8d;
                    margin-top: 20px;                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{data['name']}</h1>
                    <p>{data['job']}</p>
                    <div class="contact-info">
                        <p>Email: {data['email']}</p>
                        <p>Telefone: {data['phone']}</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Resumo Profissional</h2>
                    <div class="card">
                        <p>{data['description']}</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Experiência Profissional</h2>
                    <div class="card">
                        <p>Empresa: {data['company']}</p>
                        <p>Cargo: {data['position']}</p>
                        <p>Período: {data['startdate']} - {data.get('enddate', 'Atual')}</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Formação Acadêmica</h2>
                    <div class="card">
                        <p>Instituição: {data['institution']}</p>
                        <p>Curso: {data['course']}</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Habilidades e Idiomas</h2>
                    <div class="card">
                        <p>Habilidades: {data['skills']}</p>
                        <p>Idiomas: {data['languages']}</p>
                    </div>
                </div>

                <div class="section">
                    <h2>Contato</h2>
                    <div class="card">
                        <p>Endereço: {data['address']}</p>
                        <p>Data de Nascimento: {data['dob']}</p>
                        <p>LinkedIn: {data['linkedin']}</p>
                        <p>GitHub: {data['github']}</p>
                    </div>
                </div>

                <div class="footer">
                    <p>Currículo gerado automaticamente usando sistema online</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    @staticmethod
    def save_html_to_file(html_content, file_path="curriculo_preview.html"):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            webbrowser.open(f"file://{os.path.realpath(file_path)}")
            print(f"Arquivo HTML salvo com sucesso em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo HTML: {e}")

    @staticmethod
    def generate_pdf(data, file_path="curriculo.pdf"):
        html_content = ResumeModel.generate_html(data)
        try:
            with open(file_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
                if pisa_status.err:
                    print("Erro ao gerar PDF")
                else:
                    print(f"PDF gerado com sucesso em: {file_path}")
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")


def save_resume(data):
    db = get_db()
    resumes = db['resumes']
    result = resumes.insert_one(data)
    return result.inserted_id

def get_resume_by_id(resume_id):
    db = get_db()
    resumes = db['resumes']
    resume = resumes.find_one({"_id": resume_id})
    return resume

def generate_resume_pdf(resume_id, file_path):
    resume_data = get_resume_by_id(resume_id)
    return ResumeModel.generate_pdf(resume_data, file_path)
