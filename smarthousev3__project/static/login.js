async function checkLogin(event) {
    event.preventDefault(); // Ngăn form submit mặc định

    let email = document.getElementById("email").value;
    let password = document.getElementById("pass").value;

    let response = await fetch("/check-login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ email, pass: password })
    });

    try {
        let data = await response.json();
        console.log(data);

        if (data.success) {
            alert("Đăng nhập thành công! Chào " + data.name);
            window.location.href = data.role === "admin" ? "/admin" : "/index-vi";
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error("Lỗi: Server không trả về JSON hợp lệ!", error);
    }
}

    function showForgotForm() {
            document.getElementById("formBlock").style.display = "none";
            document.getElementById("forgotPasswordForm").style.display = "block";
        }

        function sendEmailToAdmin() {
            let phone = document.getElementById("forgotPhone").value;
            let cccd = document.getElementById("forgotCCCD").value;

            if (!phone || !cccd) {
                alert("Vui lòng nhập đầy đủ thông tin!");
                return;
            }

            let adminEmail = "yukiyukine123@gmail.com";
            let subject = encodeURIComponent("Yêu cầu cấp lại mật khẩu");
            let body = encodeURIComponent(`Thông tin người yêu cầu:\n- SĐT: ${phone}\n- CCCD: ${cccd}`);

            let gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${adminEmail}&su=${subject}&body=${body}`;
            
            let newTab = window.open(gmailLink, "_blank");

            if (!newTab) {
                alert("Trình duyệt có thể đang chặn cửa sổ bật lên. Hãy cho phép pop-up và thử lại!");
            } else {
                alert("Yêu cầu đã được gửi.");
                closeForm();
            }
        }

        function closeForm() {
            document.getElementById("forgotPasswordForm").style.display = "none";
            document.getElementById("formBlock").style.display = "block";
        }

        // Gán sự kiện bằng JavaScript thay vì dùng `onclick` trong HTML
        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("sendRequestBtn").addEventListener("click", sendEmailToAdmin);
        });

        let currentStream = null;

        function startFaceLogin() {
            console.log("👉 Bắt đầu hàm startFaceLogin");
        
            // Ẩn form đăng nhập, hiện Face ID
            document.querySelector(".formBlock").style.display = "none";
            document.getElementById("faceLoginContainer").style.display = "block";
        
            const video = document.getElementById("video");
        
            // Dừng stream cũ nếu còn
            if (currentStream) {
                console.log("🔁 Dừng stream cũ");
                currentStream.getTracks().forEach(track => track.stop());
                currentStream = null;
            }
        
            // Reset video
            video.srcObject = null;
        
            console.log("📸 Gọi getUserMedia...");
        
            // Yêu cầu mở webcam
            navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        console.log("✅ [getUserMedia] Thành công - camera được mở");
        currentStream = stream;
        video.srcObject = stream;
        return video.play();
    })
    .catch((err) => {
        console.error("❌ [getUserMedia] Lỗi truy cập webcam:", err);
        alert("Không thể truy cập webcam: " + err.message);
        cancelFaceLogin(); // quay lại form
    });
        }
        function captureAndLogin() {
            const canvas = document.getElementById("canvas");
            const video = document.getElementById("video");
            const context = canvas.getContext("2d");
        
            // Chụp hình từ webcam
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
            const imageData = canvas.toDataURL("image/jpeg");
        
            // Gửi đến server
            fetch("/api/users/login-face", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ image: imageData }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Đăng nhập thành công với email: " + data.email);
                    // Ví dụ: lưu email vào localStorage hoặc chuyển trang
                    // localStorage.setItem("user_email", data.email);
                    window.location.href = "/dashboard"; // hoặc route bạn muốn
                } else {
                    alert("Đăng nhập thất bại: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Lỗi:", error);
                alert("Lỗi đăng nhập bằng Face ID!");
            });
        }
        function cancelFaceLogin() {
            console.log("🔙 Hủy Face ID, quay về form đăng nhập");
        
            // Ẩn form Face ID, hiện lại login
            document.getElementById("faceLoginContainer").style.display = "none";
            document.querySelector(".formBlock").style.display = "block";
        
            // Dừng webcam nếu đang mở
            if (currentStream) {
                console.log("🛑 Dừng stream hiện tại");
                currentStream.getTracks().forEach(track => track.stop());
                currentStream = null;
            }
        
            const video = document.getElementById("video");
            video.srcObject = null;
        }
        
        
               
