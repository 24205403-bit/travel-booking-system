from app import create_app
from models.user import User
from models.destination import Destination
from models.review import Review
from models.booking import Booking

def seed_database():
    app = create_app()
    with app.app_context():
        print("Seeding database...")

        # 1. Clear existing documents if needed or skip if admin exists
        existing_admin = User.find_by_email("admin@travel.com")
        if existing_admin:
            print("Database already seeded. Skipping...")
            return

        # 2. Users
        admin_user = User.create(
            name="Admin User",
            email="admin@travel.com",
            password="adminpassword123",
            phone="+91 9876543210",
            role="admin"
        )
        print("Created Admin user: admin@travel.com / adminpassword123")

        demo_user = User.create(
            name="Alex Traveler",
            email="user@travel.com",
            password="userpassword123",
            phone="+91 9123456789",
            role="user"
        )
        print("Created Demo user: user@travel.com / userpassword123")

        # 3. Destinations
        dest1 = Destination.create(
            title="Queen of Hill Stations - Ooty",
            location="Nilgiris, Tamil Nadu",
            price=12500,
            duration="3 Days / 2 Nights",
            description="Experience breathtaking tea plantations, crisp mountain mist, historic Toy Train rides, and scenic lake boating in Ooty.",
            category="Hill Station",
            image_url="/static/images/ooty.jpg",
            highlights=["Nilgiri Mountain Railway", "Ooty Lake Boating", "Botanical Gardens", "Doddabetta Peak"],
            included=["Luxury Accommodation", "Breakfast & Dinner", "Sightseeing Cab", "Guide Fees"],
            rating=4.8
        )

        dest2 = Destination.create(
            title="Princess of Hill Stations - Kodaikanal",
            location="Dindigul, Tamil Nadu",
            price=14000,
            duration="4 Days / 3 Nights",
            description="Explore misty pine forests, serene lakes, Coaker's Walk vistas, and enchanted waterfalls in the jewel of the Palani Hills.",
            category="Hill Station",
            image_url="/static/images/kodaikanal.jpg",
            highlights=["Kodai Lake Boating", "Pillar Rocks", "Pine Forest Trek", "Coaker's Walk"],
            included=["Resort Stay", "Daily Meals", "Waterfall Trekking Guide", "Transport"],
            rating=4.7
        )

        dest3 = Destination.create(
            title="Tropical Beach Paradise - Goa",
            location="Goa, India",
            price=18500,
            duration="5 Days / 4 Nights",
            description="Sun-kissed golden beaches, thrilling water sports, historic Portuguese architecture, vibrant night markets, and sunset cruises.",
            category="Beach",
            image_url="/static/images/goa.jpg",
            highlights=["Baga & Calangute Beach", "Dudhsagar Waterfalls", "Cathedral & Fort Aguada", "Sunset Cruise"],
            included=["Beach Resort Stay", "Buffet Breakfast", "Airport Transfers", "Cruise Ticket"],
            rating=4.9
        )

        dest4 = Destination.create(
            title="Emerald Tea Gardens - Munnar",
            location="Idukki, Kerala",
            price=15000,
            duration="4 Days / 3 Nights",
            description="Immerse in endless rolling green tea estates, exotic flora & fauna at Eravikulam National Park, and tranquil spice valleys.",
            category="Nature",
            image_url="/static/images/munnar.jpg",
            highlights=["Tea Museum & Estates", "Eravikulam National Park", "Mattupetty Dam Boating", "Anamudi Peak View"],
            included=["Premium Hill Resort", "All Meals", "Jeep Safari", "Tea Tasting Session"],
            rating=4.9
        )

        # 4. Sample Reviews
        Review.create(
            destination_id=dest1['_id'],
            user_id=demo_user['_id'],
            user_name=demo_user['name'],
            rating=5,
            comment="Unforgettable experience! The Toy Train journey through the Nilgiri hills was absolute magic."
        )

        Review.create(
            destination_id=dest3['_id'],
            user_id=demo_user['_id'],
            user_name="Sarah Jenkins",
            rating=5,
            comment="Goa was amazing! Great beach resort and seamless booking experience."
        )

        # 5. Sample Booking
        Booking.create(
            user_id=demo_user['_id'],
            destination_id=dest1['_id'],
            travel_date="2026-11-15",
            guests=2,
            total_price=25000,
            special_requests="Honeymoon room setup with lake view room if available."
        )

        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
