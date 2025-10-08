def score_deal(profile, deal):
    # Weights (tune these)
    W_BUDGET = 0.4
    W_PREF = 0.3
    W_DATES = 0.2
    W_MISC = 0.1

    # 1. Budget fit (0..1). If price <= budget -> 1, if > budget by factor -> decays
    budget = float(profile["travel_constraints"]["budget_total_gbp"])
    price = float(deal["price_gbp"])
    if price <= budget:
        budget_score = 1.0
    else:
        # linear decay: if price is twice budget -> score 0
        budget_score = max(0.0, 1.0 - (price - budget) / budget)
    
    # 2. Preference match (0..1). Simple matching example
    pref_score = 0.0
    pref_total = 0
    pref_matches = 0

    prefs = profile["preferences"]
    # check hotel star
    if "hotel" in deal.get("components", {}):
        pref_total += 1
        hotel_stars = deal["components"]["hotel"].get("stars", 0)
        if hotel_stars >= prefs.get("hotel_stars_min", 0):
            pref_matches += 1

    # check car class
    if "car_rental" in deal.get("components", {}):
        pref_total += 1
        car_class = deal["components"]["car_rental"].get("car_class", "")
        if car_class in prefs.get("car_classes", []):
            pref_matches += 1

    # airline preference
    if "flight" in deal.get("components", {}):
        pref_total += 1
        airline = deal["components"]["flight"].get("airline", "")
        if airline in prefs.get("preferred_airlines", []):
            pref_matches += 1

    pref_score = (pref_matches / pref_total) if pref_total > 0 else 0.5

    # 3. Dates proximity (0..1) — if within flexible window
    from datetime import datetime, timedelta
    desired_depart = datetime.fromisoformat(profile["travel_constraints"]["dates"]["depart"])
    actual_depart = datetime.fromisoformat(deal["components"]["flight"]["depart"]) if "flight" in deal.get("components", {}) else desired_depart
    flex_days = int(profile["travel_constraints"]["dates"].get("flex_days", 0))
    delta_days = abs((actual_depart - desired_depart).days)
    dates_score = 1.0 if delta_days <= flex_days else max(0.0, 1.0 - (delta_days - flex_days)/30.0)

    # 4. misc: availability, cancellation policy etc. (0..1)
    misc_score = 1.0 if deal.get("components", {}).get("hotel", {}).get("free_cancel", False) else 0.8

    final_score = (
        W_BUDGET * budget_score +
        W_PREF * pref_score +
        W_DATES * dates_score +
        W_MISC * misc_score
    )
    # normalize to 0..100
    return round(final_score * 100, 2)