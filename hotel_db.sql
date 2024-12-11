/*
SQLyog Professional v13.1.1 (64 bit)
MySQL - 8.0.30 : Database - hotel_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`hotel_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `hotel_db`;

/*Table structure for table `customers` */

DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `customers` */

insert  into `customers`(`id`,`name`,`email`,`phone`,`address`) values 
(1,'frankie steinlie','fs@gmail.com','08883866931','medan'),
(3,'frankie','N/A','123','N/A'),
(4,'frankie','N/A','123','N/A');

/*Table structure for table `facilities` */

DROP TABLE IF EXISTS `facilities`;

CREATE TABLE `facilities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `facility_name` varchar(100) NOT NULL,
  `description` text,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `facilities` */

insert  into `facilities`(`id`,`facility_name`,`description`,`price`) values 
(3,'Personal Chef','Koki personal di kamar',5000000),
(4,'coba','coba',123),
(6,'bioskop','ruangan teater',400000);

/*Table structure for table `payments` */

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reservation_id` int NOT NULL,
  `payment_date` date NOT NULL,
  `amount` int NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `payments` */

insert  into `payments`(`id`,`reservation_id`,`payment_date`,`amount`,`payment_method`,`created_at`,`updated_at`) values 
(1,1,'2024-12-11',35012300,'Cash','2024-12-11 10:49:44','2024-12-11 10:49:44'),
(2,1,'2024-12-11',35012300,'Cash','2024-12-11 10:51:23','2024-12-11 10:51:23'),
(3,1,'2024-12-11',35012300,'Cash','2024-12-11 11:09:12','2024-12-11 11:09:12'),
(4,1,'2024-12-11',35012300,'Cash','2024-12-11 11:11:52','2024-12-11 11:11:52'),
(5,1,'2024-12-11',35012300,'Cash','2024-12-11 11:13:41','2024-12-11 11:13:41'),
(6,1,'2024-12-11',35012300,'Cash','2024-12-11 11:15:14','2024-12-11 11:15:14'),
(7,1,'2024-12-11',35012300,'Cash','2024-12-11 11:17:52','2024-12-11 11:17:52');

/*Table structure for table `reservation_facilities` */

DROP TABLE IF EXISTS `reservation_facilities`;

CREATE TABLE `reservation_facilities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reservation_id` int DEFAULT NULL,
  `facility_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reservation_id` (`reservation_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `reservation_facilities_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`id`),
  CONSTRAINT `reservation_facilities_ibfk_2` FOREIGN KEY (`facility_id`) REFERENCES `facilities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `reservation_facilities` */

insert  into `reservation_facilities`(`id`,`reservation_id`,`facility_id`) values 
(1,1,4);

/*Table structure for table `reservation_rooms` */

DROP TABLE IF EXISTS `reservation_rooms`;

CREATE TABLE `reservation_rooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reservation_id` int DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reservation_id` (`reservation_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `reservation_rooms_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`id`),
  CONSTRAINT `reservation_rooms_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `reservation_rooms` */

/*Table structure for table `reservations` */

DROP TABLE IF EXISTS `reservations`;

CREATE TABLE `reservations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `total_people` int NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `status` enum('Pending','Confirmed','Completed','Cancelled') DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `reservations` */

insert  into `reservations`(`id`,`customer_id`,`check_in_date`,`check_out_date`,`total_people`,`total_price`,`status`,`created_at`) values 
(1,4,'2024-12-11','2024-12-13',1,350123.00,'Pending','2024-12-11 11:36:35');

/*Table structure for table `room_types` */

DROP TABLE IF EXISTS `room_types`;

CREATE TABLE `room_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) NOT NULL,
  `description` text,
  `price` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `room_types` */

insert  into `room_types`(`id`,`type_name`,`description`,`price`) values 
(1,'Standard','Kamar nyaman dengan fasilitas modern',500000),
(2,'Executive','Kamar dasar untuk satu orang',1500000),
(3,'Deluxe','Suite mewah dengan kolam renang pribadi',2500000),
(4,'Suite','Kamar luas dengan tempat tidur king-size',3000000),
(5,'Presidential','Kamar terbaik dengan fasilitas lengkappppppp',15000000),
(6,'Coba','coba',1234570),
(8,'qwerty','kepo',350000);

/*Table structure for table `rooms` */

DROP TABLE IF EXISTS `rooms`;

CREATE TABLE `rooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_number` varchar(10) NOT NULL,
  `room_type_id` int DEFAULT NULL,
  `status` enum('Tersedia','Terisi') DEFAULT 'Tersedia',
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_number` (`room_number`),
  KEY `room_type_id` (`room_type_id`),
  CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`room_type_id`) REFERENCES `room_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `rooms` */

insert  into `rooms`(`id`,`room_number`,`room_type_id`,`status`) values 
(1,'101',1,'Tersedia'),
(2,'102',2,'Terisi'),
(3,'103',3,'Tersedia'),
(4,'104',4,'Terisi'),
(5,'105',5,'Tersedia'),
(6,'106',3,'Tersedia');

/*Table structure for table `vouchers` */

DROP TABLE IF EXISTS `vouchers`;

CREATE TABLE `vouchers` (
  `code` varchar(10) NOT NULL,
  `discount_percentage` decimal(5,2) NOT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `vouchers` */

insert  into `vouchers`(`code`,`discount_percentage`,`valid_from`,`valid_to`,`is_active`) values 
('SAY10',10.00,'2024-01-01','2024-12-31',1),
('SAY5',5.00,'2024-01-01','2024-12-31',1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
