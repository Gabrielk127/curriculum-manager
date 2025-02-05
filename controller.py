from model import ResumeModel, UserModel

class UserController:
    def user_register(username, password):
        return UserModel.user_register(username, password)

    def user_authenticate(username, password):
        return UserModel.user_authenticate(username, password)

class ResumeController:
    def handle_save_resume(data, username):
            data['username'] = username  
            resume_id = ResumeModel.save_resume(data, username) 
            html_content = ResumeModel.generate_html(data)  
            ResumeModel.save_html_to_file(html_content)  
            return resume_id

    def export_pdf(data):
        file_path = f"{data['name']}_curriculo.pdf"
        ResumeModel.generate_pdf(data, file_path)
        return file_path

    def list_resumes(username):
        return ResumeModel.all_resumes(username)
