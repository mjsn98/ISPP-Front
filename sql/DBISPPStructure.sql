--
-- Table structure for table `carrera`
--

DROP TABLE IF EXISTS carrera;
CREATE TABLE carrera (
  CarreraID int NOT NULL AUTO_INCREMENT,
  CarreraNombre varchar(255) NOT NULL,
  PRIMARY KEY (CarreraID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `orientacion`
--

DROP TABLE IF EXISTS orientacion;
CREATE TABLE orientacion (
  OrientacionID int NOT NULL AUTO_INCREMENT,
  OrientacionNombre varchar(255) NOT NULL,
  PRIMARY KEY (OrientacionID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `plandeestudio`
--

DROP TABLE IF EXISTS plandeestudio;
CREATE TABLE plandeestudio (
  PlanID int NOT NULL AUTO_INCREMENT,
  PlanNombre varchar(255) NOT NULL,
  PRIMARY KEY (PlanID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `carpo`
--

DROP TABLE IF EXISTS carpo;
CREATE TABLE carpo (
  CARPOID int NOT NULL AUTO_INCREMENT,
  CarreraID int NOT NULL,
  PlanDeEstudioID int NOT NULL,
  OrientacionID int DEFAULT NULL,
  CarpoPrograma varchar(255) DEFAULT NULL,
  estado tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (CARPOID),
  KEY CARPOCarreraID_idx (CarreraID),
  KEY CARPOOrientacionID_idx (OrientacionID),
  KEY CARPOPlanID_idx (PlanDeEstudioID),
  CONSTRAINT CARPOCarreraID FOREIGN KEY (CarreraID) REFERENCES carrera (CarreraID),
  CONSTRAINT CARPOOrientacionID FOREIGN KEY (OrientacionID) REFERENCES orientacion (OrientacionID),
  CONSTRAINT CARPOPlanID FOREIGN KEY (PlanDeEstudioID) REFERENCES plandeestudio (PlanID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `materia`
--

DROP TABLE IF EXISTS materia;
CREATE TABLE materia (
  MateriaID int NOT NULL AUTO_INCREMENT,
  MateriaNombre varchar(100) NOT NULL,
  CarpoIDMat int NOT NULL,
  `MateriaAño` int DEFAULT NULL,
  MateriaTipo varchar(100) DEFAULT NULL,
  PRIMARY KEY (MateriaID),
  KEY idcarpomat_idx (CarpoIDMat),
  CONSTRAINT idcarpomat FOREIGN KEY (CarpoIDMat) REFERENCES carpo (CARPOID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
  UsuarioID int NOT NULL AUTO_INCREMENT,
  Usuario int NOT NULL,
  UsuarioCorreo varchar(100) DEFAULT NULL,
  `UsuarioContraseña` varchar(120) DEFAULT NULL,
  `UsuarioContraseñaTemp` varchar(120) DEFAULT NULL,
  UsuarioActivo tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (UsuarioID),
  UNIQUE KEY Usuario_UNIQUE (Usuario),
  UNIQUE KEY UsuarioCorreo_UNIQUE (UsuarioCorreo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
DELIMITER ;;
/*!50003 CREATE*/ /*!50003 TRIGGER `InsertTempPassword` BEFORE INSERT ON `usuario` FOR EACH ROW BEGIN
	IF (NEW.UsuarioContraseñaTemp IS NULL) THEN
		SET NEW.UsuarioContraseñaTemp := NEW.Usuario;
	END IF;
END */;;
DELIMITER ;


--
-- Table structure for table `usuariodatos`
--

DROP TABLE IF EXISTS usuariodatos;
CREATE TABLE usuariodatos (
  UsuarioID int NOT NULL,
  UsuarioNombre varchar(100) DEFAULT NULL,
  UsuarioApellido varchar(100) DEFAULT NULL,
  UsuarioCUIL int DEFAULT NULL,
  UsuarioFechaNac date DEFAULT NULL,
  UsuarioSexoDNI varchar(45) DEFAULT NULL,
  PRIMARY KEY (UsuarioID),
  CONSTRAINT UsuarioIDDatos FOREIGN KEY (UsuarioID) REFERENCES usuario (UsuarioID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `usuariodomicilio`
--

DROP TABLE IF EXISTS usuariodomicilio;
CREATE TABLE usuariodomicilio (
  UsuarioID int NOT NULL,
  UsuarioNacionalidad varchar(100) DEFAULT NULL,
  UsuarioProvincia varchar(100) DEFAULT NULL,
  UsuarioDepartamento varchar(100) DEFAULT NULL,
  UsuarioLocalidad varchar(100) DEFAULT NULL,
  UsuarioCiudad varchar(100) DEFAULT NULL,
  UsuarioBarrio varchar(150) DEFAULT NULL,
  UsuarioCalle varchar(100) DEFAULT NULL,
  UsuarioAltura varchar(100) DEFAULT NULL,
  UsuarioPiso varchar(100) DEFAULT NULL,
  UsuarioNumDep varchar(100) DEFAULT NULL,
  UsuarioManzana varchar(100) DEFAULT NULL,
  UsuarioCP int DEFAULT NULL,
  PRIMARY KEY (UsuarioID),
  CONSTRAINT UsuarioIDDomicilio FOREIGN KEY (UsuarioID) REFERENCES usuario (UsuarioID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `perfil`
--

DROP TABLE IF EXISTS perfil;
CREATE TABLE perfil (
  PerfilID int NOT NULL AUTO_INCREMENT,
  Perfil varchar(45) NOT NULL,
  PRIMARY KEY (PerfilID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `usuarioperfil`
--

DROP TABLE IF EXISTS usuarioperfil;
CREATE TABLE usuarioperfil (
  UsuarioPerfilID int NOT NULL AUTO_INCREMENT,
  UsuarioID int NOT NULL,
  PerfilID int NOT NULL,
  UsuarioPerfilActivo tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (UsuarioPerfilID),
  KEY UsuarioPerfilUsuarioID_idx (UsuarioID),
  KEY UsuarioPerfilPerfilID_idx (PerfilID),
  CONSTRAINT UsuarioPerfilPerfilID FOREIGN KEY (PerfilID) REFERENCES perfil (PerfilID),
  CONSTRAINT UsuarioPerfilUsuarioID FOREIGN KEY (UsuarioID) REFERENCES usuario (UsuarioID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
DELIMITER ;;
/*!50003 CREATE*/ /*!50003 TRIGGER PerfilInsertUsuario AFTER INSERT ON usuarioperfil FOR EACH ROW BEGIN
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 7) THEN 
	  INSERT INTO alumno(UsuarioPerfilID) VALUES(new.usuarioperfilid);
	end if;
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 2) THEN 
	  INSERT INTO personal(UsuarioPerfilID) VALUES(new.UsuarioPerfilID);
	end if;
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 3) THEN 
	  INSERT INTO personal(UsuarioPerfilID) VALUES(new.UsuarioPerfilID);
	end if;
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 4) THEN 
	  INSERT INTO personal(UsuarioPerfilID) VALUES(new.UsuarioPerfilID);
	end if;
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 5) THEN 
	  INSERT INTO personal(UsuarioPerfilID) VALUES(new.UsuarioPerfilID);
	end if;
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 6) THEN 
	  INSERT INTO personal(UsuarioPerfilID) VALUES(new.UsuarioPerfilID);
	end if;
	IF ((SELECT perfilID FROM usuarioperfil WHERE usuarioperfilid = new.usuarioperfilid) = 8) THEN 
	  INSERT INTO personal(UsuarioPerfilID) VALUES(new.UsuarioPerfilID);
	end if;
END */;;
DELIMITER ;


--
-- Table structure for table `alumno`
--

DROP TABLE IF EXISTS alumno;
CREATE TABLE alumno (
  AlumnoID int NOT NULL AUTO_INCREMENT,
  UsuarioPerfilID int NOT NULL,
  PRIMARY KEY (AlumnoID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `alumnocarpo`
--

DROP TABLE IF EXISTS alumnocarpo;
CREATE TABLE alumnocarpo (
  AlumnoCarpoID int NOT NULL AUTO_INCREMENT,
  CarpoID int NOT NULL,
  AlumnoID int NOT NULL,
  AlumnoCarpoActivo tinyint DEFAULT '0',
  PRIMARY KEY (AlumnoCarpoID),
  KEY fk_carpo_has_Alumno_Alumno1_idx (AlumnoID),
  KEY fk_carpo_has_Alumno_carpo1_idx (CarpoID),
  CONSTRAINT fk_carpo_has_Alumno_Alumno1 FOREIGN KEY (AlumnoID) REFERENCES alumno (AlumnoID),
  CONSTRAINT fk_carpo_has_Alumno_carpo1 FOREIGN KEY (CarpoID) REFERENCES carpo (CARPOID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `alumnocarpomateria`
--

DROP TABLE IF EXISTS alumnocarpomateria;
CREATE TABLE alumnocarpomateria (
  AlumnoCarpoMateriaID int NOT NULL AUTO_INCREMENT,
  AlumnoCarpoID int NOT NULL,
  MateriaID int NOT NULL,
  PRIMARY KEY (AlumnoCarpoMateriaID),
  KEY AlumnoCarpoID_idx (AlumnoCarpoID),
  KEY AlumnoCarpoMateriaID_idx (MateriaID),
  CONSTRAINT AlumnoCarpoID FOREIGN KEY (AlumnoCarpoID) REFERENCES alumnocarpo (AlumnoCarpoID),
  CONSTRAINT AlumnoCarpoMateriaID FOREIGN KEY (MateriaID) REFERENCES materia (MateriaID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `alumnodatos`
--

DROP TABLE IF EXISTS alumnodatos;
CREATE TABLE alumnodatos (
  AlumnoDatosID int NOT NULL,
  PRIMARY KEY (AlumnoDatosID),
  CONSTRAINT AlumnoID FOREIGN KEY (AlumnoDatosID) REFERENCES alumno (AlumnoID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `personal`
--

DROP TABLE IF EXISTS personal;
CREATE TABLE personal (
  PersonalID int NOT NULL AUTO_INCREMENT,
  UsuarioPerfilID int NOT NULL,
  PRIMARY KEY (PersonalID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `personalcarpo`
--

DROP TABLE IF EXISTS personalcarpo;
CREATE TABLE personalcarpo (
  PersonalCarpoID int NOT NULL AUTO_INCREMENT,
  PersonalID int NOT NULL,
  CarpoID int NOT NULL,
  PersonalCarpoActivo tinyint DEFAULT NULL,
  PRIMARY KEY (PersonalCarpoID),
  KEY fk_Personal_has_carpo_carpo1_idx (CarpoID),
  KEY fk_Personal_has_carpo_Personal1_idx (PersonalID),
  CONSTRAINT fk_Personal_has_carpo_carpo1 FOREIGN KEY (CarpoID) REFERENCES carpo (CARPOID),
  CONSTRAINT fk_Personal_has_carpo_Personal1 FOREIGN KEY (PersonalID) REFERENCES personal (PersonalID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `personalcarpomateria`
--

DROP TABLE IF EXISTS personalcarpomateria;
CREATE TABLE personalcarpomateria (
  PersonalCarpoMateriaID int NOT NULL AUTO_INCREMENT,
  PersonalCarpoID int NOT NULL,
  MateriaID int NOT NULL,
  PRIMARY KEY (PersonalCarpoMateriaID),
  KEY fk_PersonalCarpo_has_materia_materia1_idx (MateriaID),
  KEY PersonalCarpoID_idx (PersonalCarpoID),
  CONSTRAINT MateriaID FOREIGN KEY (MateriaID) REFERENCES materia (MateriaID),
  CONSTRAINT PersonalCarpoID FOREIGN KEY (PersonalCarpoID) REFERENCES personalcarpo (PersonalCarpoID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `personaldatos`
--

DROP TABLE IF EXISTS personaldatos;
CREATE TABLE personaldatos (
  PersonalID int NOT NULL,
  PRIMARY KEY (PersonalID),
  CONSTRAINT PersonalID FOREIGN KEY (PersonalID) REFERENCES personal (PersonalID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
