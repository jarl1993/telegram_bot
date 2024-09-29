import requests
from bs4 import BeautifulSoup
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# Configura el logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables para almacenar la encuesta
votos = {
    "Ayala": 0,
    "Suma": 0,
    "CPO": 0,
    "Pirandello": 0,
}

# Conjunto para almacenar IDs de usuarios que han votado
usuarios_votantes = set()

# Variable para almacenar el último número conocido
ultimo_numero = None

# Función para obtener el número
def obtener_numero():
    # Retornamos un número fijo en lugar de obtenerlo de la web
    return "86"

# Comando para enviar el número por Telegram
def numero_command(update: Update, context: CallbackContext) -> None:
    numero = obtener_numero()
    if numero:
        update.message.reply_text(f"El próximo número a llamar es el: {numero}")
    else:
        update.message.reply_text("El número no ha sido obtenido aún.")

# Comando para enviar información de ayuda
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "¡Hola! Soy un bot que proporciona información sobre la oposición administrativo de la Universidad de Málaga.\n"
        "Aquí tienes algunos comandos que puedes usar:\n"
        "/numero - Obtén el número actual de la bolsa de trabajo.\n"
        "/archivo - Obtén el enlace al archivo de la bolsa de trabajo.\n"
        "/fecha - Información sobre las oposiciones.\n"
        "/correo - El correo de contacto con la UMA.\n"
        "/llamamiento - Información sobre llamamientos.\n"
        "/temario_teoria - Detalles del contenido de la parte teórica de la última oposición.\n"
        "/temario_informatica - Detalles del contenido de la parte informática de la última oposición.\n"
        "/personal - Información del Servicio de Personal de Administración y Servicios.\n"
        "/academias - Información sobre academias que preparan oposiciones.\n"
        "/encuesta - Realiza una encuesta sobre la mejor academia para teoría.\n"
        "/resultados - Muestra los resultados de la encuesta.\n"
        "/examen_teoria - Enlace al último examen teórico realizado.\n"
        "/examen_informatico - Enlace al último examen informático realizado.\n"
        "/help - Muestra este mensaje de ayuda."
    )
    update.message.reply_text(help_text)

# Comando para enviar el enlace al archivo PDF
def archivo_command(update: Update, context: CallbackContext) -> None:
    pdf_url = "https://www.uma.es/pas/navegador_de_ficheros/Bolsas_Trabajo/descargar/2024/20240606_OPC1ADM23_Bolsa.pdf"
    update.message.reply_text(f"Puedes consultar la lista de la bolsa aquí: {pdf_url}")

# Comando para enviar información sobre la fecha de oposiciones
def fecha_command(update: Update, context: CallbackContext) -> None:
    mensaje_fecha = (
        "Según CSIF, no habrá oposiciones en 2025, presumiblemente será entre 2026 y 2027."
    )
    update.message.reply_text(mensaje_fecha)

# Comando para enviar el correo de contacto
def correo_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("El correo de contacto con la UMA es: bolsaspas@uma.es")

# Comando para enviar información sobre llamamientos
def llamamiento_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Según CSIF, no habrá más llamamientos hasta 2025.")

