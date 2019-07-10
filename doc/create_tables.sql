CREATE TABLE `dm1_visits_per_agenda` (
  `f_idAgenda` varchar(45) DEFAULT NULL,
  `f_nomAgenda` varchar(200) DEFAULT NULL,
  `f_idEspecialitat` varchar(45) DEFAULT NULL,
  `f_nomEspecialitat` varchar(100) DEFAULT NULL,
  `f_year` varchar(4) DEFAULT NULL,
  `f_month` varchar(6) DEFAULT NULL,
  `f_count` int(11) DEFAULT NULL,
  `f_monthname` varchar(45) DEFAULT NULL,
  `f_patients` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm2_newpatient_per_month_agenda` (
  `f_month` varchar(6) DEFAULT NULL,
  `f_monthname` varchar(45) DEFAULT NULL,
  `f_idAgenda` varchar(45) DEFAULT NULL,
  `f_nomAgenda` varchar(200) DEFAULT NULL,
  `f_idEspecialitat` varchar(45) DEFAULT NULL,
  `f_nomEspecialitat` varchar(100) DEFAULT NULL,
  `f_newPatients` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm2_stats_per_month` (
  `f_month` int(11) NOT NULL,
  `f_monthname` varchar(10) DEFAULT NULL,
  `f_patients` int(11) DEFAULT '0',
  `f_new_patients` int(11) DEFAULT '0',
  `f_casuals` int(11) DEFAULT '0',
  `f_fidelitzats` int(11) DEFAULT '0',
  `f_visits_casuals` int(11) DEFAULT '0',
  `f_visits_fidelitzats` int(11) DEFAULT '0',
  `f_visits` int(11) DEFAULT '0',
  `f_inc_visits` int(11) DEFAULT '0',
  `f_inc_patients` int(11) DEFAULT '0',
  `f_inc_new_patients` int(11) DEFAULT '0',
  `f_inc_casuals` int(11) DEFAULT '0',
  `f_inc_fidelitzats` int(11) DEFAULT '0',
  `f_inc_visits_casuals` int(11) DEFAULT '0',
  `f_inc_visits_fidelitzats` int(11) DEFAULT '0',
  PRIMARY KEY (`f_month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm_especialitat_agenda` (
  `f_idAgenda` varchar(50) NOT NULL,
  `f_idEspecialitat` varchar(32) DEFAULT NULL,
  `f_nomAgenda` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`f_idAgenda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm_especialitats` (
  `f_idEspecialitat` varchar(45) NOT NULL,
  `f_nomEspecialitat` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`f_idEspecialitat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm_first_visit` (
  `f_numHistoria` varchar(45) NOT NULL,
  `f_numPeticio` int(11) DEFAULT NULL,
  `f_month` varchar(6) DEFAULT NULL,
  `f_monthname` varchar(45) DEFAULT NULL,
  `f_idAgenda` varchar(45) DEFAULT NULL,
  `f_nomAgenda` varchar(200) DEFAULT NULL,
  `f_idEspecialitat` varchar(45) DEFAULT NULL,
  `f_nomEspecialitat` varchar(200) DEFAULT NULL,
  `f_lastNumPeticio` int(11) DEFAULT NULL,
  `f_lastmonth` varchar(6) DEFAULT NULL,
  `f_lastmonthname` varchar(45) DEFAULT NULL,
  `f_lastIdAgenda` varchar(45) DEFAULT NULL,
  `f_lastNomAgenda` varchar(200) DEFAULT NULL,
  `f_lastIdEspecialitat` varchar(45) DEFAULT NULL,
  `f_lastNomEspecialitat` varchar(200) DEFAULT NULL,
  `f_totalVisits` int(11) DEFAULT NULL,
  `f_agendesDiferents` int(11) DEFAULT NULL,
  PRIMARY KEY (`f_numHistoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm_load_log` (
  `f_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `f_result` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`f_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm3_callcenter_general` (
  `f_month` int(11) DEFAULT NULL,
  `f_year` int(11) DEFAULT NULL,
  `f_month_name` varchar(20) DEFAULT NULL,
  `f_day` varchar(20) DEFAULT NULL,
  `f_week_day_order` int(11) DEFAULT NULL,
  `f_week_day` varchar(45) DEFAULT NULL,
  `f_hour` varchar(2) DEFAULT NULL,
  `f_dst_id` varchar(45) DEFAULT NULL,
  `f_dst_name` varchar(45) DEFAULT NULL,
  `f_total` int(11) DEFAULT NULL,
  `f_answered` int(11) DEFAULT NULL,
  `f_not_answered` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dm3_callcenter_per_extension` (
  `f_month` int(11) DEFAULT NULL,
  `f_year` int(11) DEFAULT NULL,
  `f_month_name` varchar(20) DEFAULT NULL,
  `f_day` varchar(20) DEFAULT NULL,
  `f_week_day` varchar(45) DEFAULT NULL,
  `f_hour` varchar(2) DEFAULT NULL,
  `f_extension` varchar(10) DEFAULT NULL,
  `f_answered` int(11) DEFAULT NULL,
  `f_spoken_time` int(11) DEFAULT NULL,
  `f_average_duration` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
