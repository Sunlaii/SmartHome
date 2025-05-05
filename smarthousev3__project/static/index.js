const menuToSection = {
  homeMenu: 'homeSection',
  roomsMenu: 'roomsSection',
  Security: 'securitySection',
};

document.querySelectorAll('.sidebar a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();

    // Bỏ class active khỏi tất cả menu
    document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
    link.classList.add('active');

    // Ẩn tất cả section
    document.querySelectorAll('.page-section').forEach(section => {
      section.style.display = 'none';
    });

    // Hiện section tương ứng
    const sectionId = menuToSection[link.id];
    if (sectionId) {
      document.getElementById(sectionId).style.display = 'block';
    }
    if (sectionId === "homeSection") {
      updateDashboardOverview(); // ✅ gọi khi về trang chính
    }
  });
});


function removeVietnameseTones(str) {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D");
}

const rooms = {
  "Phòng ngủ 1": ["Đèn", "Quạt", "Rèm"],
  "Phòng ngủ 2": ["Đèn", "Quạt", "Máy lạnh"],
  "Phòng khách": ["Đèn", "Quạt", "TV"],
  "Phòng bếp": ["Đèn", "Máy hút mùi", "Lò vi sóng"]
};

let deviceStates = {};
let deviceButtons = {};

// Hiển thị các phòng dạng card (1 hàng 1 thẻ)
document.getElementById('roomsMenu').addEventListener('click', function () {
  const roomsSection = document.getElementById('roomsSection');
  roomsSection.innerHTML = '<h2>Trạng thái các phòng</h2>';

  for (const room in rooms) {
    let onCount = 0;
    let offCount = 0;

    rooms[room].forEach(device => {
      if (deviceStates[device] === undefined) {
        deviceStates[device] = true;
      }
      if (deviceStates[device]) {
        onCount++;
      } else {
        offCount++;
      }
    });

    const card = document.createElement('div');
    card.className = 'room-card';
    card.onclick = () => showDevices(room);

    const title = document.createElement('div');
    title.className = 'room-title';
    title.textContent = room;

    const counts = document.createElement('div');
    counts.className = 'device-counts';
    counts.innerHTML = `
      <div class="device-on">Bật: ${onCount}</div>
      <div class="device-off">Tắt: ${offCount}</div>
    `;

    card.appendChild(title);
    card.appendChild(counts);
    roomsSection.appendChild(card);
  }
});


function showDevices(room) {
  const roomsSection = document.getElementById('roomsSection');
  roomsSection.innerHTML = `<h2>${room}</h2>`;
  deviceButtons = {};

  const icons = {
    'Đèn': '💡',
    'Quạt': '🌀',
    'Máy lạnh': '❄️'
  };

  rooms[room].forEach(device => {
    const card = document.createElement('div');
    card.className = 'device-card';

    const label = document.createElement('span');
    label.innerHTML = `<i>${icons[device] || '🔌'}</i> ${device}`;

    const toggleBtn = document.createElement('button');
    const isOn = deviceStates[device] ?? true;
    toggleBtn.className = `toggle-btn ${isOn ? 'on' : 'off'}`;
    toggleBtn.textContent = isOn ? "Bật" : "Tắt";

    toggleBtn.onclick = () => toggleDevice(device, toggleBtn);

    deviceStates[device] = isOn;
    deviceButtons[device] = toggleBtn;

    card.appendChild(label);
    card.appendChild(toggleBtn);
    roomsSection.appendChild(card);
  });

  // 👉 Thêm nút giọng nói vào cuối section phòng
  const voiceBtn = document.createElement('button');
  voiceBtn.className = 'voice-btn';
  voiceBtn.textContent = '🎤 Điều khiển bằng giọng nói';
  voiceBtn.onclick = startVoiceRecognition;
  voiceBtn.style.marginTop = '20px';
  roomsSection.appendChild(voiceBtn); // ❗ Gắn vào roomsSection, không phải main
}






// Cập nhật trạng thái thiết bị
function setDeviceState(device, newState) {
  deviceStates[device] = newState;
  if (deviceButtons[device]) {
    deviceButtons[device].classList.remove('on', 'off');
    deviceButtons[device].classList.add('toggle-btn', newState ? 'on' : 'off');
    deviceButtons[device].textContent = newState ? 'Bật' : 'Tắt';
  }

  if (device === "Đèn") {
    fetch(`/control_light/${newState ? 'on' : 'off'}`);
  }
  

  console.log(`Thiết bị ${device} hiện đang ${newState ? 'bật' : 'tắt'}`);
}

