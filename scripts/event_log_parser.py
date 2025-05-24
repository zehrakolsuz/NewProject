#Event log parse; bu dosya adından da anlaşılacağı gibi, bir olay günlüğü ayrıştırıcısıdır. Olay günlükleri genellikle şu tür bilgileri içerir:
#Kullanıcı giriş-çıkışları
#Hata mesajları
#Uygulama çalıştırmaları
#Sistem yeniden başlatmaları
#Güvenlik uyarıları
#Bu dosya ise bu günlükleri analiz ederek:
#Log dosyasını açar,
#İçeriğini satır satır okur,
#Örüntüleri (tarih, zaman, seviye, mesaj vs.) tanır,

import re
from typing import List, Dict

# Her log satırını bu örneğe göre ayrıştıracağız:
# 2025-05-24 14:12:01 INFO User login: sena

LOG_PATTERN = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) (?P<message>.+)")

def parse_log_file(file_path: str) -> List[Dict[str, str]]:
    parsed_logs = []

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            match = LOG_PATTERN.match(line.strip())
            if match:
                parsed_logs.append(match.groupdict())
            else:
                print(f"Satır {line_number} ayrıştırılamadı: {line.strip()}")

    return parsed_logs

if __name__ == "__main__":
    log_file = "C:/Users/Huawei/Documents/setupact.log"

    logs = parse_log_file(log_file)

    for log in logs:
        print(log)
