-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema subscriptions
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema subscriptions
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `subscriptions` DEFAULT CHARACTER SET utf8 ;
USE `subscriptions` ;

-- -----------------------------------------------------
-- Table `subscriptions`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `subscriptions`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `subscriptions`.`magazines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `subscriptions`.`magazines` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_magazines_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_magazines_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `subscriptions`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `subscriptions`.`subscriptions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `subscriptions`.`subscriptions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `magazine_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_magazines_magazines1_idx` (`magazine_id` ASC) VISIBLE,
  INDEX `fk_users_has_magazines_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_magazines_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `subscriptions`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_users_has_magazines_magazines1`
    FOREIGN KEY (`magazine_id`)
    REFERENCES `subscriptions`.`magazines` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
