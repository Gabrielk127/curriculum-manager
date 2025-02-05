import flet as ft
from controller import UserController, ResumeController

def render_auth_form(page):

    def on_register(e):
        username = username_input.value
        password = password_input.value

        if UserController.user_register(username, password):
            page.add(ft.Text("Usuário cadastrado com sucesso! Faça login."))
        else:
            page.add(ft.Text("Erro: Usuário já existe."))

    def on_login(e):
        username = username_input.value
        password = password_input.value

        if UserController.user_authenticate(username, password):
            page.add(ft.Text("Login bem-sucedido!"))
            page.clean()
            render_form(page, username) 
        else:
            page.add(ft.Text("Erro: Credenciais inválidas."))

    username_input = ft.TextField(label="Usuário")
    password_input = ft.TextField(label="Senha", password=True)

    register_button = ft.ElevatedButton("Registrar", on_click=on_register)
    login_button = ft.ElevatedButton("Login", on_click=on_login)

    form_content = ft.Column(
        [
            ft.Text("Autenticação de Usuário", size=24),
            username_input,
            password_input,
            register_button,
            login_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(form_content)

def render_form(page, username):

    Title = ft.Container(
        content=ft.Text("Preencha os campos abaixo para criar o seu currículo:", size=32),
        padding=ft.Padding(left=0, top=10, right=0, bottom=40)
    )

    Title_company = ft.Container(
        content=ft.Text('Experiência Profissional', size=24),
        padding=ft.Padding(left=0, top=30, right=10, bottom=30)
    )

    Title_intitution = ft.Container(
        content=ft.Text('Formação Acadêmica', size=24),
        padding=ft.Padding(left=0, top=30, right=10, bottom=30)
    )

    Title_skills = ft.Container(
        content=ft.Text('Habilidades', size=24),
        padding=ft.Padding(left=0, top=30, right=10, bottom=30)
    )

    Title_social = ft.Container(
        content=ft.Text("Redes Sociais:", size=24),
        padding=ft.Padding(left=0, top=30, right=0, bottom=30)
    )

    name_input = ft.TextField(label="Nome Completo")
    email_input = ft.TextField(label="Email")
    phone_input = ft.TextField(label="Telefone")
    job_input = ft.TextField(label="Cargo Desejado")
    description_input = ft.TextField(label="Resumo Profissional", multiline=True)
    address_input = ft.TextField(label="Endereço")
    dob_input = ft.TextField(label="Data de Nascimento")

    company_input = ft.TextField(label="Empresa")
    position_input = ft.TextField(label='Cargo')
    start_date_input = ft.TextField(label='Data de Início')
    end_date_input = ft.TextField(label='Data de Término')

    institution_input = ft.TextField(label='Instituição')
    course_input = ft.TextField(label='Curso')

    skills_input = ft.TextField(label='Habilidades Técnicas')
    languages_input = ft.TextField(label='Idiomas')

    linkedin_input = ft.TextField(label="LinkedIn")
    github_input = ft.TextField(label="GitHub")

    def get_data():
        return{
            "name": name_input.value,
            "email": email_input.value,
            "phone": phone_input.value,
            "job": job_input.value,
            "description": description_input.value,
            "address": address_input.value,
            "dob": dob_input.value,
            "linkedin": linkedin_input.value,
            "github": github_input.value,
            "company": company_input.value,
            'position': position_input.value,
            'startdate': start_date_input.value,
            'institution': institution_input.value,
            'course': course_input.value,
            "skills": skills_input.value,
            "languages": languages_input.value
        }

    def on_save(e):
        data = get_data() 
        try:
            resume_id = ResumeController.handle_save_resume(data, username)  
            page.add(ft.Text(f"Currículo gerado com ID: {resume_id}"))
        except Exception as ex:
            page.add(ft.Text(f"Erro ao gerar currículo: {ex}"))

    def on_export(e):
        data = get_data()
        file_path = ResumeController.export_pdf(data)
        page.add(ft.Text(f"Currículo exportado para: {file_path}"))

    save_button = ft.Container(
        content=ft.ElevatedButton("Gerar Currículo", on_click=on_save),
        padding=ft.Padding(left=0, top=30, right=0, bottom=30)
    )

    export_button = ft.Container(
        content=ft.ElevatedButton("Exportar para PDF", on_click=on_export),
        padding=ft.Padding(left=0, top=30, right=0, bottom=30)
    )

    view_list_button = ft.Container(
        content=ft.ElevatedButton("Ver Currículos Gerados", on_click=lambda e: render_resume_list(page, username)),
        padding=ft.Padding(left=0, top=30, right=0, bottom=30)
    )

    list_view_content = ft.ListView(
        controls=[
            Title, name_input, email_input, phone_input, job_input, description_input, address_input, dob_input,
            Title_company, company_input, position_input, start_date_input, end_date_input,
            Title_intitution, institution_input, course_input,
            Title_skills, skills_input, languages_input,
            Title_social, linkedin_input, github_input,
            save_button, export_button, view_list_button
        ],
        height=800,
        width=800
    )

    centered_content = ft.Container(
        content=list_view_content,
        alignment=ft.alignment.center
    )

    page.add(centered_content)

def render_resume_list(page, username):
    resumes = ResumeController.list_resumes(username)

    def export_resume(e):
        resume_id = e.control.data
        resume = next(r for r in resumes if str(r['_id']) == resume_id)
        file_path = f"{resume['name']}_curriculo.pdf"
        ResumeController.export_pdf(resume)
        page.add(ft.Text(f"Currículo exportado para: {file_path}"))

    resume_cards = []
    for resume in resumes:
        card = ft.Card(
            content=ft.Column(
                [
                    ft.Text(f"Nome: {resume['name']}"),
                    ft.Text(f"Cargo: {resume['job']}"),
                    ft.ElevatedButton("Exportar PDF", on_click=export_resume, data=str(resume['_id']))
                ]
            )
        )
        resume_cards.append(card)
    
    page.clean()

    back_button = ft.ElevatedButton("Voltar", on_click=lambda e: go_back(e, page, username))
   
    
    page.add(ft.ListView(controls=resume_cards + [back_button], height=600, width=800))

def go_back(e, page, username):
    page.clean()
    render_form(page, username)

    

