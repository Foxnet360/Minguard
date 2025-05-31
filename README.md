# Minguard
MindGuard: Herramienta de Análisis de Burnout (MBI-HSS y K-Means) MindGuard es una aplicación web interactiva y de código abierto diseñada para facilitar el análisis del Maslach Burnout Inventory (MBI), específicamente la versión para Servicios Humanos (MBI-HSS), y la identificación de perfiles de burnout mediante técnicas de clustering K-Means. Su principal objetivo es proporcionar a investigadores, profesionales de Recursos Humanos, psicólogos organizacionales y consultores una herramienta accesible y rápida para procesar y visualizar datos de burnout, promoviendo la toma de decisiones informadas para el bienestar laboral.  
La característica más destacada de MindGuard es su enfoque en la privacidad: todo el procesamiento de datos se realiza localmente en el navegador del usuario. Los archivos CSV y los datos sensibles nunca se suben a ningún servidor.  

✨ Características Principales Carga de Datos Simplificada: 
* Permite subir archivos en formato CSV con las respuestas del MBI-HSS.
* Cálculo Automático de Subescalas: Calcula automáticamente las puntuaciones para las tres dimensiones del MBI-HSS:  Agotamiento Emocional (AE)  Despersonalización (DP)  Realización Personal (RP)  Interpretación de Niveles de Burnout: Clasifica las puntuaciones de cada subescala en niveles (Bajo, Moderado, Alto) basados en puntos de corte estandarizados.  Visualización Detallada de Resultados MBI:  Tabla detallada con las puntuaciones y niveles de burnout para cada participante.  Funcionalidad de filtrado y ordenamiento en la tabla de resultados.
* Gráficos interactivos que muestran los promedios de las subescalas y la distribución de los niveles de burnout en la muestra.
* Análisis de Clustering K-Means:  Permite al usuario especificar el número de clústeres (K) a identificar.
* Agrupa a los individuos en perfiles de burnout basados en sus puntuaciones MBI estandarizadas.
* Visualización de Perfiles de Clústeres:  Tabla resumen con las características de cada clúster (Nº de individuos, puntuaciones medias de AE, DP, RP, perfil tentativo e interpretación).
* Gráfico de pastel/torta para visualizar la distribución de individuos por clúster.  Gráfico Radar para comparar visualmente los perfiles medios de burnout de cada clúster.
* Exportación de Informes: Genera un informe completo en formato PDF con los resultados del análisis MBI y del clustering.
* Procesamiento 100% Local: Garantiza la privacidad y seguridad de los datos, ya que ningún dato del archivo CSV se envía a servidores externos.
* Interfaz Intuitiva: Diseño amigable y fácil de navegar, con secciones informativas claras.  Guías Detalladas:  Instrucciones sobre cómo preparar el archivo CSV, incluyendo una guía para recolectar datos con Google Forms.
* Explicaciones sobre la metodología (MBI-HSS, K-Means, interpretación de niveles).
* Glosario de términos y sección de preguntas frecuentes (FAQ).
* Información Legal y de Equipo: Incluye secciones sobre política de privacidad, términos de uso, y presentación del equipo (ejemplo).

🛠️ Tecnologías Utilizadas
* HTML5: Para la estructura de la aplicación.
* Tailwind CSS: Para el diseño y la interfaz de usuario responsiva y moderna.
* JavaScript (Vanilla JS): Para toda la lógica de la aplicación, cálculos, manipulación del DOM y interactividad.
* PapaParse.js: Para el parseo eficiente de archivos CSV en el navegador.
* Chart.js: Para la creación de gráficos dinámicos e interactivos.
* html2pdf.js: Para la generación de informes en formato PDF.

🚀 Cómo Empezar Prepara tus Datos:  
* Recolecta las respuestas del MBI-HSS.
* Organiza los datos en un archivo CSV.
* La primera columna debe ser un ID de participante, seguida por las 22 respuestas a los ítems del MBI-HSS en orden.
* Consulta la sección "Guía" dentro de la aplicación para ver el formato detallado y recomendaciones (incluyendo el uso de Google Forms para la recolección).
* Accede a la Aplicación:  Clona este repositorio: git clone https://github.com/tu-usuario/mindguard.git
* Navega al directorio del proyecto: cd mindguard  Abre el archivo index.html (o el nombre que tenga tu archivo principal HTML) en un navegador web moderno (Chrome, Firefox, Edge, Safari).
* Alternativamente, si la aplicación está desplegada, accede a la URL correspondiente.
* Usa la Herramienta:  Navega a la sección "Herramienta".
* Haz clic en "Selecciona tu archivo CSV" y carga tu archivo.
* Presiona "Procesar Archivo CSV".
* Analiza los resultados del MBI (tablas y gráficos).
* Si deseas, ajusta el número de clústeres (K) y presiona "Realizar Clustering".
* Interpreta los perfiles de clústeres generados.
* Descarga el informe completo en PDF usando el botón "Descargar Informe PDF".

🔒 Privacidad y Seguridad MindGuard prioriza la privacidad de tus datos. 
* Todo el procesamiento de archivos CSV y los cálculos se realizan exclusivamente en tu navegador.
* Ningún dato sensible de tus participantes es enviado o almacenado en servidores externos.

📄 Contenido Informativo La aplicación incluye secciones detalladas sobre:  
* Metodología: Explicaciones sobre el MBI-HSS, la interpretación de los niveles de burnout, el funcionamiento del clustering K-Means y su valor agregado, y la seguridad de la información.
* Guía de Usuario: Instrucciones paso a paso para la preparación de datos (incluyendo Google Forms), uso de la herramienta, solución de problemas (FAQ) y un glosario extenso.
* Aspectos Legales: Política de privacidad, términos de servicio, política de cookies y un descargo de responsabilidad importante.

🤝 Contribuciones Las contribuciones son bienvenidas. Si deseas colaborar, por favor considera:  Reportar bugs o issues.  
* Sugerir nuevas características o mejoras.
* Realizar Pull Requests con mejoras al código o la documentación.  (Por favor, sigue las guías de contribución del proyecto si existen).

🖼️ Screenshots 

![ss1](https://github.com/user-attachments/assets/88239709-409a-42e6-9796-22e7b4d30b7d)
![ss2](https://github.com/user-attachments/assets/00ed1228-54ac-4e8a-b69f-50208621133e)
![ss3](https://github.com/user-attachments/assets/c0515113-74bb-43fa-af74-52451f9beac1)

Esperamos que MindGuard sea una herramienta valiosa para tu trabajo e investigación sobre el burnout.
