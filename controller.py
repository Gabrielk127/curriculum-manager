from model import ResumeModel, UserModel



class UserController:
    @staticmethod
    def register_user(username, password):
        return UserModel.register_user(username, password)

    @staticmethod
    def authenticate_user(username, password):
        return UserModel.authenticate_user(username, password)

class ResumeController:
    @staticmethod
    def handle_save_resume(data):
        """
        Gera e salva o currículo em HTML.
        """
        html_content = ResumeModel.generate_html(data)
        ResumeModel.save_html_to_file(html_content)



    @staticmethod
    def handle_export_pdf(data):
        """
        Gera e salva o currículo em PDF.
        """
        file_path = "curriculo.pdf"
        ResumeModel.generate_pdf(data, file_path)
        return file_path

    @staticmethod
    def handle_export_pdf(data):
        """
        Gera e salva o currículo em PDF.
        """
        file_path = "curriculo.pdf"
        ResumeModel.generate_pdf(data, file_path)
        return file_path