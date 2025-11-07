from app import app, db
from models import Property, PropertyImage, PropertyVideo, User
from datetime import datetime

def seed_database():
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("Creating sample properties...")
        
        # Sample properties with unique details
        properties_data = [
            {
                'title': 'Luxury Beachfront Villa Plot in Juhu',
                'description': 'Premium residential plot located in the heart of Juhu with stunning sea-facing views. Perfect for building your dream villa. The plot offers 270-degree ocean views and is surrounded by high-end amenities including five-star hotels, exclusive clubs, and fine dining restaurants. Direct beach access and excellent connectivity to the airport.',
                'property_type': 'Residential Plot',
                'price': 15000000,
                'area': 5000,
                'location': 'Mumbai',
                'address': 'Juhu Beach Road, Mumbai, Maharashtra 400049',
                'latitude': 19.0990,
                'longitude': 72.8258,
                'status': 'Available',
                'featured': True,
                'views': 245,
                'shares': 34
            },
            {
                'title': 'Prime Commercial Hub in BKC',
                'description': 'Exceptional commercial plot in Bandra Kurla Complex, Mumbai\'s premier business district. Ideal for constructing a modern office complex, retail space, or mixed-use development. Surrounded by multinational corporations, premium hotels, and the NSE building. Excellent metro and road connectivity.',
                'property_type': 'Commercial Plot',
                'price': 25000000,
                'area': 8000,
                'location': 'Mumbai',
                'address': 'Bandra Kurla Complex, Mumbai, Maharashtra 400051',
                'latitude': 19.0626,
                'longitude': 72.8687,
                'status': 'Available',
                'featured': True,
                'views': 189,
                'shares': 28
            },
            {
                'title': 'Scenic Agricultural Land in Nashik Wine Valley',
                'description': 'Sprawling fertile agricultural land in the renowned Nashik wine region. Perfect for vineyards, organic farming, or agro-tourism ventures. The property features natural water sources, rich soil, and panoramic valley views. Located near famous wineries and offers excellent potential for wine production or farm resort development.',
                'property_type': 'Agricultural Land',
                'price': 3500000,
                'area': 10000,
                'location': 'Nashik',
                'address': 'Nashik-Pune Road, Nashik, Maharashtra 422009',
                'latitude': 19.9975,
                'longitude': 73.7898,
                'status': 'Available',
                'featured': True,
                'views': 156,
                'shares': 19
            },
            {
                'title': 'Strategic Industrial Plot in MIDC Pune',
                'description': 'Large industrial plot in the established MIDC Bhosari industrial area. Perfect for manufacturing units, warehouses, or logistics hubs. The plot offers 24/7 power supply, wide approach roads, and proximity to major highways. Surrounded by established industries and offers excellent infrastructure for industrial operations.',
                'property_type': 'Industrial Plot',
                'price': 8000000,
                'area': 15000,
                'location': 'Pune',
                'address': 'MIDC Bhosari, Pune, Maharashtra 411026',
                'latitude': 18.6298,
                'longitude': 73.8450,
                'status': 'Available',
                'featured': False,
                'views': 134,
                'shares': 15
            },
            {
                'title': 'Hilltop Retreat Plot in Lonavala',
                'description': 'Breathtaking hilltop plot in the scenic hill station of Lonavala. Ideal for building a luxury weekend villa or boutique resort. Surrounded by lush greenery with panoramic views of the Sahyadri mountains. Pleasant weather year-round, close to popular tourist attractions, waterfalls, and trekking trails.',
                'property_type': 'Residential Plot',
                'price': 5500000,
                'area': 4000,
                'location': 'Lonavala',
                'address': 'Old Mumbai-Pune Highway, Lonavala, Maharashtra 410401',
                'latitude': 18.7537,
                'longitude': 73.4076,
                'status': 'Available',
                'featured': False,
                'views': 178,
                'shares': 22
            },
            {
                'title': 'Premium Gated Community Plot in Thane',
                'description': 'Well-planned residential plot in an upcoming gated community in Thane. Features include 24/7 security, landscaped gardens, clubhouse, and children\'s play area. Excellent connectivity to Eastern Express Highway and Thane railway station. Close to reputed schools, hospitals, and shopping malls.',
                'property_type': 'Residential Plot',
                'price': 7200000,
                'area': 3500,
                'location': 'Thane',
                'address': 'Ghodbunder Road, Thane, Maharashtra 400607',
                'latitude': 19.2183,
                'longitude': 72.9781,
                'status': 'Reserved',
                'featured': False,
                'views': 201,
                'shares': 26
            },
            {
                'title': 'Lakefront Villa Plot in Powai',
                'description': 'Exclusive residential plot with stunning Powai Lake views. Located in one of Mumbai\'s most prestigious neighborhoods, surrounded by IT parks, premium residential complexes, and international schools. Perfect for building a modern lakeside villa with all modern amenities.',
                'property_type': 'Residential Plot',
                'price': 18000000,
                'area': 4500,
                'location': 'Mumbai',
                'address': 'Hiranandani Gardens, Powai, Mumbai, Maharashtra 400076',
                'latitude': 19.1176,
                'longitude': 72.9060,
                'status': 'Available',
                'featured': True,
                'views': 287,
                'shares': 41
            },
            {
                'title': 'Tech Park Commercial Plot in Hinjewadi',
                'description': 'Premium commercial plot in Pune\'s IT hub, Hinjewadi Phase 1. Perfect for IT offices, tech parks, or co-working spaces. Located near major IT giants like Infosys, Wipro, and TCS. Excellent infrastructure with metro connectivity under construction. High ROI potential.',
                'property_type': 'Commercial Plot',
                'price': 12000000,
                'area': 6000,
                'location': 'Pune',
                'address': 'Hinjewadi Phase 1, Pune, Maharashtra 411057',
                'latitude': 18.5912,
                'longitude': 73.7389,
                'status': 'Available',
                'featured': True,
                'views': 312,
                'shares': 38
            },
            {
                'title': 'Riverside Resort Plot in Alibaug',
                'description': 'Stunning riverside plot in the coastal town of Alibaug, perfect for resort or vacation home development. The property offers direct river access, coconut groves, and serene natural surroundings. Only 2 hours from Mumbai, this plot is ideal for eco-resort, boutique hotel, or luxury farmhouse.',
                'property_type': 'Residential Plot',
                'price': 9500000,
                'area': 7500,
                'location': 'Alibaug',
                'address': 'Mandwa Road, Alibaug, Maharashtra 402201',
                'latitude': 18.6414,
                'longitude': 72.8722,
                'status': 'Available',
                'featured': True,
                'views': 223,
                'shares': 31
            }
        ]
        
        # Unique image sets for each property
        property_images = [
            # Property 1 - Luxury Beach Villa
            [
                'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800',
                'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
                'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800',
                'https://images.unsplash.com/photo-1602343168117-bb8ffe3e2e9f?w=800'
            ],
            # Property 2 - Commercial BKC
            [
                'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800',
                'https://images.unsplash.com/photo-1577495508048-b635879837f1?w=800',
                'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800',
                'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800'
            ],
            # Property 3 - Agricultural Nashik
            [
                'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
                'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=800',
                'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800',
                'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=800'
            ],
            # Property 4 - Industrial Pune
            [
                'https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800',
                'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800',
                'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800',
                'https://images.unsplash.com/photo-1597759675762-1678847ec32e?w=800'
            ],
            # Property 5 - Hilltop Lonavala
            [
                'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
                'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800'
            ],
            # Property 6 - Thane Gated Community
            [
                'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',
                'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',
                'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800',
                'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800'
            ],
            # Property 7 - Powai Lakefront
            [
                'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
                'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800',
                'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=800',
                'https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=800'
            ],
            # Property 8 - Tech Park Hinjewadi
            [
                'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
                'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800',
                'https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800',
                'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800'
            ],
            # Property 9 - Riverside Alibaug
            [
                'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800',
                'https://images.unsplash.com/photo-1499916078039-922301b0eb9b?w=800',
                'https://images.unsplash.com/photo-1544984243-ec57ea16fe25?w=800'
            ]
        ]
        
        # Video URLs for properties
        video_urls = [
            'https://www.youtube.com/watch?v=zumJJUL_ruM',  # Luxury Villa Tour
            'https://www.youtube.com/watch?v=Nck6BZga7TQ',  # Commercial Property
            'https://www.youtube.com/watch?v=VIDEO3',       # Agricultural Land
            'https://www.youtube.com/watch?v=VIDEO4',       # Industrial
            'https://www.youtube.com/watch?v=VIDEO5',       # Hill Station
            None,  # No video
            'https://www.youtube.com/watch?v=VIDEO7',       # Lakefront
            'https://www.youtube.com/watch?v=VIDEO8',       # Tech Park
            'https://www.youtube.com/watch?v=VIDEO9',       # Riverside
        ]
        
        for idx, prop_data in enumerate(properties_data):
            property = Property(**prop_data)
            db.session.add(property)
            db.session.flush()
            
            # Add unique images for each property
            for img_idx, img_url in enumerate(property_images[idx]):
                prop_image = PropertyImage(
                    property_id=property.id,
                    image_url=img_url,
                    is_primary=(img_idx == 0)
                )
                db.session.add(prop_image)
            
            # Add video if available
            if video_urls[idx]:
                prop_video = PropertyVideo(
                    property_id=property.id,
                    video_url=video_urls[idx],
                    video_type='youtube'
                )
                db.session.add(prop_video)
        
        # Create a demo user
        demo_user = User(
            name='Demo User',
            email='demo@example.com',
            phone='+91 98765 43210'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        
        # Create Atharva user
        atharva_user = User(
            name='Atharva',
            email='atharva@example.com',
            phone='+91 98765 00177'
        )
        atharva_user.set_password('atharva123')
        db.session.add(atharva_user)
        
        db.session.commit()
        print("✅ Database seeded successfully!")
        print(f"\n{'='*60}")
        print(f"{'SEED DATA SUMMARY':^60}")
        print(f"{'='*60}")
        print(f"\n📊 Total Properties Created: 9")
        print(f"   - Featured Properties: 6")
        print(f"   - Residential Plots: 5")
        print(f"   - Commercial Plots: 2")
        print(f"   - Agricultural Land: 1")
        print(f"   - Industrial Plot: 1")
        print(f"\n👥 User Accounts Created: 2")
        print(f"\n{'='*60}")
        print(f"{'LOGIN CREDENTIALS':^60}")
        print(f"{'='*60}")
        print(f"\n🔐 ADMIN ACCESS:")
        print(f"   URL: http://localhost:8000/admin/login")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"\n👤 DEMO USER:")
        print(f"   Email: demo@example.com")
        print(f"   Password: demo123")
        print(f"\n👤 ATHARVA USER:")
        print(f"   Email: atharva@example.com")
        print(f"   Password: atharva123")
        print(f"\n{'='*60}")
        print(f"\n🌐 Access Website: http://localhost:8000")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    seed_database()