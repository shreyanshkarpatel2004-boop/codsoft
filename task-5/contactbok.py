#!/usr/bin/env python3
"""
Contact Book

Features:
- Store name, phone number, email, and address for each contact.
- Add, view, search (by name or phone), update, and delete contacts.
- JSON persistence to `contacts.json` in the same folder.
- Simple CLI user-friendly menu.

Usage: run `python contactbok.py` and follow the menu prompts.
"""

import json
import os
import re
import argparse
from typing import List, Dict, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), "contacts.json")


def load_contacts(path: str = DATA_FILE) -> List[Dict[str, Any]]:
	if not os.path.exists(path):
		return []
	try:
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception:
		return []


def save_contacts(contacts: List[Dict[str, Any]], path: str = DATA_FILE) -> None:
	tmp = path + ".tmp"
	with open(tmp, "w", encoding="utf-8") as f:
		json.dump(contacts, f, indent=2, ensure_ascii=False)
	os.replace(tmp, path)


def validate_phone(phone: str) -> bool:
	s = re.sub(r"[\s\-()]+", "", phone)
	return s.isdigit() and 5 <= len(s) <= 15


def validate_email(email: str) -> bool:
	if not email:
		return True
	return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


def add_contact(contacts: List[Dict[str, Any]]) -> None:
	print("\nAdd New Contact")
	name = input("Name: ").strip()
	if not name:
		print("Name is required.")
		return
	phone = input("Phone: ").strip()
	if not validate_phone(phone):
		print("Invalid phone number. Keep digits and common separators, min 5 digits.")
		return
	email = input("Email (optional): ").strip()
	if not validate_email(email):
		print("Invalid email address.")
		return
	address = input("Address (optional): ").strip()

	contact = {"name": name, "phone": phone, "email": email, "address": address}
	contacts.append(contact)
	save_contacts(contacts)
	print("Contact saved.")


def print_contact(contact: Dict[str, Any], idx: int = None) -> None:
	prefix = f"[{idx}] " if idx is not None else ""
	print(f"{prefix}{contact.get('name')} — {contact.get('phone')}")
	if contact.get("email"):
		print(f"    Email: {contact.get('email')}")
	if contact.get("address"):
		print(f"    Address: {contact.get('address')}")


def view_contacts(contacts: List[Dict[str, Any]]) -> None:
	print("\nContact List")
	if not contacts:
		print("No contacts found.")
		return
	for i, c in enumerate(contacts, start=1):
		print_contact(c, i)


def search_contacts(contacts: List[Dict[str, Any]]) -> List[int]:
	query = input("Enter name or phone to search: ").strip().lower()
	if not query:
		print("Empty search.")
		return []
	results = []
	for i, c in enumerate(contacts, start=1):
		if query in (c.get("name") or "").lower() or query in (c.get("phone") or "").lower():
			results.append(i)
	if not results:
		print("No matches found.")
	else:
		print(f"Found {len(results)} match(es):")
		for idx in results:
			print_contact(contacts[idx - 1], idx)
	return results


def choose_contact_index(contacts: List[Dict[str, Any]], prompt: str = "Select contact number: ") -> int:
	if not contacts:
		print("No contacts available.")
		return -1
	view_contacts(contacts)
	try:
		s = input(prompt).strip()
		if not s:
			return -1
		idx = int(s)
		if 1 <= idx <= len(contacts):
			return idx - 1
	except ValueError:
		pass
	print("Invalid selection.")
	return -1


def update_contact(contacts: List[Dict[str, Any]]) -> None:
	print("\nUpdate Contact")
	matches = search_contacts(contacts)
	if not matches:
		return
	try:
		sel = int(input("Enter match number to update (e.g. 1 for first shown): ").strip())
	except Exception:
		print("Invalid input.")
		return
	if sel < 1 or sel > len(matches):
		print("Selection out of range.")
		return
	idx = matches[sel - 1] - 1
	contact = contacts[idx]
	print("Leave blank to keep current value.")
	name = input(f"Name [{contact.get('name')}]: ").strip() or contact.get('name')
	phone = input(f"Phone [{contact.get('phone')}]: ").strip() or contact.get('phone')
	if not validate_phone(phone):
		print("Invalid phone number.")
		return
	email = input(f"Email [{contact.get('email','')}]: ").strip() or contact.get('email')
	if not validate_email(email):
		print("Invalid email.")
		return
	address = input(f"Address [{contact.get('address','')}]: ").strip() or contact.get('address')

	contact.update({"name": name, "phone": phone, "email": email, "address": address})
	save_contacts(contacts)
	print("Contact updated.")


def delete_contact(contacts: List[Dict[str, Any]]) -> None:
	print("\nDelete Contact")
	matches = search_contacts(contacts)
	if not matches:
		return
	try:
		sel = int(input("Enter match number to delete (e.g. 1 for first shown): ").strip())
	except Exception:
		print("Invalid input.")
		return
	if sel < 1 or sel > len(matches):
		print("Selection out of range.")
		return
	idx = matches[sel - 1] - 1
	print_contact(contacts[idx], idx + 1)
	confirm = input("Type 'yes' to confirm delete: ").strip().lower()
	if confirm == "yes":
		contacts.pop(idx)
		save_contacts(contacts)
		print("Contact deleted.")
	else:
		print("Delete cancelled.")


def clear_screen() -> None:
	os.system('cls' if os.name == 'nt' else 'clear')


def main_menu() -> None:
	contacts = load_contacts()
	while True:
		print("\n--- Contact Book ---")
		print("1) Add Contact")
		print("2) View Contact List")
		print("3) Search Contact")
		print("4) Update Contact")
		print("5) Delete Contact")
		print("6) Exit")
		choice = input("Choose an option (1-6): ").strip()
		if choice == "1":
			add_contact(contacts)
		elif choice == "2":
			view_contacts(contacts)
		elif choice == "3":
			search_contacts(contacts)
		elif choice == "4":
			update_contact(contacts)
		elif choice == "5":
			delete_contact(contacts)
		elif choice == "6":
			print("Goodbye.")
			break
		else:
			print("Invalid choice. Please choose 1-6.")


def parse_args():
	p = argparse.ArgumentParser(add_help=False)
	p.add_argument('-v', '--version', action='store_true', help='show version and exit')
	args, _ = p.parse_known_args()
	return args


if __name__ == '__main__':
	args = parse_args()
	if args.version:
		print("Contact Book v1.0")
	else:
		try:
			main_menu()
		except KeyboardInterrupt:
			print("\nExiting.")

