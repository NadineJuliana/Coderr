from offers_app.models import Offer, OfferDetail


def create_offer_with_details(user):
    offer = Offer.objects.create(
        user=user,
        title="Website Design",
        description="Professionelles Website-Design",
    )

    basic = OfferDetail.objects.create(
        offer=offer,
        title="Basic Design",
        revisions=2,
        delivery_time_in_days=5,
        price=100,
        features=["Logo Design", "Visitenkarte"],
        offer_type="basic",
    )

    standard = OfferDetail.objects.create(
        offer=offer,
        title="Standard Design",
        revisions=5,
        delivery_time_in_days=7,
        price=200,
        features=[
            "Logo Design",
            "Visitenkarte",
            "Briefpapier",
        ],
        offer_type="standard",
    )

    premium = OfferDetail.objects.create(
        offer=offer,
        title="Premium Design",
        revisions=10,
        delivery_time_in_days=10,
        price=500,
        features=[
            "Logo Design",
            "Visitenkarte",
            "Briefpapier",
            "Flyer",
        ],
        offer_type="premium",
    )

    return offer, basic, standard, premium


def get_valid_offer_data():
    return {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": (
            "Ein umfassendes Grafikdesign-Paket "
            "für Unternehmen."
        ),
        "details": [
            {
                "title": "Basic Design",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": ["Logo Design"],
                "offer_type": "basic",
            },
            {
                "title": "Standard Design",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": [
                    "Logo Design",
                    "Visitenkarte",
                ],
                "offer_type": "standard",
            },
            {
                "title": "Premium Design",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": [
                    "Logo Design",
                    "Visitenkarte",
                    "Flyer",
                ],
                "offer_type": "premium",
            },
        ],
    }
