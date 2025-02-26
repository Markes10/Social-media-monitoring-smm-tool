@router.post("/subscribe")
def subscribe(agency_id: int, plan_id: int, db: Session = Depends(get_db)):
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()

    if not agency or not plan:
        return {"message": "Invalid agency or plan"}

    # Simulate payment processing (Stripe, PayPal, etc.)
    return {"message": f"Agency {agency.name} subscribed to {plan.name} for ${plan.price}"}
