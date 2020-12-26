-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema gun_violence
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gun_violence
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gun_violence` DEFAULT CHARACTER SET utf8 ;
USE `gun_violence` ;

-- -----------------------------------------------------
-- Table `gun_violence`.`dim_date`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_date` (
  `dim_date_id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `day` INT NULL,
  `month` INT NULL,
  `year` INT NULL,
  PRIMARY KEY (`dim_date_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`dim_incident_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_incident_info` (
  `dim_incident_info_id` INT NOT NULL,
  `incident_characteristics` VARCHAR(45) NULL,
  `notes` VARCHAR(45) NULL,
  PRIMARY KEY (`dim_incident_info_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`dim_state_district`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_state_district` (
  `dim_state_district_id` INT NOT NULL,
  `senate` INT NULL,
  `house` INT NULL,
  PRIMARY KEY (`dim_state_district_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`dim_location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_location` (
  `dim_location_id` INT NOT NULL AUTO_INCREMENT,
  `city_or_county` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `latitude` FLOAT NULL,
  `longitude` FLOAT NULL,
  `address` VARCHAR(45) NULL,
  `location_description` VARCHAR(45) NULL,
  `dim_state_district_id` INT NOT NULL,
  PRIMARY KEY (`dim_location_id`),
  INDEX `fk_dim_location_dim_state_district1_idx` (`dim_state_district_id` ASC) VISIBLE,
  CONSTRAINT `fk_dim_location_dim_state_district1`
    FOREIGN KEY (`dim_state_district_id`)
    REFERENCES `gun_violence`.`dim_state_district` (`dim_state_district_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`facts_gun_incident`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`facts_gun_incident` (
  `incident_id` INT NOT NULL,
  `n_killed` INT NULL,
  `n_injured` INT NULL,
  `n_guns_involved` INT NULL,
  `dim_date_id` INT NOT NULL,
  `dim_incident_info_id` INT NOT NULL,
  `dim_location_id` INT NOT NULL,
  PRIMARY KEY (`incident_id`),
  INDEX `fk_facts_gun_incident_dim_date1_idx` (`dim_date_id` ASC) VISIBLE,
  INDEX `fk_facts_gun_incident_dim_incident_info1_idx` (`dim_incident_info_id` ASC) VISIBLE,
  INDEX `fk_facts_gun_incident_dim_location1_idx` (`dim_location_id` ASC) VISIBLE,
  CONSTRAINT `fk_facts_gun_incident_dim_date1`
    FOREIGN KEY (`dim_date_id`)
    REFERENCES `gun_violence`.`dim_date` (`dim_date_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facts_gun_incident_dim_incident_info1`
    FOREIGN KEY (`dim_incident_info_id`)
    REFERENCES `gun_violence`.`dim_incident_info` (`dim_incident_info_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facts_gun_incident_dim_location1`
    FOREIGN KEY (`dim_location_id`)
    REFERENCES `gun_violence`.`dim_location` (`dim_location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`dim_gun`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_gun` (
  `dim_gun_id` INT NOT NULL AUTO_INCREMENT,
  `gun_type` VARCHAR(45) NULL,
  `gun_stolen` INT NULL,
  `facts_gun_incident_incident_id` INT NOT NULL,
  PRIMARY KEY (`dim_gun_id`),
  INDEX `fk_dim_gun_facts_gun_incident1_idx` (`facts_gun_incident_incident_id` ASC) VISIBLE,
  CONSTRAINT `fk_dim_gun_facts_gun_incident1`
    FOREIGN KEY (`facts_gun_incident_incident_id`)
    REFERENCES `gun_violence`.`facts_gun_incident` (`incident_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`dim_participant_age_group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_participant_age_group` (
  `dim_participant_age_group_id` INT NOT NULL,
  `class_age_group` VARCHAR(150) NULL,
  PRIMARY KEY (`dim_participant_age_group_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun_violence`.`dim_participant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun_violence`.`dim_participant` (
  `dim_participant_id` INT NOT NULL AUTO_INCREMENT,
  `gender` VARCHAR(45) NULL,
  `name` VARCHAR(150) NULL,
  `relationship` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `dim_participant_age_group_id` INT NOT NULL,
  `age` INT NULL,
  `facts_gun_incident_incident_id` INT NOT NULL,
  PRIMARY KEY (`dim_participant_id`),
  INDEX `fk_dim_participant_dim_participant_age1_idx` (`dim_participant_age_group_id` ASC) VISIBLE,
  INDEX `fk_dim_participant_facts_gun_incident1_idx` (`facts_gun_incident_incident_id` ASC) VISIBLE,
  CONSTRAINT `fk_dim_participant_dim_participant_age1`
    FOREIGN KEY (`dim_participant_age_group_id`)
    REFERENCES `gun_violence`.`dim_participant_age_group` (`dim_participant_age_group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dim_participant_facts_gun_incident1`
    FOREIGN KEY (`facts_gun_incident_incident_id`)
    REFERENCES `gun_violence`.`facts_gun_incident` (`incident_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
