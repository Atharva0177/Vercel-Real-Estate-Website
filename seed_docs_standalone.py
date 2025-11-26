#!/usr/bin/env python3
"""
Standalone script to seed documents directly to database
Run this independently: python seed_docs_standalone.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app
from app import app, db
from models import Property, PropertyDocument
import random

def seed_documents():
    with app.app_context():
        try:
            doc_templates = [
                ('Property_Legal_Document.pdf', 'LEGAL', '2.3 MB', 'uploads/documents/sample_legal.pdf'),
                ('Floor_Plan.pdf', 'FLOOR PLAN', '1.5 MB', 'uploads/documents/sample_floor_plan.pdf'),
                ('NOC_Certificate.pdf', 'NOC', '856 KB', 'uploads/documents/sample_noc.pdf'),
                ('Approval_Letter.pdf', 'APPROVAL', '1.2 MB', 'uploads/documents/sample_approval.pdf'),
                ('Property_Survey_Report.pdf', 'OTHER', '3.1 MB', 'uploads/documents/sample_survey.pdf'),
            ]
            
            properties = Property.query.all()
            
            if not properties:
                print("❌ No properties found in database!")
                return
            
            print(f"\n📄 Processing {len(properties)} properties...\n")
            
            added_count = 0
            skipped_count = 0
            
            for prop in properties:
                if len(prop.documents) > 0:
                    print(f"⏭️  Property #{prop.id} '{prop.title}' already has {len(prop.documents)} documents, skipping...")
                    skipped_count += 1
                    continue
                
                num_docs = random.randint(3, 5)
                selected = random.sample(doc_templates, num_docs)
                
                for doc_name, doc_type, file_size, doc_url in selected:
                    doc = PropertyDocument(
                        property_id=prop.id,
                        document_name=doc_name,
                        document_url=doc_url,
                        document_type=doc_type,
                        file_size=file_size
                    )
                    db.session.add(doc)
                    added_count += 1
                
                print(f"✅ Added {num_docs} documents to Property #{prop.id}: {prop.title}")
            
            db.session.commit()
            
            print(f"\n🎉 Success!")
            print(f"   - Added {added_count} dummy documents")
            print(f"   - Skipped {skipped_count} properties that already had documents")
            print(f"\n💡 Now visit any property page to see:")
            print(f"   - 📄 Property Documents section")
            print(f"   - Document cards with Preview/Download buttons")
            print(f"   - 'Download All (X files)' button")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_documents()
