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
