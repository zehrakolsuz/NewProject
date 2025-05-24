# Author: Emir Keçeli
"""
Bu script, Zimmerman araçlarından üretilmiş JSON dosyalarını alır ve
web/dashboard.html şablonuna gömerek statik bir HTML rapor oluşturur.
"""
import json
import os

def generate_html_report(timeline_path, score_path, template_path, output_path):
    # JSON dosyalarını oku
    with open(timeline_path, 'r', encoding='utf-8') as f:
        timeline = json.load(f)
    with open(score_path, 'r', encoding='utf-8') as f:
        scores = json.load(f)

    # HTML şablonunu oku
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()

    # JSON verilerini JS bloğu olarak ekle
    data_script = f"""
<script>
  const timelineData = {json.dumps(timeline)};
  const scoreData = {json.dumps(scores)};
</script>
"""
    # </body> etiketinden önce script bloğunu ekle
    final_html = html_template.replace('</body>', data_script + '\n</body>')

    # Çıktı dizinini oluştur
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"HTML raporu üretildi: {output_path}")

# Kullanım örneği
if __name__ == '__main__':
    generate_html_report(
        timeline_path='output/combined_timeline.json',
        score_path='output/scored_sessions.json',
        template_path='web/dashboard.html',
        output_path='output_reports/report.html'
    )
