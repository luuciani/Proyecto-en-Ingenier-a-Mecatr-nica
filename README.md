# Diseño y Fabricación de Máquina Inyectora de Plástico

## Descripción
Este proyecto consiste en el diseño, fabricación e implementación de una máquina inyectora de plástico a escala, orientada a la reutilización de residuos plásticos generados en Atómica Láser.

El sistema permite transformar material termoplástico (polipropileno) en nuevas piezas mediante un proceso controlado de calentamiento, inyección y enfriamiento, integrando componentes mecánicos, electrónicos y de software.

## Objetivo
Desarrollar una solución mecatrónica funcional que permita:
- Reducir desperdicios plásticos
- Reutilizar material

El proyecto fue concebido no solo a nivel teórico, sino también como una implementación física completamente operativa.

## Características principales

- Sistema de inyección accionado por motor paso a paso
- Calentamiento por resistencia eléctrica
- Control de temperatura mediante termocupla tipo K
- Sistema de apertura y cierre de molde motorizado
- Interfaz de usuario con pantalla táctil
- Control central basado en Raspberry Pi

## Conceptos aplicados
- Moldeo por inyección de plásticos
- Control de motores paso a paso
- Sistemas de control térmico
- Integración mecatrónica (hardware + software)
- Automatización de procesos industriales

## Funcionamiento
El proceso de inyección se compone de las siguientes etapas:

1. Alimentación del material (pellets de plástico)
2. Calentamiento hasta estado viscoso (160–175 °C)
3. Inyección del material dentro del molde
4. Enfriamiento y solidificación
5. Apertura del molde y expulsión de la pieza

## Componentes principales

### Mecánicos
- Horno de calentamiento e inyección
- Sistema de transmisión por poleas
- Estructura de acero y aluminio
- Molde de inyección

### Electrónicos
- Raspberry Pi (control central)
- Drivers TB6600
- Motores paso a paso NEMA 23
- Termocupla tipo K + módulo MAX6675
- Pantalla táctil
- Sensores de final de carrera

### Térmicos
- Resistencias tipo banda

## Funcionamiento del sistema de control

- Control de motores mediante señales STEP/DIR
- Control de temperatura 
- Interfaz gráfica para operación y configuración
- Supervisión en tiempo real de variables del proceso

## Resultados

El sistema fue construido y probado con éxito, logrando:
- Correcta plastificación del material
- Inyección efectiva en molde
- Obtención de piezas funcionales
- Funcionamiento estable del sistema

## Documentación
El proyecto completo incluye:
- Diseño 3D
- Planos de conexión
- Cálculos de dimensionamiento
- Proceso de fabricación y ensamblaje

## Autora
Canela Lucía Ciani Fungueiriño  
Proyecto de Ingeniería Mecatrónica  
Universidad Nacional de Lomas de Zamora
