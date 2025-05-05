const describe = `Chào mừng đến với Trang Quản Trị Hệ Thống! <br><br>

Chúng tôi rất vui mừng được chào đón bạn đến với giao diện quản trị của hệ thống.
Đây là nơi bạn có thể theo dõi và quản lý tất cả các hoạt động,
bao gồm việc quản lý khách hàng cũng như cách feedbacks.<br><br>

Trang quản trị của chúng tôi được thiết kế với mục tiêu giúp bạn dễ dàng quản lý và
tối ưu hóa hiệu suất của ứng dụng trực tuyến. Tất cả dữ liệu được tổ chức rõ ràng,
dễ dàng truy cập, giúp bạn ra quyết định nhanh chóng và hiệu quả.
Bạn có thể thêm, sửa, xóa các dữ liệu, theo dõi các phản hồi mới nhất
để nâng cao chất lượng ứng dụng.<br>

Các tính năng chính:<br><br>

✔ Quản lý Người dùng: Quản lý tài khoản khách hàng, hỗ trợ chăm sóc khách hàng nhanh chóng.<br>
✔ Feed back: Nhận những yêu cầu, hỗ trợ chăm sóc khách hàng nhanh chóng.<br>`;


document.addEventListener("DOMContentLoaded", function () {
    let descElement = document.getElementById("adminDescription");
    if (descElement) {
        descElement.innerHTML = describe;
    } else {
        console.error("❌ Không tìm thấy phần tử #adminDescription trong HTML.");
    }
});
function showAdminInfo() {
    if (adminData.role !== "admin") {
        window.location.href = "login.html"; // Chuyển hướng nếu không phải admin
        return;
    }

    let topbar = document.getElementById("container");
    let item = document.createElement("div");
    item.classList.add("topBar");
    item.innerHTML = `
        <img src="static/images/admin_avt.jpg" alt="Avatar">
        <p>
            ${adminData.name}  
            <i class="fa-solid fa-right-to-bracket" onclick="logout()"></i> 
        </p>
    `;

    let firstChild = document.getElementById("CONTENT");
    topbar.insertBefore(item, firstChild);
}

// Hàm đăng xuất
function logout() {
    fetch("http://127.0.0.1:5000/logout", { method: "POST", credentials: "include" })
        .then(() => {
            window.location.href = "/";
        })
        .catch(error => console.error("Lỗi:", error));
}

// Gọi hàm khi trang tải xong
document.addEventListener("DOMContentLoaded", showAdminInfo);



