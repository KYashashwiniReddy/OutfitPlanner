from src.config import get_supabase

class PlanDAO:
    def __init__(self):
        self.client = get_supabase()
        self.table = "plans"

    def add_plan(self, user_id, outfit_id, plan_date):
        # Get next plan id for this user
        existing_ids = self.client.table(self.table).select("id").eq("user_id", user_id).execute().data
        next_id = 1
        if existing_ids:
            ids = [p["id"] for p in existing_ids]
            next_id = max(ids) + 1

        data = {
            "id": next_id,
            "user_id": user_id,
            "outfit_id": outfit_id,
            "date": plan_date
        }

        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return response.data[0]
        else:
            raise ValueError("Failed to insert plan into Supabase.")

    def list_plans(self, user_id, limit=100):
        response = self.client.table(self.table).select("*").eq("user_id", user_id).limit(limit).execute()
        return response.data

    def search_plans(self, user_id, keyword):
        response = self.client.table(self.table).select("*").eq("user_id", user_id).execute()
        keyword_lower = keyword.lower()
        results = [
            p for p in response.data
            if keyword_lower in str(p.get("date", "")).lower()
        ]
        return results


plan_dao = PlanDAO()
