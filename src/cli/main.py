# src/cli/main.py
import argparse
import json
from src.config import get_supabase
#supabase = get_supabase()
from src.services.user_service import user_service
from src.dao.user_dao import user_dao
from src.services.wardrobe_service import wardrobe_service
from src.dao.wardrobe_dao import wardrobe_dao
from src.services.outfit_service import outfit_service
from src.dao.outfit_dao import outfit_dao
from src.services.plan_service import plan_service
from src.dao.plan_dao import plan_dao

class OutfitCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="outfit-cli")
        self.sub = self.parser.add_subparsers(dest="cmd")
        self._setup_user_commands()
        self._setup_wardrobe_commands()
        self._setup_outfit_commands()
        self._setup_plan_commands()

    # --- USERS ---
    def _setup_user_commands(self):
        p_user = self.sub.add_parser("user", help="user commands")
        user_sub = p_user.add_subparsers(dest="action")

        addu = user_sub.add_parser("add")
        addu.add_argument("--name", required=True)
        addu.add_argument("--email", required=True)
        addu.set_defaults(func=self._cmd_user_add)

        listu = user_sub.add_parser("list")
        listu.set_defaults(func=self._cmd_user_list)

    def _cmd_user_add(self, args):
        user = user_service.add_user(name=args.name, email=args.email)
        print("Created user:", json.dumps(user, indent=2, default=str))

    def _cmd_user_list(self, args):
        users = user_dao.list_users(limit=100)
        print(json.dumps(users, indent=2, default=str))

    # --- WARDROBE ---
    def _setup_wardrobe_commands(self):
        p_ward = self.sub.add_parser("wardrobe", help="wardrobe commands")
        ward_sub = p_ward.add_subparsers(dest="action")

        addw = ward_sub.add_parser("add")
        addw.add_argument("--user_id", type=int, required=True)
        addw.add_argument("--name", required=True)
        addw.add_argument("--color", default=None)
        addw.add_argument("--type", default=None)
        addw.set_defaults(func=self._cmd_wardrobe_add)

        listw = ward_sub.add_parser("list")
        listw.add_argument("--user_id", type=int, required=True)
        listw.set_defaults(func=self._cmd_wardrobe_list)

        searchw = ward_sub.add_parser("search")
        searchw.add_argument("--user_id", type=int, required=True)
        searchw.add_argument("--keyword", required=True)
        searchw.set_defaults(func=self._cmd_wardrobe_search)

    def _cmd_wardrobe_add(self, args):
        item = wardrobe_service.add_item(
            user_id=args.user_id, name=args.name, color=args.color, type=args.type
        )
        print("Added wardrobe item:", json.dumps(item, indent=2, default=str))

    def _cmd_wardrobe_list(self, args):
        items = wardrobe_dao.list_items(user_id=args.user_id, limit=100)
        print(json.dumps(items, indent=2, default=str))

    def _cmd_wardrobe_search(self, args):
        items = wardrobe_service.search_items(user_id=args.user_id, keyword=args.keyword)
        print(f"Search results for '{args.keyword}':")
        for i in items:
            print(i)

    # --- OUTFITS ---
    def _setup_outfit_commands(self):
        p_outfit = self.sub.add_parser("outfit", help="outfit commands")
        outfit_sub = p_outfit.add_subparsers(dest="action")

        addo = outfit_sub.add_parser("add")
        addo.add_argument("--user_id", type=int, required=True)
        addo.add_argument("--name", required=True)
        addo.add_argument("--occasion", default=None)
        addo.add_argument("--item_ids", default=None, help="Comma separated wardrobe item IDs")
        addo.set_defaults(func=self._cmd_outfit_add)

        listo = outfit_sub.add_parser("list")
        listo.add_argument("--user_id", type=int, required=True)
        listo.set_defaults(func=self._cmd_outfit_list)

        searcho = outfit_sub.add_parser("search")
        searcho.add_argument("--user_id", type=int, required=True)
        searcho.add_argument("--keyword", required=True)
        searcho.set_defaults(func=self._cmd_outfit_search)

    def _cmd_outfit_add(self, args):
        try:
            item_ids = None
            if args.item_ids:
                item_ids = [int(i.strip()) for i in args.item_ids.split(",") if i.strip()]

            outfit = outfit_service.add_outfit(
                user_id=args.user_id, name=args.name, occasion=args.occasion, item_ids=item_ids
            )
            print("Created outfit:", json.dumps(outfit, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def _cmd_outfit_list(self, args):
        outfits = outfit_dao.list_outfits(user_id=args.user_id, limit=100)
        print(json.dumps(outfits, indent=2, default=str))

    def _cmd_outfit_search(self, args):
        outfits = outfit_service.search_outfits(user_id=args.user_id, keyword=args.keyword)
        print(f"Search results for '{args.keyword}':")
        for o in outfits:
            print(o)

    # --- PLANS ---
    def _setup_plan_commands(self):
        p_plan = self.sub.add_parser("plan", help="plan commands")
        plan_sub = p_plan.add_subparsers(dest="action")

        addp = plan_sub.add_parser("add")
        addp.add_argument("--user_id", type=int, required=True)
        addp.add_argument("--outfit_id", type=int, required=True)
        addp.add_argument("--date", required=True)
        addp.set_defaults(func=self._cmd_plan_add)

        listp = plan_sub.add_parser("list")
        listp.add_argument("--user_id", type=int, required=True)
        listp.set_defaults(func=self._cmd_plan_list)

    def _cmd_plan_add(self, args):
        plan = plan_service.add_plan(
            user_id=args.user_id, outfit_id=args.outfit_id, date=args.date
        )
        print("Created plan:", json.dumps(plan, indent=2, default=str))

    def _cmd_plan_list(self, args):
        plans = plan_dao.list_plans(user_id=args.user_id, limit=100)
        print(json.dumps(plans, indent=2, default=str))

    # --- RUN ---
    def run(self):
        import sys
        if len(sys.argv) > 1:
            args = self.parser.parse_args()
            if hasattr(args, "func"):
                args.func(args)
            else:
                self.parser.print_help()
        else:
            self.interactive_menu()

    # --- INTERACTIVE MENU ---
    def interactive_menu(self):
        while True:
            print("\n--- Outfit Planner Menu ---")
            print("1. Manage Wardrobe Items")
            print("2. Manage Outfits")
            print("3. Plan Outfits")
            print("4. View Planned Outfits")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.wardrobe_menu()
            elif choice == "2":
                self.outfit_menu()
            elif choice == "3":
                self.plan_menu()
            elif choice == "4":
                self.view_plans()
            elif choice == "5":
                print("Exiting Outfit Planner. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    # --- INTERACTIVE SUBMENUS ---
    def wardrobe_menu(self):
        while True:
            print("\n--- Wardrobe Menu ---")
            print("1. Add Wardrobe Item")
            print("2. List Wardrobe Items")
            print("3. Search Wardrobe Items")
            print("4. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                user_id = int(input("User ID: "))
                name = input("Item Name: ")
                type_ = input("Type: ")
                color = input("Color: ")
                wardrobe_service.add_item(user_id, name, color, type_)
                print("Item added.")
            elif choice == "2":
                user_id = int(input("User ID: "))
                items = wardrobe_dao.list_items(user_id=user_id, limit=100)
                for i in items:
                    print(i)
            elif choice == "3":
                user_id = int(input("User ID: "))
                keyword = input("Enter keyword to search: ")
                results = wardrobe_service.search_items(user_id, keyword)
                for r in results:
                    print(r)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def outfit_menu(self):
        while True:
            print("\n--- Outfit Menu ---")
            print("1. Create Outfit")
            print("2. List Outfits")
            print("3. Search Outfits")
            print("4. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                user_id = int(input("User ID: "))
                name = input("Outfit Name: ")
                occasion = input("Occasion: ")
                ids_input = input("Enter wardrobe item IDs (comma separated) to include: ")
                item_ids = [int(i.strip()) for i in ids_input.split(",") if i.strip()]
                try:
                    outfit_service.add_outfit(user_id, name, occasion, item_ids)
                    print("Outfit created.")
                except Exception as e:
                    print("Error:", e)
            elif choice == "2":
                user_id = int(input("User ID: "))
                outfits = outfit_dao.list_outfits(user_id=user_id, limit=100)
                for o in outfits:
                    print(o)
            elif choice == "3":
                user_id = int(input("User ID: "))
                keyword = input("Enter keyword to search: ")
                results = outfit_service.search_outfits(user_id, keyword)
                for r in results:
                    print(r)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def plan_menu(self):
        while True:
            print("\n--- Plan Menu ---")
            print("1. Schedule Outfit")
            print("2. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                user_id = int(input("User ID: "))
                outfit_id = int(input("Outfit ID: "))
                date = input("Date (YYYY-MM-DD): ")
                plan_service.add_plan(user_id, outfit_id, date)
                print("Outfit scheduled.")
            elif choice == "2":
                break
            else:
                print("Invalid choice.")

    def view_plans(self):
        user_id = int(input("User ID to view plans: "))
        plans = plan_dao.list_plans(user_id=user_id, limit=100)
        for p in plans:
            print(p)


if __name__ == "__main__":
    cli = OutfitCLI()
    cli.run()
