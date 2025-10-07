from src.config import get_supabase

class WardrobeDAO:
    def __init__(self):
        self.client = get_supabase()
        self.table = "wardrobe"

    def add_item(self, user_id, name, color, item_type):
        # Find max id for this user_id and increment
        existing_items = self.client.table(self.table).select("id").eq("user_id", user_id).execute().data
        next_id = 1
        if existing_items:
            ids = [item["id"] for item in existing_items]
            next_id = max(ids) + 1

        return self.client.table(self.table).insert({
            "id": next_id,
            "user_id": user_id,
            "name": name,
            "color": color,
            "type": item_type
        }).execute().data

    def list_items(self, user_id):
        return self.client.table(self.table).select("*").eq("user_id", user_id).execute().data

    def search_items(self, user_id, keyword):
        return self.client.table(self.table).select("*").eq("user_id", user_id).ilike("name", f"%{keyword}%").execute().data

    def get_item(self, user_id, item_id):
        result = self.client.table(self.table)\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("id", item_id)\
            .execute()
        return result.data[0] if result.data else None

wardrobe_dao = WardrobeDAO()
