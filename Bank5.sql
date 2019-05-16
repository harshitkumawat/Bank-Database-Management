-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 13, 2019 at 04:14 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Bank5`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `account_no` varchar(20) NOT NULL,
  `name` text NOT NULL,
  `address` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact_no` varchar(10) NOT NULL,
  `account_type` text NOT NULL,
  `balance` int(10) NOT NULL,
  `open_date` date NOT NULL,
  `status` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`account_no`, `name`, `address`, `email`, `contact_no`, `account_type`, `balance`, `open_date`, `status`) VALUES
('10017043377227', 'Raj Patel', 'Rajkot', 'rajp@gmail.com', '7043377227', 'current', 2500, '2018-03-11', 'open'),
('10018197205950', 'Harshit Kumawat', 'Surat', 'harshit@gmail.com', '8197205950', 'saving', 7500, '2019-02-12', 'open'),
('10018310440109', 'Raavi Kaushik', 'Bengaluru', 'raavikaushik48@gmail.com', '8310440109', 'FD', 9500, '2019-05-21', 'open'),
('10019725462705', 'Neel Patel', 'Mumbai', 'neelp@gmail.com', '9725462705', 'saving', 4000, '2019-01-20', 'open');

-- --------------------------------------------------------

--
-- Table structure for table `fd`
--

CREATE TABLE `fd` (
  `account_no` varchar(20) NOT NULL,
  `fd_account_no` varchar(20) NOT NULL,
  `amount` int(10) NOT NULL,
  `duration` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fd`
--

INSERT INTO `fd` (`account_no`, `fd_account_no`, `amount`, `duration`) VALUES
('10018310440109', '1FD8310440109', 2000, '12'),
('10018310440109', '2FD8310440109', 7500, '24');

-- --------------------------------------------------------

--
-- Table structure for table `loan`
--

CREATE TABLE `loan` (
  `account_no` varchar(20) NOT NULL,
  `loan_no` varchar(20) NOT NULL,
  `amount` int(10) NOT NULL,
  `repayment_term` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `loan`
--

INSERT INTO `loan` (`account_no`, `loan_no`, `amount`, `repayment_term`) VALUES
('10018197205950', '1LN8197205950', 5000, '24');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `user_name` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`user_name`, `password`) VALUES
('10017043377227', 'Raj123'),
('10018197205950', 'Harshit123'),
('10018310440109', 'Raavi123'),
('10019725462705', 'Neel123');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `trans_id` int(10) NOT NULL,
  `trans_type` text NOT NULL,
  `account_no` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `amount` int(10) NOT NULL,
  `account_type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`trans_id`, `trans_type`, `account_no`, `date`, `amount`, `account_type`) VALUES
(1, 'Credited', '10018197205950', '2019-04-13', 2000, 'saving'),
(2, 'Debited', '10018197205950', '2019-04-13', 500, 'saving'),
(3, 'Credited', '10018310440109', '2019-04-13', 2000, '1FD8310440109'),
(4, 'Credited', '10018310440109', '2019-04-13', 5500, '2FD8310440109'),
(5, 'Credited', '10017043377227', '2019-04-13', 5500, 'current'),
(6, 'Debited', '10017043377227', '2019-04-13', 1000, 'current'),
(7, 'Credited', '10018197205950', '2019-04-13', 1000, 'saving'),
(8, 'Debited', '10017043377227', '2019-04-13', 2000, 'current'),
(9, 'Credited', '10018310440109', '2019-04-13', 2000, '2FD8310440109'),
(10, 'Credited', '10018197205950', '2019-04-13', 5000, '1LN8197205950'),
(11, 'Credited', '10019725462705', '2019-04-13', 3000, 'saving'),
(12, 'Credited', '10019725462705', '2019-04-13', 1000, 'saving');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`account_no`);

--
-- Indexes for table `fd`
--
ALTER TABLE `fd`
  ADD PRIMARY KEY (`fd_account_no`),
  ADD KEY `account_no` (`account_no`);

--
-- Indexes for table `loan`
--
ALTER TABLE `loan`
  ADD PRIMARY KEY (`loan_no`),
  ADD KEY `account_no` (`account_no`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`user_name`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`trans_id`),
  ADD KEY `account_no` (`account_no`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fd`
--
ALTER TABLE `fd`
  ADD CONSTRAINT `fd_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `customer` (`account_no`);

--
-- Constraints for table `loan`
--
ALTER TABLE `loan`
  ADD CONSTRAINT `loan_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `customer` (`account_no`);

--
-- Constraints for table `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`user_name`) REFERENCES `customer` (`account_no`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `customer` (`account_no`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
