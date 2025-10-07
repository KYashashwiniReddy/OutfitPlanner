from src.config import get_supabase

class UserDAO:
    def __init__(self):
        self.client = get_supabase()
        self.table = "users"

    def add_user(self, name, email):
        result = self.client.table(self.table).insert({
            "name": name,
            "email": email
        }).execute()
        return result.data[0]

    def get_user_by_email(self, email):
        result = self.client.table(self.table).select("*").eq("email", email).execute()
        return result.data[0] if result.data else None

    def get_user(self, user_id):
        result = self.client.table(self.table).select("*").eq("id", user_id).execute()
        return result.data[0] if result.data else None

user_dao = UserDAO()
