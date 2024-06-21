from datetime import datetime, timezone

# Eredeti időbélyeg milliszekundumokban
timestamp_ms = 1718877934180

# Időbélyeg átalakítása másodpercekké
timestamp_s = timestamp_ms / 1000.0

# Dátum és idő átalakítása UTC időzónában
date_time = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)

print("Az időbélyeg által reprezentált dátum és idő:", date_time)
