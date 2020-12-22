-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema gun
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gun
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gun` DEFAULT CHARACTER SET utf8 ;
USE `gun` ;

-- -----------------------------------------------------
-- Table `gun`.`dim_date`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_date` (
  `dim_date_id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `day` INT NULL,
  `month` INT NULL,
  `year` INT NULL,
  PRIMARY KEY (`dim_date_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`dim_participant_age`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_participant_age` (
  `dim_participant_age_id` INT NOT NULL,
  `participant_age` INT NULL,
  `participant_age_group` INT NULL,
  PRIMARY KEY (`dim_participant_age_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`dim_participant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_participant` (
  `dim_participant_id` INT NOT NULL,
  `gender` VARCHAR(45) NULL,
  `name` VARCHAR(150) NULL,
  `relationship` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `dim_participant_age_id` INT NOT NULL,
  PRIMARY KEY (`dim_participant_id`),
  INDEX `fk_dim_participant_dim_participant_age1_idx` (`dim_participant_age_id` ASC) VISIBLE,
  CONSTRAINT `fk_dim_participant_dim_participant_age1`
    FOREIGN KEY (`dim_participant_age_id`)
    REFERENCES `gun`.`dim_participant_age` (`dim_participant_age_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`dim_gun`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_gun` (
  `dim_gun_id` INT NOT NULL,
  `gun_type` VARCHAR(45) NULL,
  `gun_stolen` INT NULL,
  PRIMARY KEY (`dim_gun_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`dim_incident_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_incident_info` (
  `dim_incident_info_id` INT NOT NULL,
  `incident_characteristics` VARCHAR(45) NULL,
  `notes` VARCHAR(45) NULL,
  PRIMARY KEY (`dim_incident_info_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`dim_state_district`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_state_district` (
  `dim_state_district_id` INT NOT NULL,
  `senate` INT NULL,
  `house` INT NULL,
  PRIMARY KEY (`dim_state_district_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`dim_location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`dim_location` (
  `dim_location_id` INT NOT NULL,
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
    REFERENCES `gun`.`dim_state_district` (`dim_state_district_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gun`.`facts_gun_incident`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gun`.`facts_gun_incident` (
  `incident_id` INT NOT NULL,
  `n_killed` INT NULL,
  `n_injured` INT NULL,
  `n_guns_involved` INT NULL,
  `dim_participant_id` INT NOT NULL,
  `dim_date_id` INT NOT NULL,
  `dim_gun_id` INT NOT NULL,
  `dim_incident_info_id` INT NOT NULL,
  `dim_location_id` INT NOT NULL,
  PRIMARY KEY (`incident_id`),
  INDEX `fk_facts_gun_incident_dim_participant_idx` (`dim_participant_id` ASC) VISIBLE,
  INDEX `fk_facts_gun_incident_dim_date1_idx` (`dim_date_id` ASC) VISIBLE,
  INDEX `fk_facts_gun_incident_dim_gun1_idx` (`dim_gun_id` ASC) VISIBLE,
  INDEX `fk_facts_gun_incident_dim_incident_info1_idx` (`dim_incident_info_id` ASC) VISIBLE,
  INDEX `fk_facts_gun_incident_dim_location1_idx` (`dim_location_id` ASC) VISIBLE,
  CONSTRAINT `fk_facts_gun_incident_dim_participant`
    FOREIGN KEY (`dim_participant_id`)
    REFERENCES `gun`.`dim_participant` (`dim_participant_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facts_gun_incident_dim_date1`
    FOREIGN KEY (`dim_date_id`)
    REFERENCES `gun`.`dim_date` (`dim_date_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facts_gun_incident_dim_gun1`
    FOREIGN KEY (`dim_gun_id`)
    REFERENCES `gun`.`dim_gun` (`dim_gun_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facts_gun_incident_dim_incident_info1`
    FOREIGN KEY (`dim_incident_info_id`)
    REFERENCES `gun`.`dim_incident_info` (`dim_incident_info_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facts_gun_incident_dim_location1`
    FOREIGN KEY (`dim_location_id`)
    REFERENCES `gun`.`dim_location` (`dim_location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
