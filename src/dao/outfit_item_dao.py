# src/dao/outfit_item_dao.py
from src.config import get_supabase

class OutfitItemDAO:
    def __init__(self):
        self.client = get_supabase()
        self.table = "outfit_items"
    def add_outfit_item(self, outfit_id, wardrobe_id):
        data = {"outfit_id": outfit_id, "wardrobe_id": wardrobe_id}
        return self.client.table(self.table).insert(data).execute().data[0]
    def list_outfit_items(self, outfit_id):
        return (
            self.client.table(self.table)
            .select("*")
            .eq("outfit_id", outfit_id)
            .execute()
            .data
        )
outfit_item_dao = OutfitItemDAO()