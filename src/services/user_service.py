from src.dao.user_dao import user_dao

class UserService:
    def add_user(self, name, email):
        existing_user = user_dao.get_user_by_email(email)
        if existing_user:
            return {"message": "User already exists", "user": existing_user}
        return user_dao.add_user(name, email)

    def get_user(self, user_id):
        return user_dao.get_user(user_id)

user_service = UserService()
