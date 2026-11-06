# RoboCup @Home Voice 2026

Subsistema de voz y diálogo interactivo para robot de servicio en ROS 2 Jazzy (Ubuntu 24.04). Conecta reconocimiento de voz fuera de línea (**Vosk ASR**), una máquina de estados de diálogo HRI guiada por la iniciativa del robot (**Voice Node**), procesamiento de lenguaje natural con spaCy (**speech_one**), síntesis de voz (**Piper TTS**) y un puente de integración hacia navegación y visión por computador mediante tópicos de ROS 2.

---

## 🚀 Mejoras e Innovaciones Implementadas (HRI & NLU)

### 1. Esquema de Diálogo Guiado por el Robot (Robot-Initiated HRI)
* **Iniciativa Autónoma al Arrancar:** El robot toma el control proactivo de la interacción emitiendo su presentación e instrucciones de uso al posicionarse en la arena: *"Hello, my name is Havva. I am here to serve you. Please say my name at the beginning of each instruction and wait for my response. What can I bring you and from where?"*
* **Bucle de Preguntas de Aclaración (Slot Filling):** Si el comando del usuario es incompleto, la máquina de estados retiene la información capturada en memoria persistente (`current_object` y `current_location`) y solicita activamente el dato faltante:
  * Si solo detecta el objeto: *"Where should I get the [OBJETO] from?"*
  * Si solo detecta la ubicación: *"What item should I bring from the [LUGAR]?"*
* **Formato Estricto de Repetición y Confirmación:** Una vez completados ambos campos y validados por voz (`yes`, `confirm`, etc.), el robot sintetiza la instrucción usando el formato exacto exigido por la prueba: `"Bring [OBJETO] from [LUGAR]."`

### 2. Extracción de Entidades con spaCy (NLU)
* **Desacoplamiento NLU:** El nodo `speech_one` analiza las oraciones con el modelo `en_core_web_sm` de spaCy para la extracción dinámica de las entidades `/target_object` y `/nav_location`.
* **Normalización de Aliases:** Mapeo automático de variaciones fonéticas (`coke` $\leftarrow$ `cake`, `cok`) y palabras clave de activación (`havva`, `hava`, `ava`, `java`, `robot`).

### 3. Sincronización ASR/TTS y Control de Audio
* **Control Mute Inteligente (ASR OFF):** Desactivación automática del micrófono/reconocedor Vosk mientras el robot habla a través de Piper TTS para evitar retroalimentación, ecos o auto-escucha.
* **Gestión Dinámica de Modos:** Cambio inteligente entre estados de reconocimiento (`command`, `confirmation`, `off`) y filtrado de ruido.

---

## 📋 Requisitos previos

Tus compañeras deben contar con:
1. **Ubuntu 24.04 LTS**.
2. **ROS 2 Jazzy** instalado y configurado en `/opt/ros/jazzy`.
3. Micrófono y bocina/altavoces (o audífonos) reconocidos por el sistema de audio.

---

## 🛠️ Guía de instalación rápida

Sigue estos pasos en la terminal desde la raíz del repositorio clonado:

