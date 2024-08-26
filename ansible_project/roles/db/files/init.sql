CREATE DATABASE IF NOT EXISTS hospitaldb;
USE hospitaldb;


CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    doctor_name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Hos_data (
    HospitalID INT(4) NULL AUTO_INCREMENT PRIMARY KEY,
    HospitalName CHAR(40) NULL,
    Address VARCHAR(10) NULL,
    TotalHospitalBeds INT(3) NULL,
    UsingHospitalBeds CHAR(3) NULL,
    ICD CHAR(50) NULL
);

CREATE TABLE IF NOT EXISTS user (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    hospital VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS MedData (
    PatientID INT(11) NOT NULL AUTO_INCREMENT,
    Name VARCHAR(100) NULL,
    BirthDate DATE NULL,
    BloodType VARCHAR(4) NULL,
    ICD VARCHAR(10) NULL,
    PRIMARY KEY (PatientID)
);


INSERT INTO Hos_data (HospitalName, Address, TotalHospitalBeds, UsingHospitalBeds, ICD) VALUES
('BlueSkyHospital', '02', 20, '2', 'A00,E11.9,J45.0,N40,R51'),
('MyeongjiClinic', '02', 18, '15', 'B20,F32.1,G43.9,I10,L40.0'),
('OnnuriMedicalCenter', '02', 25, '2', 'C34.1,D50.9,H10.9,M54.5,O80'),
('NewBeginningHospital', '02', 18, '2', 'I25.1,J20.9,K35.8,M25.50,N80.0'),
('CentralHealthClinic', '031', 28, '22', 'Q21.1,R42,S52.5,T14.9,Z01.9'),
('ForestofHopeHospital', '031', 47, '31', 'A03.0,F41.1,G47.0,I63.9,L03.9'),
('GaramGeneralHospital', '031', 35, '31', 'B07,E78.5,J44.9,K21.0,M79.1'),
('NextGenerationHospital', '02', 19, '2', 'C50.9,D73.9,H52.4,I20.0,L29.8'),
('FutureMedicalCenter', '02', 16, '2', 'A02.1,F32.2,G20,I63.5,L40.1'),
('HopeMedicalCenter', '02', 27, '21', 'B18.2,F33.0,G43.1,I10,M06.9'),
('SejongMedical', '033', 30, '26', 'C18.9,D50.0,H90.3,J40,L02.9'),
('PeaceandHealthHospital', '02', 23, '2', 'A04.7,F42.0,G46.1,I70.0,L60.9'),
('BeautifulLifeClinic', '02', 16, '14', 'B15,F31.9,G37.0,I25.0,L29.9'),
('GardenHospital', '031', 28, '11', 'C21.9,D61.9,H02.4,J30.4,M54.4'),
('SunshineMedicalCenter', '031', 24, '11', 'A03.1,F40.9,G45.9,I11.9,L99'),
('GraceHospital', '031', 20, '11', 'B05,F43.9,G40.8,I64,L21'),
('SeogwangGeneralHospital', '031', 18, '14', 'C07,D72.9,H10.1,J42,M51.0'),
('HealthyFutureClinic', '033', 26, '12', 'A08.0,F44.9,G71.0,I20.9,L03.0'),
('TrueLoveHospital', '033', 35, '21', 'B09,F50.9,G56.0,I10,M79.7'),
('HopeMedicalCenter', '033', 27, '12', 'C09,D73.8,H01.9,J44.0,N84.0');

INSERT INTO MedData (Name, BirthDate, BloodType, ICD) VALUES
('John Doe', '1980-05-15', 'A+', 'A00'),
('Jane Smith', '1992-11-30', 'B-', 'F32.1'),
('Michael Brown', '1975-07-20', 'O+', 'G43.9'),
('Emily Davis', '2000-03-10', 'AB-', 'C34.1');

