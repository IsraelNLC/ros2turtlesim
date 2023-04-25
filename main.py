#!/usr/bin/env python3

# Importa as bibliotecas necessárias
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import random

# Cria uma subclasse da classe Node para controlar a tartaruga
class TurtleController(Node):
    # Construtor da classe
    def __init__(self):
        # Chama o construtor da superclasse
        super().__init__('turtle_controller')
        # Cria um publicador para enviar mensagens Twist ao tópico 'turtle1/cmd_vel'
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        # Cria um timer para chamar o método move_turtle a cada 0.1 segundo
        self.timer_ = self.create_timer(0.1, self.move_turtle)
        # Cria um timer para chamar o método pen_color a cada 0.1 segundo
        self.timer_ = self.create_timer(0.1, self.pen_color)

        # Cria uma mensagem Twist para armazenar as velocidades linear e angular da tartaruga
        self.twist_msg_ = Twist()

    # Método para atualizar a mensagem Twist e publicá-la no tópico 'turtle1/cmd_vel'
    def move_turtle(self):
        # Define a velocidade angular da tartaruga com base no tempo atual
        self.twist_msg_.angular.z = 10 * self.get_clock().now().nanoseconds / 1e8
        # Define a velocidade linear da tartaruga como 7.0
        self.twist_msg_.linear.x = 7.0

        # Publica a mensagem Twist no tópico 'turtle1/cmd_vel'
        self.publisher_.publish(self.twist_msg_)

    # Método para alterar a cor da tartaruga com valores aleatórios
    def pen_color(self):
        # Cria um cliente para o serviço 'turtle1/set_pen'
        self.set_pen = self.create_client(SetPen, 'turtle1/set_pen')
        # Espera o serviço ficar disponível por até 1 segundo
        while not self.set_pen.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        # Define os valores RGB da cor como valores aleatórios entre 0 e 255
        request = SetPen.Request()
        request.r = random.randint(0, 255)
        request.g = random.randint(0, 255)
        request.b = random.randint(0, 255)
        request.width = 3
        request.off = 0
        # Faz uma chamada assíncrona ao serviço para alterar a cor da tartaruga
        future = self.set_pen.call_async(request)

# Função principal do programa
def main(args=None):
    # Inicializa o nó do ROS
    rclpy.init(args=args)
    # Cria uma instância da classe TurtleController
    turtle_controller = TurtleController()
    # Executa o loop principal do nó até que o programa seja encerrado
    rclpy.spin(turtle_controller)
    # Destrói o nó quando o programa é encerrado
    turtle_controller.destroy_node()
    # Encerra o contexto do ROS
    rclpy.shutdown()

if __name__ == '__main__':
    # chamando a função principal
    main()
