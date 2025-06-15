create database goals_inter;

use  goals_inter;

CREATE TABLE `goals` (
  `goal_id` INT NOT NULL AUTO_INCREMENT,
  
  -- User Information
  `login_name` VARCHAR(45) NOT NULL,

  -- Goal Information
  `goal_name` VARCHAR(45) DEFAULT NULL,
  `goal_type` VARCHAR(45) DEFAULT NULL,
  `goal_description` VARCHAR(1024) DEFAULT NULL,
  `goal_duration` INT DEFAULT NULL,
  `tags` VARCHAR(255) DEFAULT NULL,
  `category` VARCHAR(45) DEFAULT NULL,

  -- URLs
  `goal_url` VARCHAR(300) DEFAULT NULL,
  `goal_image_url` VARCHAR(300) DEFAULT NULL,

  -- Pricing & Currency
  `price` VARCHAR(10) DEFAULT NULL,
  `amount` DECIMAL(8,2) DEFAULT '0.00',
  `discount` DECIMAL(8,2) DEFAULT '0.00',
  `currency_type` VARCHAR(4) DEFAULT NULL,

  -- Metrics
  `rating` DECIMAL(1,1) DEFAULT NULL,
  `popularity` VARCHAR(300) DEFAULT NULL,

  -- Status Flags
  `goal_status` TINYINT(1) DEFAULT '0',
  `published` TINYINT(1) DEFAULT '0',
  `archived` TINYINT(1) NOT NULL DEFAULT '0',

  -- Audit Fields
  `action` VARCHAR(45) DEFAULT NULL,
  `actionBy` VARCHAR(45) DEFAULT NULL,
  `createdAt` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP,

  -- Primary Key
  PRIMARY KEY (`goal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb3;


drop table goals_templates;


select * from goals;






CREATE TABLE `services` (
  `service_id` INT NOT NULL AUTO_INCREMENT,

  -- User Information
  `login_name` VARCHAR(45) NOT NULL,

  -- Service Details
  `service_name` VARCHAR(45) DEFAULT NULL,
  `service_type` VARCHAR(45) DEFAULT NULL,
  `service_description` VARCHAR(1024) DEFAULT NULL,
  `service_duration` INT DEFAULT NULL,

  -- Media & Links
  `service_url` VARCHAR(300) DEFAULT NULL,
  `service_image_url` VARCHAR(300) DEFAULT NULL,

  -- Status Flags
  `service_status` TINYINT(1) DEFAULT '0',
  `published` TINYINT(1) DEFAULT '0',
  `archived` TINYINT(1) NOT NULL DEFAULT '0',

  -- Audit Information
  `action` VARCHAR(45) DEFAULT NULL,
  `actionBy` VARCHAR(45) DEFAULT NULL,
  `createdAt` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` DATETIME DEFAULT NULL,

  -- Primary Key
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=341 DEFAULT CHARSET=utf8mb3;

select * from services;




CREATE TABLE `goals_services` (
  -- Composite Key Columns
  `goal_id` INT NOT NULL,
  `service_type` VARCHAR(45) NOT NULL,
  `service_id` INT NOT NULL,

  -- Relationship Details
  `order_index` TINYINT DEFAULT '0',
  `status` TINYINT(1) DEFAULT '0',

  -- Audit Fields
  `action` VARCHAR(45) DEFAULT NULL,
  `action_by` VARCHAR(45) DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP,

  -- Primary Key (composite)
  PRIMARY KEY (`goal_id`, `service_type`, `service_id`),

  -- Indexes for faster joins/queries
  KEY `fk_goal_has_service_goal1_idx` (`goal_id`),
  KEY `fk_goal_has_service_goal2_idx` (`service_type`),
  KEY `fk_goal_has_service_goal3_idx` (`service_id`),

  -- Foreign Key Constraint
  CONSTRAINT `fk_goal_has_service_template1` 
    FOREIGN KEY (`goal_id`) 
    REFERENCES `goals` (`goal_id`)
    ON DELETE CASCADE ON UPDATE CASCADE

  -- NOTE: Consider adding foreign key for `service_template_id` if desired
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


select * from goals_services;


drop table goals;
**************************************************************************************************************************************************************************************





CREATE TABLE `services_templates` (
 `service_template_id` int NOT NULL AUTO_INCREMENT,
 `service_name` varchar(45) DEFAULT NULL,
 `service_type` varchar(45) DEFAULT NULL,
 `service_duration` int DEFAULT NULL,
 `service_url` varchar(300) DEFAULT NULL,
 `service_image_url` varchar(300) DEFAULT NULL,
 `service_description` varchar(1024) DEFAULT NULL,
 `service_status` tinyint(1) DEFAULT '0',
 `published` tinyint(1) DEFAULT '0',
 PRIMARY KEY (`service_template_id`)
) ENGINE=InnoDB AUTO_INCREMENT=341 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `goals_templates` (
 `goal_template_id` int NOT NULL AUTO_INCREMENT,
 `goal_name` varchar(45) DEFAULT NULL,
 `goal_type` varchar(45) DEFAULT NULL,
 `goal_duration` int DEFAULT NULL,
 `goal_url` varchar(300) DEFAULT NULL,
 `goal_image_url` varchar(300) DEFAULT NULL,
 `goal_description` varchar(1024) DEFAULT NULL,

 PRIMARY KEY (`goal_template_id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `goals_services_templates` (
 `goal_template_id` int NOT NULL,
 `service_type` varchar(45) NOT NULL,
 `service_template_id` int NOT NULL,
 `order_index` tinyint DEFAULT '0',
 `status` tinyint(1) DEFAULT '0',
 `action` varchar(45) DEFAULT NULL,
 PRIMARY KEY (`goal_template_id`,`service_type`,`service_template_id`),
 KEY `fk_goal_has_service_goal1_idx` (`goal_template_id`),
 KEY `fk_goal_has_service_goal2_idx` (`service_type`),
 KEY `fk_goal_has_service_goal3_idx` (`service_template_id`),
 CONSTRAINT `fk_goal_has_service_template1` FOREIGN KEY (`goal_template_id`) REFERENCES `goals_templates` (`goal_template_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


select * from goals_services_templates;
select * from goals_templates;
select * from services_templates;

SELECT goal_template_id,goal_description FROM goals_templates;

drop table goals_templates;

INSERT INTO goals_templates (goal_template_id, goal_description)
VALUES
(1, 'Phase 1: Fundamentals\n1. Learn Java basics:\n    - Data types\n    - Variables\n    - Operators\n    - Control structures\n    - Functions\n    - Object-Oriented Programming (OOP) concepts\n2. Familiarize yourself with Java Development Kit (JDK) and Integrated Development Environments (IDEs) like Eclipse or IntelliJ.\n\nPhase 2: Java Programming\n1. Learn advanced Java concepts:\n    - Exception handling\n    - Multithreading\n    - Collections framework\n    - File I/O\n    - Networking\n2. Practice coding:\n    - Solve problems on platforms like LeetCode, HackerRank, or CodeWars\n    - Build small projects\n\nPhase 3: Java Frameworks and Libraries\n1. Learn popular Java frameworks:\n    - Spring\n    - Hibernate\n    - JavaFX\n2. Understand how to use libraries for tasks like:\n    - Database connectivity\n    - Networking\n    - File I/O\n\nPhase 4: Project Development\n1. Develop a personal project:\n    - Choose a project idea that interests you\n    - Apply Java concepts and frameworks learned earlier\n2. Improve problem-solving skills:\n    - Participate in coding challenges or hackathons\n    - Learn design patterns, principles, and best practices'),

(2, 'Phase 1: Fundamentals\n1. Learn Python basics:\n    - Data types\n    - Variables\n    - Operators\n    - Control structures\n    - Functions\n    - Modules\n2. Familiarize yourself with:\n    - Python syntax\n    - Indentation\n    - Basic data structures (lists, dictionaries, sets)\n\nPhase 2: Python Programming\n1. Learn advanced Python concepts:\n    - Object-Oriented Programming (OOP)\n    - Decorators\n    - Generators\n    - File I/O\n    - Exception handling\n2. Practice coding:\n    - Solve problems on platforms like LeetCode, HackerRank, or CodeWars\n    - Build small projects (e.g., command-line tools, games)\n\nPhase 3: Python Libraries and Frameworks\n1. Learn popular Python libraries:\n    - NumPy\n    - Pandas\n    - Matplotlib\n    - Scikit-learn\n2. Familiarize yourself with frameworks:\n    - Flask\n    - Django\n    - Pyramid\n\nPhase 4: Data Science and Machine Learning\n1. Learn data science concepts:\n    - Data cleaning\n    - Data visualization\n    - Statistical analysis\n2. Learn machine learning:\n    - Supervised learning\n    - Unsupervised learning\n    - Deep learning\n\nPhase 5: Project Development\n1. Develop a personal project:\n    - Choose a project idea that interests you\n    - Apply Python concepts and libraries learned earlier\n2. Improve problem-solving skills:\n    - Participate in coding challenges or hackathons\n    - Learn design patterns, principles, and best practices');
