--Dữ liệu chạy trên MySQLMySQL
--host="127.0.0.1",
--        user="root",
--        password="1234567890123wQ",
--        database="smarthome",
--        port=3307





-- Tạo cơ sở dữ liệu
CREATE DATABASE IF NOT EXISTS smarthome CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE smarthome;

-- Bảng users
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `status` enum('Hoạt động','Bị khóa') DEFAULT 'Hoạt động',
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `CCCD` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Bảng user_faces
CREATE TABLE `user_faces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `image` longblob,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `face_encoding` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `email` (`email`),
  CONSTRAINT `user_faces_ibfk_1` FOREIGN KEY (`email`) REFERENCES `users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dữ liệu mẫu cho bảng users
INSERT INTO `users` (`name`, `email`, `pass`, `role`, `status`, `phone`, `address`, `CCCD`) VALUES
('Admin One', 'admin@smarthome.com', 'adminpass', 'admin', 'Hoạt động', '0123456789', '123 Admin St', '0011223344'),
('User One', 'user1@smarthome.com', 'userpass1', 'user', 'Hoạt động', '0900000001', '1 User Road', '1111111111'),
('User Two', 'user2@smarthome.com', 'userpass2', 'user', 'Hoạt động', '0900000002', '2 User Road', '2222222222'),
('User Three', 'user3@smarthome.com', 'userpass3', 'user', 'Hoạt động', '0900000003', '3 User Road', '3333333333'),
('User Four', 'user4@smarthome.com', 'userpass4', 'user', 'Hoạt động', '0900000004', '4 User Road', '4444444444'),
('User Five', 'user5@smarthome.com', 'userpass5', 'user', 'Hoạt động', '0900000005', '5 User Road', '5555555555'),
('User Six', 'user6@smarthome.com', 'userpass6', 'user', 'Hoạt động', '0900000006', '6 User Road', '6666666666'),
('User Seven', 'user7@smarthome.com', 'userpass7', 'user', 'Hoạt động', '0900000007', '7 User Road', '7777777777'),
('User Eight', 'user8@smarthome.com', 'userpass8', 'user', 'Hoạt động', '0900000008', '8 User Road', '8888888888'),
('User Nine', 'user9@smarthome.com', 'userpass9', 'user', 'Hoạt động', '0900000009', '9 User Road', '9999999999');
