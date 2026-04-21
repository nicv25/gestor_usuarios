-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-04-2026 a las 08:35:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestor_usuarios`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas`
--

CREATE TABLE `areas` (
  `id_area` int(11) NOT NULL,
  `Nombre_A` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `areas`
--

INSERT INTO `areas` (`id_area`, `Nombre_A`) VALUES
(2, 'Administracion'),
(3, 'Contabilidad'),
(4, 'Gerencia'),
(5, 'Marketing'),
(1, 'Recursos Humanos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_Empleado` int(11) NOT NULL,
  `documento_Emple` varchar(50) NOT NULL,
  `nombre_Emple` varchar(50) NOT NULL,
  `apellido_Emple` varchar(50) NOT NULL,
  `cargo` varchar(50) NOT NULL,
  `Salario_B` decimal(10,2) NOT NULL,
  `Horas_Extras` int(11) NOT NULL,
  `bonificacion` decimal(10,2) NOT NULL,
  `salud` decimal(10,2) NOT NULL,
  `pension` decimal(10,2) NOT NULL,
  `salario_Neto` decimal(10,2) DEFAULT NULL,
  `id_area` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_Empleado`, `documento_Emple`, `nombre_Emple`, `apellido_Emple`, `cargo`, `Salario_B`, `Horas_Extras`, `bonificacion`, `salud`, `pension`, `salario_Neto`, `id_area`) VALUES
(1, '1013115936', 'Nicolas', 'Vargas', 'gerente', 2500000.00, 8, 300000.00, 100000.00, 100000.00, 2600000.00, 3),
(2, '1127472002', 'Michael', 'Vargas', 'Contador', 3200000.00, 5, 500000.00, 128000.00, 128000.00, 3444000.00, 1),
(3, '1010', 'Samuel', 'Sanchez', 'Administrador', 2800000.00, 10, 400000.00, 112000.00, 112000.00, 2976000.00, 2),
(10, '3030', 'prueba', 'vargas', 'Otro', 1800000.00, 15, 150000.00, 72000.00, 72000.00, 1946625.00, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `documento_Emple` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `password`, `rol`, `documento_Emple`) VALUES
(1, 'nicolas.vargas', 'Minolas2007', 'administrador', '1013115936'),
(2, 'michael.vargas', '123456', 'empleado', '1127472002'),
(5, 'samuel.sanchez', '4135', 'Administrador', '1010');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`id_area`),
  ADD UNIQUE KEY `uq_nombre_area` (`Nombre_A`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_Empleado`),
  ADD UNIQUE KEY `documento_Emple` (`documento_Emple`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `documento_Emple` (`documento_Emple`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `areas`
--
ALTER TABLE `areas`
  MODIFY `id_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_Empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `areas` (`id_area`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`documento_Emple`) REFERENCES `empleados` (`documento_Emple`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
