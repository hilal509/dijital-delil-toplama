import os
import datetime
import subprocess
import json

# Varsayılan dizinler
DEFAULT_DIRECTORIES = [
    'C:/Users/Public/Documents',  # Genel Belgeler
    'C:/Users/Public/Pictures',   # Genel Resimler
    'C:/Windows/System32',        # Windows Sistem Dosyaları
]

def collect_files(directory):
    """Belirtilen dizindeki dosyaların bilgilerini toplar."""
    files_data = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_stats = os.stat(file_path)
            files_data.append({
                'file_name': filename,
                'file_path': file_path,
                'size': file_stats.st_size,
                'created': datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'accessed': datetime.datetime.fromtimestamp(file_stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            })
    return files_data

def collect_processes():
    """Sistemdeki aktif işlemleri toplar."""
    process_data = []
    # Windows ortamında çalıştırılabilir bir komutla tüm işlemleri alıyoruz.
    process_list = subprocess.getoutput('tasklist')
    process_lines = process_list.splitlines()

    for line in process_lines[3:]:  # İlk 3 satır başlık ve boş satırdır, onları geçiyoruz
        process_info = line.split()
        if len(process_info) >= 5:
            process_data.append({
                'name': process_info[0],
                'pid': process_info[1],
                'memory_usage': process_info[4]
            })
    return process_data

def collect_connections():
    """Ağ bağlantılarını toplar."""
    connection_data = []
    # `netstat` komutuyla ağ bağlantılarını alıyoruz.
    connection_list = subprocess.getoutput('netstat -an')
    connection_lines = connection_list.splitlines()

    for line in connection_lines[4:]:  # İlk 4 satır başlık bilgileri
        if 'TCP' in line or 'UDP' in line:
            connection_info = line.split()
            connection_data.append({
                'protocol': connection_info[0],
                'local_address': connection_info[1],
                'foreign_address': connection_info[2],
                'state': connection_info[3] if len(connection_info) > 3 else 'N/A'
            })
    return connection_data

def save_data_to_file(data, filename):
    """Toplanan verileri JSON formatında dosyaya kaydeder."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Veriler {filename} dosyasına kaydedildi.")

def display_files_data(files_data):
    """Dosya bilgilerini terminalde gösterir."""
    print("\n--- Dosya Bilgileri ---")
    for file_info in files_data:
        print(f"Dosya: {file_info['file_name']}, Yol: {file_info['file_path']}, Boyut: {file_info['size']} bytes, "
              f"Oluşturulma: {file_info['created']}, Değiştirilme: {file_info['modified']}, Erişim: {file_info['accessed']}")

def display_process_data(process_data):
    """İşlem bilgilerini terminalde gösterir."""
    print("\n--- İşlem Bilgileri ---")
    for proc_info in process_data:
        print(f"İsim: {proc_info['name']}, PID: {proc_info['pid']}, Bellek Kullanımı: {proc_info['memory_usage']}")

def display_connection_data(connection_data):
    """Ağ bağlantı bilgilerini terminalde gösterir."""
    print("\n--- Ağ Bağlantıları ---")
    for conn_info in connection_data:
        print(f"Protokol: {conn_info['protocol']}, Yerel Adres: {conn_info['local_address']}, "
              f"Yabancı Adres: {conn_info['foreign_address']}, Durum: {conn_info['state']}")

def main():
    print("Temel Dijital Delil Toplama Aracı - Başlangıç")

    # Varsayılan dizinlerde dosya bilgileri topla ve göster
    print("\nDosyalar toplanıyor...")
    all_files_data = []
    for directory in DEFAULT_DIRECTORIES:
        if os.path.exists(directory):
            print(f"\nTarama yapılıyor: {directory}")
            files_data = collect_files(directory)
            all_files_data.extend(files_data)
            display_files_data(files_data)

    # İşlem bilgilerini topla ve göster
    print("\nİşlemler toplanıyor...")
    process_data = collect_processes()
    display_process_data(process_data)

    # Ağ bağlantılarını topla ve göster
    print("\nAğ bağlantıları toplanıyor...")
    connection_data = collect_connections()
    display_connection_data(connection_data)

    # Verileri JSON dosyasına kaydet
    data_to_save = {
        'files': all_files_data,
        'processes': process_data,
        'connections': connection_data,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_data_to_file(data_to_save, 'digital_evidence.json')

if __name__ == "__main__":
    main()