/*quản lý tài khoản*/
document.querySelector("li#statistics").addEventListener("click", () => {
    document.getElementById("user-management").style.display = "block";
  
    // Gọi API từ Flask
    fetch("/api/users")
      .then(response => response.json())
      .then(data => renderUsers(data));
  });
  
  function renderUsers(users) {
    const tbody = document.querySelector("#user-table tbody");
    tbody.innerHTML = "";
  
    users.forEach((user, index) => {
      const row = document.createElement("tr");
  
      row.innerHTML = `
        <td>${index + 1}</td>      
        <td style="display: none">${user.id}</td>  
        <td>${user.name}</td>
        <td>${user.address}</td>
        <td>${user.email}</td>
        <td>${user.pass}</td>
        <td>${user.phone}</td>
        <td>${user.CCCD}</td>
        <td>${user.status}</td>
        <td>
          <button onclick="editUser(${index})">Sửa</button>
          <button onclick="deleteUser(${index})">Xóa</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  }
  function showSection(sectionId) {
    const sections = ["homeContent", "user-management", "feedback-content"];
    
    sections.forEach(id => {
      const element = document.getElementById(id);
      if (element) {
        element.style.display = (id === sectionId) ? "block" : "none";
      }
    });
  }
  
  // Khi click vào từng mục trong sidebar:
  document.querySelector("li#home").addEventListener("click", () => {
    showSection("homeContent");
  });
  
  document.querySelector("li#statistics").addEventListener("click", () => {
    showSection("user-management");
    fetch("/api/users")
      .then(response => response.json())
      .then(data => renderUsers(data));
  });
  
  document.querySelector("li#feedback").addEventListener("click", () => {
    showSection("feedback-content");
  });



  function addUser() {
    const tbody = document.getElementById("user-table-body");
  
    // Tạo hàng mới với ô input
    const rowCount = tbody.querySelectorAll("tr").length + 1;
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
      <td>${rowCount}</td>
      <td><input type="text" id="new-name" placeholder="Tên"></td>
      <td><input type="text" id="new-address" placeholder="Địa chỉ"></td>
      <td><input type="email" id="new-email" placeholder="Email"></td>
      <td><input type="password" id="new-pass" placeholder="Mật khẩu"></td>
      <td><input type="text" id="new-phone" placeholder="SĐT"></td>
      <td><input type="text" id="new-CCCD" placeholder="CCCD"></td>
      <td>Hoạt động</td>
      <td>
        <button onclick="saveUser()">Lưu</button>
        <button onclick="this.closest('tr').remove()">Hủy</button>
      </td>
    `;
    tbody.appendChild(newRow);
  }
  
  function saveUser() {
    const name = document.getElementById("new-name").value;
    const address = document.getElementById("new-address").value;
    const email = document.getElementById("new-email").value;
    const pass = document.getElementById("new-pass").value;
    const phone = document.getElementById("new-phone").value;
    const cccd = document.getElementById("new-CCCD").value;
  
    if (!name || !email || !pass) {
      alert("Vui lòng nhập đầy đủ tên, email, và mật khẩu!");
      return;
    }
  
    fetch('/api/users/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, address, email, pass, phone,cccd })
    })
    .then(res => res.json())
    .then(data => {
      alert("Thêm người dùng thành công!");
      location.reload(); // Tải lại để cập nhật bảng
    })
    .catch(error => {
      console.error(error);
      alert("Có lỗi xảy ra khi thêm người dùng.");
    });
  }


  function editUser(index) {
    const row = document.querySelectorAll("#user-table-body tr")[index];
    const cells = row.children;
  
    const id = cells[1].textContent.trim();      // ✅ Lấy ID từ cột ẩn
    const name = cells[2].textContent.trim();
    const address = cells[3].textContent.trim();
    const email = cells[4].textContent.trim();
    const pass = cells[5].textContent.trim();
    const phone = cells[6].textContent.trim();
    const cccd = cells[7].textContent.trim();
    const status = cells[8].textContent.trim();
  
    row.innerHTML = `
      <td>${index + 1}</td>
      <td><input type="text" value="${name}" id="edit-name"></td>
      <td><input type="text" value="${address}" id="edit-address"></td>
      <td><input type="email" value="${email}" id="edit-email"></td>
      <td><input type="password" value="${pass}" id="edit-pass"></td>
      <td><input type="text" value="${phone}" id="edit-phone"></td>
      <td><input type="text" value="${cccd}" id="edit-cccd"></td>
      <td>
      <select id="edit-status">
        <option value="Hoạt động" ${status === "Hoạt động" ? "selected" : ""}>Hoạt động</option>
        <option value="Bị khóa" ${status === "Bị khóa" ? "selected" : ""}>Bị khóa</option>
      </select>
      </td>
      <td>
        <button onclick="saveEdit('${id}')">Lưu</button>
        <button onclick="location.reload()">Hủy</button>
      </td>
    `;
  }
  function saveEdit(id) {
    const name = document.getElementById("edit-name").value;
    const address = document.getElementById("edit-address").value;
    const email = document.getElementById("edit-email").value;
    const pass = document.getElementById("edit-pass").value;
    const phone = document.getElementById("edit-phone").value;
    const cccd = document.getElementById("edit-cccd").value;
    const status = document.getElementById("edit-status").value;
  
    fetch('/api/users/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id, name, address, email, pass, phone,cccd,status})
    })
    .then(res => res.json())
    .then(data => {
      alert("Cập nhật thành công!");
      location.reload();
    })
    .catch(err => {
      console.error(err);
      alert("Có lỗi khi cập nhật.");
    });
  }
  function deleteUser(index) {
    const row = document.querySelectorAll("#user-table-body tr")[index];
    const id = row.children[1].textContent;
  
    if (confirm(`Bạn có chắc muốn xóa người dùng ?`)) {
      fetch(`/api/users/delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id })
      })
      .then(res => res.json())
      .then(data => {
        alert("Xóa thành công!");
        location.reload();
      })
      .catch(err => {
        console.error(err);
        alert("Có lỗi khi xóa người dùng.");
      });
    }
  }
      
  
  




