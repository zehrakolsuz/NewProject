
// Örnek veri setleri (gerçek verilerinizle değiştirin)
const timelineData = [
  {"timestamp": "2025-05-24 10:00", "program": "notepad.exe", "path": "C:\\Windows\\notepad.exe"},
  {"timestamp": "2025-05-24 10:05", "filename": "suspicious.exe", "path": "C:\\Temp\\suspicious.exe"},
  {"timestamp": "2025-05-24 10:10", "program": "cmd.exe", "path": "C:\\Windows\\System32\\cmd.exe"}
];

const scoreData = [
  {"user_session": "Oturum 1", "behavior_score": 1},
  {"user_session": "Oturum 2", "behavior_score": 2},
  {"user_session": "Oturum 3", "behavior_score": 4},
  {"user_session": "Oturum 4", "behavior_score": 3}
];


window.addEventListener('DOMContentLoaded', () => {
  // Zaman Çizelgesi
  const timelineList = document.getElementById('timeline-list');
  if (typeof timelineData !== 'undefined') {
    timelineData.forEach(item => {
      const li = document.createElement('li');
      li.textContent = `${item.timestamp} - ${item.program || item.filename} (${item.path || ''})`;
      timelineList.appendChild(li);
    });
  }

  // Oturum Skorları Grafiği
  if (typeof scoreData !== 'undefined') {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    const labels = scoreData.map(x => x.user_session);
    const scores = scoreData.map(x => x.behavior_score);
    const colors = scores.map(s => s <= 1 ? '#FFD1E3' : s <= 3 ? '#EBD3F8' : '#E3D095'); 

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Davranış Skoru',
          data: scores,
          backgroundColor: colors,
          borderColor: 'transparent',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 5,
            grid: { borderColor: '#7858A6', color: '#5B4B8A' },
            ticks: { color: '#E0E0E0' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#E0E0E0' }
          }
        },
        plugins: {
          legend: { display: false },
          title: { 
            display: true, 
            text: 'Kullanıcı Oturum Skorları', 
            color: '#E0E0E0',
            font: { size: 16, family: 'Roboto', weight: '700' }
          }
        },
        animation: {
          duration: 1000,
          easing: 'easeInOutQuad'
        }
      }
    });
  }

  // JSON Görselleştirme
  const jsonData = {
    analysis: {
      user: 'Kullanıcı 1',
      session: {
        id: '12345',
        score: 85,
        suspiciousActions: ['Dosya indirme', 'Yetkisiz erişim denemesi']
      },
      timestamp: '2025-05-24 10:00'
    }
  };

  const jsonContainer = document.getElementById('json-visualization');
  jsonContainer.textContent = JSON.stringify(jsonData, null, 2);
});