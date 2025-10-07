from src.dao.wardrobe_dao import wardrobe_dao

class WardrobeService:
    def add_item(self, user_id, name, color, item_type):
        return wardrobe_dao.add_item(user_id, name, color, item_type)

    def list_items(self, user_id):
        return wardrobe_dao.list_items(user_id)

    def search_items(self, user_id, keyword):
        return wardrobe_dao.search_items(user_id, keyword)

wardrobe_service = WardrobeService()