### 1. Clonar el repositorio y entrar a la carpeta
```bash
git clone [https://github.com/Raphinha1/robocup-at-home-voice-2026.git](https://github.com/Raphinha1/robocup-at-home-voice-2026.git)
cd robocup-at-home-voice-2026

2. Instalar herramientas de compilación y dependencias del sistema
Bash

sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-pip \
  python3-venv \
  python3-rosdep \
  portaudio19-dev \
  libasound2-plugins

  3. Crear y activar el entorno virtual de Python

Para evitar conflictos con los paquetes del sistema en Ubuntu 24.04 (PEP 668), se recomienda usar un entorno virtual con --system-site-packages (para que tenga acceso a las bibliotecas de ROS 2):
Bash

python3 -m venv --system-site-packages .venv
source .venv/bin/activate

Instalar las dependencias de Python requeridas (incluyendo spaCy y su modelo en inglés):
Bash

pip install -r requirements-dev.txt
python3 -m spacy download en_core_web_sm

4. Resolver dependencias de ROS y compilar

Inicializa rosdep (si no lo has hecho antes) y compila el workspace con colcon:
Bash

source /opt/ros/jazzy/setup.bash
# Solo si nunca has inicializado rosdep en tu máquina:
# sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y

# Compilar desde la raíz del workspace (NUNCA dentro de src/)
colcon build --base-paths src --symlink-install

    [!WARNING]
    Ejecuta siempre colcon build desde la raíz del repositorio, nunca dentro de src/.

🗣️ Modelos de Voz (ASR y TTS)
1. Reconocimiento de voz (Vosk ASR)

El modelo ligero en inglés vosk-model-small-en-us-0.15 viene incluido en el paquete robocup_asr dentro de src/robocup_asr/vosk_models/. No necesitas descargar nada adicional para reconocimiento de voz.
2. Síntesis de voz (Piper TTS)

Por cuestiones de licencias y tamaño, los pesos del modelo de Piper no se distribuyen en el repositorio. Necesitas un modelo .onnx y su archivo descriptor .onnx.json correspondiente:

    Puedes descargar una voz compatible en español o inglés desde el repositorio oficial de voces de Piper (por ejemplo es_ES-sharvard-medium o en_US-lessac-medium).

    Guarda el archivo .onnx y su .onnx.json en una ruta conocida, por ejemplo:src/robocup_tts/piper-models/en_US-lessac-medium.onnx
    y src/robocup_tts/piper-models/en_US-lessac-medium.onnx.json.

🚀 Cómo ejecutar el sistema
Opción A: Modo completo (Voz + Diálogo + Puente con audio real)

Requiere micrófono, bocinas y la ruta al modelo de voz Piper:
Bash

source /opt/ros/jazzy/setup.bash
source .venv/bin/activate
source install/setup.bash

ros2 launch robocup_bringup robot_launch.py audio:=true

    Consejo (Alias de ejecución rápida): Puedes agregar un alias a tu ~/.bashrc para iniciar todo con la orden run_havva:
    Bash

    alias run_havva="cd ~/robocup-at-home-voice-2026/robocup-at-home-voice-2026 && source /opt/ros/jazzy/setup.bash && source .venv/bin/activate && source install/setup.bash && ros2 launch robocup_bringup robot_launch.py audio:=true"

Opción B: Modo solo texto (sin micrófono ni bocina, para pruebas de lógica y ROS 2)

Ideal para verificar la máquina de estados y tópicos sin requerir hardware de audio ni el modelo Piper:
Bash

source /opt/ros/jazzy/setup.bash
source .venv/bin/activate
source install/setup.bash

ros2 launch robocup_bringup robot_launch.py audio:=false

Para interactuar en este modo, abre otra terminal con el mismo entorno y publica texto simulando la voz:

    Despertar al robot (Wake word):
    Bash

    ros2 topic pub --once /speech_text std_msgs/msg/String "{data: 'ava'}"

    Enviar la orden (Objeto y Ubicación):
    Bash

    ros2 topic pub --once /speech_text std_msgs/msg/String "{data: 'bring milk from bed'}"

    Confirmar la orden:
    Bash

    ros2 topic pub --once /speech_text std_msgs/msg/String "{data: 'yes'}"

    Verificar la salida en los tópicos de navegación y visión:
    Bash

    ros2 topic echo /command
    ros2 topic echo /target_object
    ros2 topic echo /nav_location

Opción C: Demo simulada rápida (Sin ROS ni hardware)

Para verificar la lógica de integración y el flujo completo en un solo comando:
Bash

python3 scripts/demo_simulated.py

🏗️ Arquitectura del Sistema
Fragmento de código

flowchart LR
    Mic["Micrófono<br/>(Entrada de audio)"] --> ASR["Vosk ASR<br/>(robocup_asr)"]
    Model["Modelo Vosk<br/>(Empaquetado)"] --> ASR
    ASR -->|/speech_text: String| Voice["Diálogo / Estados HRI<br/>(robocup_voice)"]
    Voice -->|/tts_text: String| TTS["Piper TTS<br/>(robocup_tts)"]
    Private["Modelo Piper ONNX<br/>(Local)"] -.-> TTS
    TTS --> Speaker["Altavoz / Bocina<br/>(Salida de audio)"]
    TTS -->|/asr_control: Bool| ASR
    Voice -->|/asr_mode y /asr_grammar: String| ASR
    Voice -->|/command: String| Bridge["Puente NLU spaCy<br/>(robocup_speech_one)"]
    Bridge -.->|/nav_location: String| Nav["Navegación / Nav2<br/>(Consumidor externo)"]
    Bridge -.->|/target_object: String| Object["Reconocimiento de objetos<br/>(Consumidor externo)"]

Paquetes incluidos en src/
Paquete	Ejecutable	Responsabilidad
robocup_asr	vosk_asr_node	Captura PCM a 16 kHz mono, filtro dinámico de energía, reconocimiento con Vosk y gramática activa.
robocup_tts	tts_node	Síntesis y reproducción de voz con Piper, control de pausa/reanudación del ASR para evitar eco.
robocup_voice	voice_node	Iniciativa HRI, preguntas de aclaración (slot filling), confirmación, rechazo y timeout.
robocup_speech_one	speech_one	Desempaqueta /command, analiza entidades con spaCy y despacha /target_object y /nav_location.
robocup_bringup	robot_launch.py	Orquestación de lanzamiento general (con argumento opcional audio:=false).
📡 Tópicos principales de ROS 2
Tópico	Tipo	Descripción
/speech_text	std_msgs/msg/String	Texto reconocido por Vosk o inyectado para pruebas.
/tts_text	std_msgs/msg/String	Texto que el sintetizador Piper debe reproducir.
/asr_control	std_msgs/msg/Bool	False cuando el robot está hablando (pausa ASR); True cuando termina.
/asr_mode	std_msgs/msg/String	Modo actual: command, confirmation u off.
/asr_grammar	std_msgs/msg/String	Lista JSON con el vocabulario activo enviado dinámicamente a Vosk.
/command	std_msgs/msg/String	Comando confirmado en formato diccionario: {'object': 'milk', 'location': 'bed'}.
/target_object	std_msgs/msg/String	Objeto destino extraído para el nodo de visión (ej. milk).
/nav_location	std_msgs/msg/String	Destino extraído para el nodo de navegación (ej. bed).
⚙️ Personalización de Objetos, Ubicaciones y Palabras de Activación

Puedes modificar los nombres de los objetos y ubicaciones válidos editando el archivo de configuración:
Bash

src/robocup_voice/config/competition_config.yaml

Valores por defecto:

    Wake words: havva, hava, ava, java.

    Objetos: coke, milk, noodle, yogurt.

    Ubicaciones: bed, table, shelf, counter, kitchen, living room, bedroom.

    Aliases: Variaciones fonéticas comunes (ej. cake o cok mapeados a coke).

Si modificas el archivo YAML, vuelve a compilar el paquete correspondiente:
Bash

colcon build --packages-select robocup_voice
source install/setup.bash

🧪 Pruebas y verificación

Para ejecutar la batería de pruebas automatizadas:
Bash

source /opt/ros/jazzy/setup.bash
source .venv/bin/activate
pytest tests/

Para probar el flujo de texto real sobre ROS 2 Jazzy y DDS sin periféricos de audio:
Bash

python3 scripts/verify_ros_flow.py

❓ Preguntas frecuentes y solución de problemas

    Error: FileNotFoundError: Piper voice weights are intentionally not bundled...

    Causa: Estás ejecutando en modo con audio sin haber especificado la ruta al modelo ONNX de Piper.

    Solución: Descarga una voz de Piper y pasa el argumento tts_model_path:=/ruta/a/tu/voz.onnx, o bien ejecuta con audio:=false si solo vas a probar la lógica de ROS.

    Error: ModuleNotFoundError: No module named 'piper' o vosk:

    Asegúrate de haber activado el entorno virtual (source .venv/bin/activate) donde instalaste requirements-dev.txt.

    Audio y micrófono en Linux:

    Verifica que tu micrófono y altavoz funcionen con:
    Bash

    python3 -c "import sounddevice as sd; print(sd.query_devices())"