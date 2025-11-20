import csv
import shutil
from pathlib import Path

# Paden instellen
csv_path = Path("routeeventlog/labels.csv")
base_data_path = Path("Container Detection/Images")
source_root = Path("routeeventlog")

# Doelmappen
dest_dirs = {
    -1: base_data_path / "Geen containers",
    0: base_data_path / "Containers" / "Zonder bijplaatsing",
    1: base_data_path / "Containers" / "Met bijplaatsing"
}

# Maak doelmappen aan als ze niet bestaan
for label, dest_dir in dest_dirs.items():
    dest_dir.mkdir(parents=True, exist_ok=True)

# Lees labels.csv en kopieer foto's
copied_count = {-1: 0, 0: 0, 1: 0}
skipped_count = 0

with open(csv_path, "r") as f:
    reader = csv.reader(f)
    next(reader, None)  # Sla header over
    
    for row in reader:
        if not row or len(row) < 2:
            continue
        
        image_path_str = row[0].strip()
        label = int(row[1])
        
        # Verwijder "routeeventlog/" prefix als die aanwezig is
        if image_path_str.startswith("routeeventlog/"):
            image_path_str = image_path_str[len("routeeventlog/"):]
        elif image_path_str.startswith("routeeventlog\\"):
            image_path_str = image_path_str[len("routeeventlog\\"):]
        
        # Zet backslashes om naar forward slashes voor consistent path handling
        image_path_str = image_path_str.replace("\\", "/")
        
        # Bouw volledige bron-pad
        src_file = source_root / image_path_str
        
        if not src_file.exists():
            print(f"⚠️  Bestand niet gevonden: {image_path_str}")
            skipped_count += 1
            continue
        
        # Bepaal doelmap
        if label not in dest_dirs:
            print(f"⚠️  Onbekend label: {label} voor {image_path_str}")
            skipped_count += 1
            continue
        
        dest_dir = dest_dirs[label]
        dest_file = dest_dir / src_file.name
        
        # Kopieer bestand
        try:
            shutil.copy2(src_file, dest_file)
            copied_count[label] += 1
            print(f"✓ Gekopieerd ({label}) naar: {dest_file.name}")
        except Exception as e:
            print(f"✗ Fout bij kopiëren {image_path_str}: {e}")
            skipped_count += 1

# Toon samenvatting
print("\n" + "="*60)
print("SAMENVATTING")
print("="*60)
print(f"Geen containers (-1):              {copied_count[-1]} foto's")
print(f"Containers zonder bijplaatsing (0): {copied_count[0]} foto's")
print(f"Containers met bijplaatsing (1):    {copied_count[1]} foto's")
print(f"Totaal gekopieerd:                 {sum(copied_count.values())} foto's")
print(f"Overgeslagen:                      {skipped_count} foto's")
print("="*60)
