-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 01, 2018 at 11:11 PM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.1.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `auto-oglasi`
--

-- --------------------------------------------------------

--
-- Table structure for table `car_makes`
--

CREATE TABLE `car_makes` (
  `id` int(10) UNSIGNED NOT NULL,
  `make` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `car_makes`
--

INSERT INTO `car_makes` (`id`, `make`) VALUES
(1, 'Alfa Romeo'),
(2, 'Audi'),
(3, 'BMW'),
(4, 'Citroen'),
(5, 'Lada');

-- --------------------------------------------------------

--
-- Table structure for table `car_models`
--

CREATE TABLE `car_models` (
  `id` int(10) UNSIGNED NOT NULL,
  `model` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `make_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `car_models`
--

INSERT INTO `car_models` (`id`, `model`, `make_id`) VALUES
(1, '33', 1),
(2, '75', 1),
(3, 'A1', 2),
(4, 'A2', 2),
(5, 'X5', 3),
(6, 'X6', 3),
(7, 'C1', 4),
(8, 'Xsara Picasso', 4),
(9, 'Niva', 5),
(10, 'Kalina', 5);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(10) UNSIGNED NOT NULL,
  `model_id` int(10) UNSIGNED NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `year` year(4) NOT NULL,
  `price` int(10) UNSIGNED NOT NULL,
  `km` int(10) UNSIGNED NOT NULL,
  `status` enum('New','Used') COLLATE utf8mb4_unicode_ci NOT NULL,
  `kw` int(10) UNSIGNED NOT NULL,
  `hp` int(10) UNSIGNED NOT NULL,
  `ccm` int(10) UNSIGNED NOT NULL,
  `fuel_type` enum('Diesel','Gasoline','LPG','Other') COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `model_id`, `user_id`, `year`, `price`, `km`, `status`, `kw`, `hp`, `ccm`, `fuel_type`, `description`, `phone`, `address`) VALUES
(1, 10, 1, 2007, 10000, 1, 'New', 60, 81, 1596, 'Gasoline', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla commodo orci nec enim sodales pulvinar. Maecenas scelerisque lacinia felis, non ullamcorper turpis. Ut ornare velit tincidunt est ornare euismod. Phasellus et rutrum mi, at volutpat ipsum. Praesent vulputate, dui tempus commodo dignissim, eros odio sagittis quam, id fringilla turpis metus et ipsum. Aliquam accumsan convallis dolor non porta. Aenean nec massa quis lorem scelerisque tincidunt id vitae magna. Nam non diam mauris.', '0631234567', 'Bulevar Kralja Petra I 1\r\n21000 Novi Sad');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `surname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` char(66) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `surname`, `email`, `password`, `is_admin`) VALUES
(1, 'Admin', 'Admin', 'admin@admin.com', '$2b$12$eMT0Lx9XEHRTuYNoyrGAB.ZjDILtPlfRVFRSFYNCzqJnvnbcktnG2', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `car_makes`
--
ALTER TABLE `car_makes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `car_models`
--
ALTER TABLE `car_models`
  ADD PRIMARY KEY (`id`),
  ADD KEY `car_models_make_id_foreign` (`make_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_model_id_foreign` (`model_id`),
  ADD KEY `products_user_id_foreign` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `car_makes`
--
ALTER TABLE `car_makes`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `car_models`
--
ALTER TABLE `car_models`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `car_models`
--
ALTER TABLE `car_models`
  ADD CONSTRAINT `car_models_make_id_foreign` FOREIGN KEY (`make_id`) REFERENCES `car_makes` (`id`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_model_id_foreign` FOREIGN KEY (`model_id`) REFERENCES `car_models` (`id`),
  ADD CONSTRAINT `products_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
