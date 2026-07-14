import yaml
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import (
    Base, PaketWisata, HargaTiket, Hotel, TempatPenting,
    NomorPenting, Wisata, Transportasi
)

DATA_DIR = "data"

def create_tables():
    """Create all tables in database"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def clear_existing_data(db: Session):
    """Clear existing data from all tables"""
    try:
        db.query(PaketWisata).delete()
        db.query(HargaTiket).delete()
        db.query(Hotel).delete()
        db.query(TempatPenting).delete()
        db.query(NomorPenting).delete()
        db.query(Wisata).delete()
        db.query(Transportasi).delete()
        db.commit()
        print("✓ Existing data cleared")
    except Exception as e:
        print(f"✗ Error clearing data: {e}")
        db.rollback()


def load_paket_wisata(db: Session):
    """Load paket_wisata_lists.toon"""
    filepath = os.path.join(DATA_DIR, "paket_wisata_lists.toon")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML-like format (separated by ---)
    entries = content.split('---')
    
    count = 0
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        try:
            data = yaml.safe_load(entry)
            if not data or 'paket' not in data:
                continue
            
            paket = data['paket']
            data_id = paket.get('id')
            
            existing = db.query(PaketWisata).filter_by(data_id=data_id).first()
            if existing:
                continue
            
            paket_obj = PaketWisata(
                data_id=data_id,
                name=paket.get('n'),
                url=paket.get('url'),
                image_url=paket.get('img')
            )
            db.add(paket_obj)
            count += 1
        except Exception as e:
            print(f"Error parsing paket entry: {e}")
            continue
    
    db.commit()
    print(f"✓ Loaded {count} paket wisata entries")


def load_harga_tiket(db: Session):
    """Load harga_tiket_lists.toon"""
    filepath = os.path.join(DATA_DIR, "harga_tiket_lists.toon")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    current_group = None
    count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('ticket_group:') or (line.startswith('n:') and 'n: "' in line):
            if 'n: "' in line:
                current_group = line.split('n: "')[1].rstrip('"')
        
        if line.startswith('- { n:'):
            try:
                # Extract name and price
                parts = line.split('n: "')[1].split('"')[0]
                name = parts
                
                if 'p: "' in line:
                    price = line.split('p: "')[1].rstrip('"').rstrip(' }')
                    
                    # Check if already exists
                    existing = db.query(HargaTiket).filter_by(
                        group_name=current_group,
                        item_name=name
                    ).first()
                    if not existing:
                        tiket = HargaTiket(
                            group_name=current_group,
                            item_name=name,
                            price=price
                        )
                        db.add(tiket)
                        count += 1
            except Exception as e:
                continue
    
    db.commit()
    print(f"✓ Loaded {count} harga tiket entries")


def load_transportasi(db: Session):
    """Load transportasi.txt"""
    filepath = os.path.join(DATA_DIR, "transportasi.txt")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = {
        'Jalur Darat': '',
        'Jalur Udara': '',
        'Jalur Kereta': ''
    }
    
    current_section = None
    lines = content.split('\n')
    
    for line in lines:
        if 'Jalur Darat' in line:
            current_section = 'Jalur Darat'
        elif 'Jalur Udara' in line:
            current_section = 'Jalur Udara'
        elif 'Jalur Kereta' in line or 'Kereta API' in line:
            current_section = 'Jalur Kereta'
        
        if current_section:
            sections[current_section] += line + '\n'
    
    count = 0
    for section_name, section_content in sections.items():
        if section_content.strip():
            existing = db.query(Transportasi).filter_by(section_name=section_name).first()
            if not existing:
                trans = Transportasi(
                    section_name=section_name,
                    content=section_content.strip()
                )
                db.add(trans)
                count += 1
    
    db.commit()
    print(f"✓ Loaded {count} transportasi entries")


def load_hotel(db: Session):
    """Load hotel_lists.toon"""
    filepath = os.path.join(DATA_DIR, "hotel_lists.toon")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.split('---')
    count = 0
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        try:
            data = yaml.safe_load(entry)
            if not data or 'hotel' not in data:
                continue
            
            hotel = data['hotel']
            data_id = hotel.get('id')
            
            existing = db.query(Hotel).filter_by(data_id=data_id).first()
            if existing:
                continue
            
            hotel_obj = Hotel(
                data_id=data_id,
                name=hotel.get('n'),
                url=hotel.get('url')
            )
            db.add(hotel_obj)
            count += 1
        except Exception as e:
            continue
    
    db.commit()
    print(f"✓ Loaded {count} hotel entries")


def load_tempat_penting(db: Session):
    """Load tempat_penting_lists.toon"""
    filepath = os.path.join(DATA_DIR, "tempat_penting_lists.toon")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.split('---')
    count = 0
    skipped = 0
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        try:
            data = yaml.safe_load(entry)
            if not data or 'place' not in data:
                continue
            
            place = data['place']
            data_id = place.get('id')
            
            existing = db.query(TempatPenting).filter_by(data_id=data_id).first()
            if existing:
                skipped += 1
                continue
            
            place_obj = TempatPenting(
                data_id=data_id,
                name=place.get('n'),
                description=place.get('cat'),
                url=place.get('url'),
                image_url=place.get('img')
            )
            db.add(place_obj)
            db.flush()  # Flush immediately to catch duplicates
            count += 1
        except Exception as e:
            db.rollback()
            print(f"✗ Error on entry: {e}")
            skipped += 1
            db.flush()
            continue
    
    db.commit()
    print(f"✓ Loaded {count} tempat penting entries (skipped {skipped})")


def load_nomor_penting(db: Session):
    """Load nomor_penting_lists.toon"""
    filepath = os.path.join(DATA_DIR, "nomor_penting_lists.toon")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.split('---')
    count = 0
    skipped = 0
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        try:
            data = yaml.safe_load(entry)
            if not data or 'emergency_contact' not in data:
                continue
            
            contact = data['emergency_contact']
            data_id = contact.get('id')
            
            existing = db.query(NomorPenting).filter_by(data_id=data_id).first()
            if existing:
                skipped += 1
                continue
            
            nomor_obj = NomorPenting(
                data_id=data_id,
                name=contact.get('n'),
                phone=contact.get('tel'),
                description=contact.get('addr')
            )
            db.add(nomor_obj)
            db.flush()
            count += 1
        except Exception as e:
            db.rollback()
            print(f"✗ Error on entry: {e}")
            skipped += 1
            db.flush()
            continue
    
    db.commit()
    print(f"✓ Loaded {count} nomor penting entries (skipped {skipped})")


def load_wisata(db: Session):
    """Load wisata_lists.toon"""
    filepath = os.path.join(DATA_DIR, "wisata_lists.toon")
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.split('---')
    count = 0
    skipped = 0
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        try:
            data = yaml.safe_load(entry)
            if not data or 'wisata' not in data:
                continue
            
            wisata = data['wisata']
            data_id = wisata.get('id')
            
            existing = db.query(Wisata).filter_by(data_id=data_id).first()
            if existing:
                skipped += 1
                continue
            
            wisata_obj = Wisata(
                data_id=data_id,
                name=wisata.get('n'),
                url=wisata.get('url'),
                image_url=wisata.get('img')
            )
            db.add(wisata_obj)
            db.flush()
            count += 1
        except Exception as e:
            db.rollback()
            print(f"✗ Error on entry: {e}")
            skipped += 1
            db.flush()
            continue
    
    db.commit()
    print(f"✓ Loaded {count} wisata entries (skipped {skipped})")


def load_all_data():
    """Load all data from files to database"""
    db = SessionLocal()
    try:
        create_tables()
        clear_existing_data(db)
        load_paket_wisata(db)
        load_harga_tiket(db)
        load_hotel(db)
        load_tempat_penting(db)
        load_nomor_penting(db)
        load_wisata(db)
        load_transportasi(db)
        print("\n✓ All data loaded successfully!")
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    load_all_data()
