-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema players_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema players_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `players_db` DEFAULT CHARACTER SET utf8 ;
USE `players_db` ;

-- -----------------------------------------------------
-- Table `players_db`.`hitters`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `players_db`.`hitters` ;

CREATE TABLE IF NOT EXISTS `players_db`.`hitters` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `rhp` DOUBLE NULL,
  `lhp` DOUBLE NULL,
  `hpflyball` DOUBLE NULL,
  `hppower` DOUBLE NULL,
  `hpavg` DOUBLE NULL,
  `hpfinesse` DOUBLE NULL,
  `hphome` DOUBLE NULL,
  `hpaway` DOUBLE NULL,
  `hpgroundball` DOUBLE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `players_db`.`pitchers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `players_db`.`pitchers` ;

CREATE TABLE IF NOT EXISTS `players_db`.`pitchers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `rhb` DOUBLE NULL,
  `lhb` DOUBLE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
