#!/usr/bin/env python3
"""Add extended seed data route to app.py"""

import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the existing seed route with expanded version
old_seed_route = """@app.route('/admin/seed-database')
@admin_login_required
def admin_seed_database():"""

# Check if route already exists
if old_seed_route in content:
    # Find the entire route and replace it
    start_idx = content.find(old_seed_route)
    # Find the next @app.route after this one
    next_route_idx = content.find("\n@app.route", start_idx + 100)
    
    if next_route_idx == -1:
        print("ERROR: Could not find end of seed route!")
        exit(1)
    
    # Remove the old route
    content = content[:start_idx] + content[next_route_idx:]

# Now add the new extended route
seed_route_code = """@app.route('/admin/seed-database')
@admin_login_required
def admin_seed_database():
    try:
        # Sample properties data - 9 properties total
        properties_data = [
            {
                'title': 'Luxury Beachfront Villa Plot in Juhu',
                'description': 'Premium residential plot located in the heart of Juhu with stunning sea-facing views. Perfect for building your dream villa. The plot offers 270-degree ocean views and is surrounded by high-end amenities.',
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
                'description': 'Exceptional commercial plot in Bandra Kurla Complex, Mumbai\\'s premier business district. Ideal for constructing a modern office complex, retail space, or mixed-use development.',
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
                'description': 'Sprawling fertile agricultural land in the renowned Nashik wine region. Perfect for vineyards, organic farming, or agro-tourism ventures. Features natural water sources and rich soil.',
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
                'title': 'Lakefront Villa Plot in Powai',
                'description': 'Exclusive residential plot with stunning Powai Lake views. Located in one of Mumbai\\'s most prestigious neighborhoods, surrounded by IT parks and premium residential complexes.',
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
                'description': 'Premium commercial plot in Pune\\'s IT hub, Hinjewadi Phase 1. Perfect for IT offices, tech parks, or co-working spaces. Located near major IT giants.',
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
                'title': 'Hilltop Retreat Plot in Lonavala',
                'description': 'Breathtaking hilltop plot in the scenic hill station of Lonavala. Ideal for building a luxury weekend villa or boutique resort. Surrounded by lush greenery with panoramic mountain views.',
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
                'title': 'Strategic Industrial Plot in MIDC Pune',
                'description': 'Large industrial plot in the established MIDC Bhosari industrial area. Perfect for manufacturing units, warehouses, or logistics hubs. 24/7 power supply and excellent connectivity.',
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
                'title': 'Premium Gated Community Plot in Thane',
                'description': 'Well-planned residential plot in an upcoming gated community in Thane. Features include 24/7 security, landscaped gardens, clubhouse, and children\\'s play area.',
                'property_type': 'Residential Plot',
                'price': 7200000,
                'area': 3500,
                'location': 'Thane',
                'address': 'Ghodbunder Road, Thane, Maharashtra 400607',
                'latitude': 19.2183,
                'longitude': 72.9781,
                'status': 'Available',
                'featured': False,
                'views': 201,
                'shares': 26
            },
            {
                'title': 'Riverside Resort Plot in Alibaug',
                'description': 'Stunning riverside plot in the coastal town of Alibaug, perfect for resort or vacation home development. Direct river access, coconut groves, and serene natural surroundings.',
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
        
        # Image URLs for each property
        property_images_list = [
            ['https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800',
             'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
             'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800'],
            ['https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800',
             'https://images.unsplash.com/photo-1577495508048-b635879837f1?w=800',
             'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800'],
            ['https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
             'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=800',
             'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800'],
            ['https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
             'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800',
             'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=800'],
            ['https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
             'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800',
             'https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800'],
            ['https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800',
             'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
             'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800'],
            ['https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800',
             'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800',
             'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800'],
            ['https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',
             'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',
             'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800'],
            ['https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
             'https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800',
             'https://images.unsplash.com/photo-1499916078039-922301b0eb9b?w=800']
        ]
        
        count = 0
        for idx, prop_data in enumerate(properties_data):
            # Check if property already exists
            existing = Property.query.filter_by(title=prop_data['title']).first()
            if not existing:
                property = Property(**prop_data)
                db.session.add(property)
                db.session.flush()
                
                # Add images
                for img_idx, img_url in enumerate(property_images_list[idx]):
                    prop_image = PropertyImage(
                        property_id=property.id,
                        image_url=img_url,
                        is_primary=(img_idx == 0)
                    )
                    db.session.add(prop_image)
                
                count += 1
        
        db.session.commit()
        flash(f'Successfully added {count} properties to the database!', 'success')
        log_activity('seed_database', f'Seeded {count} properties', 'admin')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error seeding database: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

"""

# Find insertion point
insertion_point = content.find("@app.route('/admin/properties')")

if insertion_point == -1:
    print("ERROR: Could not find insertion point!")
    exit(1)

# Insert the code
new_content = content[:insertion_point] + seed_route_code + "\n" + content[insertion_point:]

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Added extended seed database route with 9 properties successfully!")
