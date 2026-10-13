#!/usr/bin/env python3
"""
speech_one.py
=============
Nodo puente ROS2 para el sistema de voz del robot RoboCup @Home.

Suscripción:
    /command  (std_msgs/String)  — dict serializado desde voice_node
                                   ej: "{'object': 'coke', 'location': 'kitchen'}"

Publicaciones:
    /target_object  (std_msgs/String)  — nombre del objeto para Object Recognition
    /nav_location   (std_msgs/String)  — nombre del lugar  para Navigation

Comportamiento:
    • Parsea el dict con ast.literal_eval (seguro, sin eval() puro).
    • Valida que existan las claves 'object' y 'location'.
    • Publica cada dato en su tópico correspondiente.
    • Imprime en terminal un log detallado por cada comando recibido.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import ast


class SpeechOneNode(Node):

    def __init__(self):
        super().__init__('speech_one')

        # -------------------------------------------------------
        # Suscriptor — recibe el comando completo de voice_node
        # -------------------------------------------------------
        self.create_subscription(
            String,
            '/command',
            self.command_callback,
            10
        )

        # -------------------------------------------------------
        # Publicador → sistema de Object Recognition
        # -------------------------------------------------------
        self.object_pub = self.create_publisher(
            String,
            '/target_object',
            10
        )

        # -------------------------------------------------------
        # Publicador → sistema de Navegación
        # -------------------------------------------------------
        self.location_pub = self.create_publisher(
            String,
            '/nav_location',
            10
        )

        self.get_logger().info("=" * 50)
        self.get_logger().info("  speech_one LISTO")
        self.get_logger().info("  Suscrito  : /command")
        self.get_logger().info("  Publica   : /target_object  | /nav_location")
        self.get_logger().info("=" * 50)

    # ===========================================================
    # CALLBACK PRINCIPAL
    # ===========================================================
    def command_callback(self, msg: String):

        raw = msg.data.strip()
        self.get_logger().info(f"[speech_one] Comando recibido → {raw}")

        # --- Parseo seguro del dict serializado ---
        try:
            command = ast.literal_eval(raw)
        except (ValueError, SyntaxError) as e:
            self.get_logger().error(
                f"[speech_one] ❌ No se pudo parsear el comando: '{raw}' | Error: {e}"
            )
            return

        if not isinstance(command, dict):
            self.get_logger().error(
                f"[speech_one] ❌ Se esperaba un dict, se obtuvo: {type(command).__name__}"
            )
            return

        # --- Extracción de campos ---
        obj = command.get('object', '').strip()
        loc = command.get('location', '').strip()

        if not obj:
            self.get_logger().warn("[speech_one] ⚠️  Campo 'object' vacío o ausente.")
        if not loc:
            self.get_logger().warn("[speech_one] ⚠️  Campo 'location' vacío o ausente.")

        if not obj and not loc:
            self.get_logger().error("[speech_one] ❌ Ambos campos vacíos, ignorando comando.")
            return

        # --- Publicación ---
        if obj:
            self.object_pub.publish(String(data=obj))
            self.get_logger().info(
                f"[speech_one] 📦 /target_object  → '{obj}'"
            )

        if loc:
            self.location_pub.publish(String(data=loc))
            self.get_logger().info(
                f"[speech_one] 🗺️  /nav_location   → '{loc}'"
            )

        # --- Confirmación final en terminal ---
        self.get_logger().info(
            f"[speech_one] ✅ Despachado: OBJETO='{obj}'  LUGAR='{loc}'"
        )
        print(
            f"\n{'─'*50}\n"
            f"  [speech_one]  NUEVO COMANDO\n"
            f"  Objeto   → {obj}\n"
            f"  Lugar    → {loc}\n"
            f"{'─'*50}\n"
        )


# ===========================================================
# MAIN
# ===========================================================
def main(args=None):

    rclpy.init(args=args)

    node = SpeechOneNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
