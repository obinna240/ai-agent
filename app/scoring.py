def score_deal(profile, deal):
    """Simple budget + preference scoring."""
    budget = profile.get("travel_constraints", {}).get("budget_total_gbp", 1000)
    price = deal.get("price_gbp", 0)

    try:
        price = float(price)
    except Exception:
        price = 0.0

    if price <= budget:
        budget_score = 1.0
    else:
        budget_score = max(0.0, 1.0 - (price - budget) / budget)

    pref_score = 0.8 if deal.get("provider","") in ["Expedia", "Booking.com"] else 0.6
    final_score = 0.7 * budget_score + 0.3 * pref_score
    deal["score"] = round(final_score * 100, 2)
    return deal