# Comando para enviar el temario de la parte teórica
def temario_teoria_command(update: Update, context: CallbackContext) -> None:
    temario_teoria_texto = (
        "1. La Constitución Española de 1978: derechos y deberes fundamentales; las "
        "Cortes Generales; el Gobierno y la Administración; el Tribunal Constitucional; la reforma "
        "de la Constitución.\n"
        "2. Las fuentes del Derecho Administrativo y la jerarquía normativa. Leyes y disposiciones "
        "normativas: concepto, naturaleza, clases y límites.\n"
        "3. Planes de igualdad de la Universidad de Málaga: referencia normativa; ámbito de aplicación; "
        "diagnósticos de situación en igualdad de género; contenido mínimo de los planes de igualdad; "
        "vigencia, seguimiento y evaluación de los planes de igualdad; planes de igualdad en la UMA.\n"
        "4. El Reglamento 2/2023, de la Universidad de Málaga, sobre normas de convivencia universitaria.\n"
        "5. La Ley 39/2015, del Procedimiento Administrativo Común de las Administraciones Públicas: objeto y "
        "ámbito de aplicación; los interesados en el procedimiento; la actividad de las Administraciones públicas; "
        "los actos administrativos; el procedimiento administrativo; la revisión de los actos administrativos.\n"
        "6. La Ley 40/2015, de Régimen Jurídico del Sector Público: objeto, principios y ámbito de aplicación; "
        "órganos de las Administraciones públicas; funcionamiento electrónico del sector público.\n"
        "7. Los Estatutos de la Universidad de Málaga.\n"
        "8. La Ley Orgánica 2/2023, del Sistema Universitario: disposiciones generales; funciones del sistema "
        "universitario y autonomía de las Universidades; creación y reconocimiento de Universidades y calidad "
        "del sistema universitario; organización de las enseñanzas; investigación y transferencia e intercambio "
        "del conocimiento e innovación; cooperación, coordinación y participación en el sistema universitario; "
        "el estudiantado en el sistema universitario; régimen específico de las Universidades públicas.\n"
        "9. La Ley Andaluza de Universidades: disposiciones generales; la institución universitaria; la comunidad "
        "universitaria; la actividad universitaria; la calidad universitaria; régimen económico, financiero y "
        "patrimonial.\n"
        "10. Las enseñanzas universitarias en España: ordenación, estructura, sistema de calificaciones, "
        "verificación y acreditación de títulos.\n"
        "11. El acceso y la admisión a los estudios conducentes a títulos universitarios de carácter oficial y "
        "validez en todo el territorio nacional en la Universidad de Málaga.\n"
        "12. La matriculación de estudiantes para cursar enseñanzas correspondientes a estudios de Grado, Máster "
        "y Doctorado en la Universidad de Málaga.\n"
        "13. Los reconocimientos de estudios, experiencia laboral y profesional, y actividades universitarias, "
        "en estudios conducentes a títulos universitarios de carácter y validez en todo el territorio nacional "
        "en la Universidad de Málaga.\n"
        "14. El régimen jurídico del profesorado universitario: normativa estatal y autonómica.\n"
        "15. El Estatuto Básico del Empleado Público: objeto y ámbito de aplicación; personal al servicio de "
        "las Administraciones públicas; derechos y deberes: código de conducta de los empleados públicos; "
        "adquisición y pérdida de la relación de servicio; ordenación de la actividad profesional; situaciones "
        "administrativas; régimen disciplinario. Régimen de incompatibilidades del personal al servicio de las "
        "Administraciones públicas.\n"
        "16. El Plan de Ordenación de los Recursos Humanos del PAS de la Universidad de Málaga: Reglamento de "
        "provisión de puestos de trabajo del personal funcionario de administración y servicios; normas de "
        "aplicación y ejecución de la Relación de puestos de trabajo.\n"
        "17. La gestión económica de la Universidad de Málaga: estructura presupuestaria de ingresos y gastos. "
        "Reglamento de Régimen Económico-Financiero de la Universidad de Málaga."
    )
    update.message.reply_text(temario_teoria_texto)

# Comando para enviar el temario de la parte informática
def temario_informatica_command(update: Update, context: CallbackContext) -> None:
    temario_informatica_texto = (
        "1. Procesador de textos Word 2019: Nociones elementales. Formato de documentos. "
        "Plantillas de documentos. Estilos. Tablas. Importar documentos. Anotaciones y revisiones "
        "de documentos. Generación de documentos y correos personalizados. Imágenes, gráficos y "
        "SmartArt. Secciones. Organigramas y diagramas. Notas al pie. Seguridad. Gestión de referencias: "
        "índices. Formato y diseño de impresión.\n"
        "2. Hojas de cálculo Excel 2019: Gestión básica de libros y hojas de cálculo. Funciones. "
        "Gráficos. Tablas dinámicas. Seguridad. Exportación de datos. Gestión de referencias. "
        "Crear formularios.\n"
        "3. Correo electrónico. Correo electrónico Outlook 2019: Gestión básica de envío y recepción de mensajes; "
        "firma de mensajes. Seguridad de claves. Correo seguro. Tipos de listas de correo. Normativa de uso "
        "aceptable y seguridad básica del correo electrónico institucional de la Universidad de Málaga. Nociones "
        "elementales de los protocolos POP3, IMAP4 y SMTP para envío desde cliente («Submission»)."
    )
    update.message.reply_text(temario_informatica_texto)

# Comando para enviar información del personal
def personal_command(update: Update, context: CallbackContext) -> None:
    personal_info_texto = (
        "Horario de atención al público: de 09:00 a 14:00 horas, de lunes a viernes.\n\n"
        "Correo electrónico: serviciopas@uma.es\n\n"
        "Teléfonos: 952131058, 952137256\n\n"
        "Dirección Postal:\n\n"
        "Servicio de Personal de Administración y Servicios\n"
        "Universidad de Málaga\n"
        "Edificio de Servicios Múltiples\n"
        "Plaza de El Ejido s/n\n"
        "29071 - Málaga"
    )
    update.message.reply_text(personal_info_texto)

# Comando para enviar información sobre academias
def academias_command(update: Update, context: CallbackContext) -> None:
    academias_info_texto = (
        "1. **Ayala** - Lo da, por un lado, Fernando Moratalla (dos grupos, uno abierto) y por otro, dos funcionarios de Granada (un grupo abierto): "
        "[Academia Jesús Ayala](https://academiajesusayala.com/oposiciones/universidad-malaga-administrativos/)\n"
        "2. **Suma** - Lo da Angel Serrano (dos grupos abiertos): "
        "[Suma Preparadores](https://www.sumapreparadores.com/)\n"
        "3. **CPO** - Lo da Antonio Nuñez y dos profesores más (un grupo abierto): "
        "[CPO Nuñez](https://www.cponunez.com/universidad-de-malaga-administrativo/)\n"
        "4. **Pirandello** - Lo da Rosa Baeza (sin información de grupos abiertos): "
        "[Pirandello Formación](https://pirandelloformacion.com/oposiciones-administrativo-universidad-malaga-uma/)"
    )
    update.message.reply_text(academias_info_texto)

