from src.config import get_supabase
from src.dao.wardrobe_dao import wardrobe_dao

class OutfitDAO:
    def __init__(self):
        self.client = get_supabase()
        self.table = "outfits"

    def add_outfit(self, user_id, name, occasion=None, item_ids=None):
        if not item_ids:
            raise ValueError("No wardrobe items provided.")

        # Verify ownership of each wardrobe item
        items = []
        for item_id in item_ids:
            item = wardrobe_dao.get_item(user_id, item_id)
            if not item:
                raise ValueError(f"Wardrobe item ID {item_id} does not belong to user {user_id}.")
            items.append({"name": item["name"]})  # Only store names

        # Get next outfit ID for this user
        existing_ids = self.client.table(self.table).select("id").eq("user_id", user_id).execute().data
        next_id = 1
        if existing_ids:
            ids = [o["id"] for o in existing_ids]
            next_id = max(ids) + 1

        data = {
            "id": next_id,
            "user_id": user_id,
            "name": name,
            "occasion": occasion,
            "items": items  # store only names
        }

        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return response.data[0]
        else:
            raise ValueError("Failed to insert outfit into Supabase.")

    def list_outfits(self, user_id, limit=100):
        response = self.client.table(self.table).select("*").eq("user_id", user_id).limit(limit).execute()
        results = []
        for o in response.data:
            unique_names = list(set(item["name"] for item in o.get("items", [])))  # convert to set for uniqueness
            results.append({
                "id": o["id"],
                "user_id": o["user_id"],
                "name": o["name"],
                "occasion": o.get("occasion"),
                "created_at": o.get("created_at"),
                "items": unique_names
            })
        return results

    def search_outfits(self, user_id, keyword):
        response = self.client.table(self.table).select("*").eq("user_id", user_id).execute()
        keyword_lower = keyword.lower()
        results = []
        for o in response.data:
            if keyword_lower in o["name"].lower() or (o.get("occasion") and keyword_lower in o["occasion"].lower()):
                unique_names = list(set(item["name"] for item in o.get("items", [])))
                results.append({
                    "id": o["id"],
                    "user_id": o["user_id"],
                    "name": o["name"],
                    "occasion": o.get("occasion"),
                    "created_at": o.get("created_at"),
                    "items": unique_names
                })
        return results


outfit_dao = OutfitDAO()