// Điều khiển bằng giọng nói
function startVoiceRecognition() {
  fetch('http://localhost:5000/voice_recognition')
    .then(response => response.json())
    .then(data => {
      if (data.text) {
        const command = data.text.toLowerCase();
        console.log('Bạn nói:', command);


        const main = document.getElementById('mainContent');
        const logEntry = document.createElement('div');
logEntry.textContent = "Bạn vừa nói: " + command;
document.getElementById('voiceLogContent').prepend(logEntry);

        

        const normalizedCommand = removeVietnameseTones(command);
        const isTurnOn = normalizedCommand.includes("bat") || normalizedCommand.includes("open");
        const isTurnOff = normalizedCommand.includes("tat") || normalizedCommand.includes("finish");

        const isFan = normalizedCommand.includes("quat") || normalizedCommand.includes("fan");
        console.log( normalizedCommand , isTurnOff , isTurnOn , isFan)

        if (isFan) {
          const action = isTurnOn ? "open fan" : isTurnOff ? "finish fan" : null;
          console.log("goi ham", action)
        
          if (action) {
            fetch('http://localhost:5000/control_device', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ action: action })
            })
            .then(response => response.json())
            .then(data => {
              console.log("Kết quả điều khiển:", data);
            })
            .catch(error => {
              console.error("Lỗi điều khiển thiết bị:", error);
            });
            if (action ==="open fan"){
              setDeviceState("quat",true)
            }
            if(action==="finish fan"){
              setDeviceState("quat",false)
            }
          }
        }
      

        for (const device in deviceButtons) {
          const normalizedDevice = removeVietnameseTones(device.toLowerCase());
          console.log(normalizedDevice)
          if (normalizedCommand.includes(normalizedDevice)) {
            if (isTurnOn && !deviceStates[device]) {
              setDeviceState(device, true);
            } else if (isTurnOff && deviceStates[device]) {
              setDeviceState(device, false);
            }
            break;
          }
        }
      } else {
        alert("Không nhận diện được giọng nói. Thử lại!");
      }
    })
    .catch(error => {
      console.error('Lỗi server:', error);
    });
}
function toggleVoiceLog() {
  document.getElementById('voiceLogPanel').classList.toggle('active');
}
document.getElementById("Security").addEventListener("click", function () {
  showSection("securitySection");
});

function showSection(id) {
  document.querySelectorAll(".page-section").forEach(sec => sec.style.display = "none");
  document.getElementById(id).style.display = "block";
}


const cameraFeed = document.getElementById("cameraFeed");
const startCameraBtn = document.getElementById("startCameraBtn");
const stopCameraBtn = document.getElementById("stopCameraBtn");
const motionToggle = document.getElementById("motionToggle");

// Bật camera
startCameraBtn.onclick = async () => {
  const response = await fetch("/security/start_camera", { method: "POST" });

  if (response.ok) {
    console.log("oke")
    cameraFeed.src = "/security/video_feed";  // Đặt source cho ảnh video stream
    startCameraBtn.disabled = true;  // Vô hiệu nút bật camera
    stopCameraBtn.disabled = false;  // Kích hoạt nút tắt camera
  } else {
    alert("Không thể bật camera!");
  }
};

// Tắt camera
stopCameraBtn.onclick = async () => {
  const response = await fetch("/security/stop_camera", { method: "POST" });

  if (response.ok) {
    cameraFeed.src = "";  // Xóa nguồn video
    stopCameraBtn.disabled = true;  // Vô hiệu nút tắt camera
    startCameraBtn.disabled = false;  // Kích hoạt nút bật camera
  } else {
    alert("Không thể tắt camera!");
  }
};

// Chế độ phát hiện chuyển động (motion detection)
motionToggle.addEventListener("change", async () => {
  const isEnabled = motionToggle.checked;
  const response = await fetch('/security/update-motion-detection', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ enabled: isEnabled })
  });

  if (response.ok) {
    alert(isEnabled ? "Phát hiện người lạ đã bật" : "Phát hiện người lạ đã tắt");
  } else {
    alert("Không thể cập nhật phát hiện chuyển động!");
  }
});

function updateDashboardOverview() {
  document.getElementById('roomCount').textContent = Object.keys(rooms).length;

  let activeCount = 0;
  for (const devices of Object.values(rooms)) {
    for (const device of devices) {
      if (deviceStates[device] === undefined) {
        deviceStates[device] = true;
      }
      if (deviceStates[device]) {
        activeCount++;
      }
    }
  }
  document.getElementById('activeDevices').textContent = activeCount;

  // ✅ Gọi API Flask để lấy số cảnh báo
  fetch("/get-alert-count")
    .then(response => response.json())
    .then(data => {
      document.getElementById('securityWarnings').textContent = data.count || 0;
    })
    .catch(error => {
      console.error("Lỗi lấy số cảnh báo:", error);
      document.getElementById('securityWarnings').textContent = 0;
    });
}
function logout() {
  fetch("http://127.0.0.1:5000/logout", { method: "POST", credentials: "include" })
      .then(() => {
          window.location.href = "/";
      })
      .catch(error => console.error("Lỗi:", error));
}
document.addEventListener("DOMContentLoaded", () => {
  updateDashboardOverview(); // Cập nhật lần đầu khi trang load
});












