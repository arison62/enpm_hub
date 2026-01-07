import json
import random

def generate_fake_users(num_users=5):
    roles = ["user", "admin_site", "super_admin"]
    statuts = ["etudiant", "alumni", "enseignant", "personnel_admin", "partenaire"]
    
    users = []
    for i in range(1, num_users + 1):
        has_email = random.choice([True, False])
        has_telephone = not has_email if random.random() < 0.2 else True  # Ensure at least one
        
        user = {
            "email": f"user{i}@example.com" if has_email else None,
            "telephone": f"+2376500188{i:02d}" if has_telephone else None,
            "password": f"password{i:03d}",
            "role_systeme": random.choice(roles),
            "est_actif": random.choice([True, False]),
            "profil": {
                "nom_complet": f"User Name {i}",
                "statut_global": random.choice(statuts),
                "adresse": f"Address {i}",
                "telephone": f"+2376500188{i:02d}",
                "ville": f"City {i}",
                "pays": "US",
                "bio": f"Bio for user {i}"
            }
        }
        # Ensure not both email and telephone empty (though logic above prevents it)
        if not user["email"] and not user["telephone"]:
            user["email"] = f"default{i}@example.com"
        
        users.append(user)
    
    payload = {
        "users": users,
        "mode": "strict",
        "batch_size": 100
    }
    
    return json.dumps(payload, indent=2)

# Generate and print
print(generate_fake_users(99))