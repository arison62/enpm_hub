from django.utils import timezone
from datetime import date, datetime
from django.utils.translation import gettext as _

def format_linkedin_duration(start_date, end_date=None):
    """
    Calcule la durée entre deux dates et la formate façon LinkedIn.
    Si end_date est None, utilise la date actuelle (pour les posts ou postes actuels).
    """
    if not start_date:
        return None
        
    # Conversion en datetime si on reçoit des objets date
    if isinstance(start_date, date) and not isinstance(start_date, datetime):
        start_date = datetime.combine(start_date, datetime.min.time())
    
    now = timezone.now() if timezone.is_aware(start_date) else datetime.now()
    
    reference_date = end_date or now
    if isinstance(reference_date, date) and not isinstance(reference_date, datetime):
        reference_date = datetime.combine(reference_date, datetime.min.time())

    delta = reference_date - start_date
    
    seconds = delta.total_seconds()
    
    # Logique de calcul progressive
    if seconds < 60:
        return _("À l'instant")
    
    minutes = seconds // 60
    if minutes < 60:
        return f"{int(minutes)} min"
        
    hours = minutes // 60
    if hours < 24:
        return f"{int(hours)} h"
        
    days = delta.days
    if days < 7:
        return f"{days} j"
        
    weeks = days // 7
    if days < 30:
        return f"{int(weeks)} sem"
        
    months = days // 30
    if months < 12:
        return f"{int(months)} mois"
        
    years = months // 12
    remaining_months = int(months % 12)
    
    year_str = f"{int(years)} an" + ("s" if years > 1 else "")
    if remaining_months > 0:
        return f"{year_str} {remaining_months} mois"
    return year_str