# Comando para enviar la encuesta
def encuesta_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Ayala", callback_data='Ayala'),
         InlineKeyboardButton("Suma", callback_data='Suma')],
        [InlineKeyboardButton("CPO", callback_data='CPO'),
         InlineKeyboardButton("Pirandello", callback_data='Pirandello')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Comprobar si el usuario ya ha votado
    if update.effective_user.id in usuarios_votantes:
        update.message.reply_text("Ya has votado en esta encuesta.")
    else:
        update.message.reply_text("¿Qué academia es mejor para teoría?\n"
                                   "1. Ayala\n"
                                   "2. Suma\n"
                                   "3. CPO\n"
                                   "4. Pirandello", reply_markup=reply_markup)

# Comando para mostrar resultados
def resultados_command(update: Update, context: CallbackContext) -> None:
    resultados_texto = (
        "Resultados de la encuesta:\n"
        f"Ayala: {votos['Ayala']}\n"
        f"Suma: {votos['Suma']}\n"
        f"CPO: {votos['CPO']}\n"
        f"Pirandello: {votos['Pirandello']}"
    )
    update.message.reply_text(resultados_texto)

# Comando para enviar el examen de teoría
def examen_teoria_command(update: Update, context: CallbackContext) -> None:
    examen_teoria_texto = (
        "El último examen teórico se realizó el 28 de octubre de 2023. Puedes acceder al examen aquí: "
        "https://www.uma.es/pas/navegador_de_ficheros/Procesos_Selectivos/descargar/2023/20230426_OPC1ADM23/20231030_OPC1ADM23_1Ej_Examen.pdf"
    )
    update.message.reply_text(examen_teoria_texto)

# Comando para enviar el examen informático
def examen_informatico_command(update: Update, context: CallbackContext) -> None:
    examen_informatico_texto = (
        "El último examen informático se realizó el 16 de diciembre de 2023. Puedes acceder al examen aquí: "
        "https://www.uma.es/pas/navegador_de_ficheros/Procesos_Selectivos/descargar/2023/20230426_OPC1ADM23/20231218_OPC1ADM23_2Ej_Examen.pdf"
    )
    update.message.reply_text(examen_informatico_texto)

# Manejar las respuestas de la encuesta
def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    # Incrementar el voto correspondiente
    academia_votada = query.data
    
    # Comprobar si el usuario ya ha votado
    if query.from_user.id in usuarios_votantes:
        query.edit_message_text(text=f"Ya has votado por: {academia_votada}\n\n"
                                      "Gracias por participar en la encuesta!\n"
                                      f"Resultados actuales:\n"
                                      f"Ayala: {votos['Ayala']}\n"
                                      f"Suma: {votos['Suma']}\n"
                                      f"CPO: {votos['CPO']}\n"
                                      f"Pirandello: {votos['Pirandello']}")
    else:
        # Registrar el voto
        votos[academia_votada] += 1
        usuarios_votantes.add(query.from_user.id)  # Añadir al conjunto de usuarios que han votado
        
        # Informar al usuario
        query.edit_message_text(text=f"Votaste por: {academia_votada}\n\n"
                                      "Gracias por participar en la encuesta!\n"
                                      f"Resultados actuales:\n"
                                      f"Ayala: {votos['Ayala']}\n"
                                      f"Suma: {votos['Suma']}\n"
                                      f"CPO: {votos['CPO']}\n"
                                      f"Pirandello: {votos['Pirandello']}")

# Función principal para ejecutar el bot
def main() -> None:
    # Sustituye aquí por tu token
    updater = Updater("7571408671:AAEjcf9eoZwVnThW9_sXqMW2og6N7qA12iU", use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("numero", numero_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("archivo", archivo_command))
    dispatcher.add_handler(CommandHandler("fecha", fecha_command))
    dispatcher.add_handler(CommandHandler("correo", correo_command))
    dispatcher.add_handler(CommandHandler("llamamiento", llamamiento_command))
    dispatcher.add_handler(CommandHandler("temario_teoria", temario_teoria_command))
    dispatcher.add_handler(CommandHandler("temario_informatica", temario_informatica_command))
    dispatcher.add_handler(CommandHandler("personal", personal_command))
    dispatcher.add_handler(CommandHandler("academias", academias_command))
    dispatcher.add_handler(CommandHandler("encuesta", encuesta_command))  # Comando para la encuesta
    dispatcher.add_handler(CommandHandler("resultados", resultados_command))  # Comando para mostrar resultados
    dispatcher.add_handler(CommandHandler("examen_teoria", examen_teoria_command))  # Comando para examen de teoría
    dispatcher.add_handler(CommandHandler("examen_informatico", examen_informatico_command))  # Comando para examen informático
    dispatcher.add_handler(CallbackQueryHandler(button_callback))  # Manejar las respuestas de la encuesta

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
