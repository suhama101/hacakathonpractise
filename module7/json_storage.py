# import json
# import os
# from datetime import datetime

# class ChatHistory:
#     def __init__(self, filename="chat_history.json"):
#         self.filename = filename
#         if not os.path.exists(filename):
#             with open(filename, "w") as f:
#                 json.dump([], f)
    
#     def save_message(self, role, content, session_id="default"):
#         """Ek message save karo"""
#         history = self.load_all()
        
#         history.append({
#             "session_id": session_id,
#             "role": role,
#             "content": content,
#             "time": datetime.now().strftime("%H:%M:%S"),
#             "date": datetime.now().strftime("%Y-%m-%d")
#         })
        
#         with open(self.filename, "w") as f:
#             json.dump(history, f, indent=4)
    
#     def load_session(self, session_id="default"):
#         """Ek session ki history lo"""
#         history = self.load_all()
#         return [m for m in history if m["session_id"] == session_id]
    
#     def load_all(self):
#         """Sab history lo"""
#         try:
#             with open(self.filename, "r") as f:
#                 return json.load(f)
#         except:
#             return []
    
#     def clear_session(self, session_id="default"):
#         """Session clear karo"""
#         history = self.load_all()
#         history = [m for m in history if m["session_id"] != session_id]
#         with open(self.filename, "w") as f:
#             json.dump(history, f, indent=4)
    
#     def get_stats(self):
#         """Statistics"""
#         history = self.load_all()
#         return {
#             "total_messages": len(history),
#             "sessions": len(set(m["session_id"] for m in history))
#         }

# # ==================
# # TEST
# # ==================
# chat = ChatHistory()

# chat.save_message("user", "Python kya hai?")
# chat.save_message("assistant", "Python ek programming language hai!")
# chat.save_message("user", "Loops explain karo")
# chat.save_message("assistant", "Loops code ko repeat karte hain...")

# # Load karo
# session = chat.load_session()
# print("Chat History:")
# for msg in session:
#     print(f"  [{msg['time']}] {msg['role']}: {msg['content'][:40]}...")

# # Stats
# stats = chat.get_stats()
# print(f"\nTotal messages: {stats['total_messages']}")


import json
import os
from datetime import datetime

# ==================
# JSON STORAGE CLASS
# ==================

class DataStorage:
    def __init__(self, filename):
        self.filename = filename
        # File nahi hai to banao
        if not os.path.exists(filename):
            self._save({})
    
    def _load(self):
        """File se data load karo"""
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def _save(self, data):
        """Data file mein save karo"""
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
    
    def set(self, key, value):
        """Data save karo"""
        data = self._load()
        data[key] = value
        self._save(data)
    
    def get(self, key):
        """Data lo"""
        data = self._load()
        return data.get(key, None)
    
    def delete(self, key):
        """Data hata do"""
        data = self._load()
        if key in data:
            del data[key]
            self._save(data)
    
    def get_all(self):
        """Sab data lo"""
        return self._load()

# ==================
# TEST KARO
# ==================

db = DataStorage("mydata.json")

# Save karo
db.set("user_001", {
    "name": "Suhama",
    "city": "Lahore",
    "joined": datetime.now().strftime("%Y-%m-%d")
})

db.set("user_002", {
    "name": "Ali",
    "city": "Karachi",
    "joined": datetime.now().strftime("%Y-%m-%d")
})

# Load karo
user = db.get("user_001")
print(f"User: {user['name']} from {user['city']}")

# Sab dekho
all_data = db.get_all()
print(f"\nTotal users: {len(all_data)}")
for uid, info in all_data.items():
    print(f"  {uid}: {info['name']}")