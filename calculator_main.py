##202130443 이승엽
import sys
from PyQt5.QtWidgets import *
from math import sqrt

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # 등호가 눌렸는지, 수식을 저장할 리스트 초기화
        self.equal_pressed = False
        self.expression = []

        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_operation2 = QHBoxLayout()
        layout_operation3 = QHBoxLayout()
        layout_number = QGridLayout()
        layout_equation_solution = QVBoxLayout()
        layout_operation = QVBoxLayout()
        layout_sub = QHBoxLayout()
        

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.equation = QLineEdit("")
        self.equation.setReadOnly(True)
        self.equation.setFixedHeight(50)

        ### layout_equation_solution 레이아웃에 수식 위젯을 추가
        layout_equation_solution.addWidget(self.equation)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num=number:
                                                       self.number_button_clicked(num))
            if number > 0:
                x, y = divmod(number - 1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number == 0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num=".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("±")
        button_double_zero.clicked.connect(lambda state, num="": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 3, 0)

        ### 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_clear2 = QPushButton("CE")
        button_modulo = QPushButton("%")
        button_backspace = QPushButton("⬅️")
        button_reciprocal = QPushButton("1/x")
        button_square = QPushButton("x^2")
        button_square_root = QPushButton("√x")


        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_clear2.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        # %, 1/x, x^2, √x 버튼 클릭 시 시그널 설정
        button_modulo.clicked.connect(self.button_modulo_clicked)
        button_reciprocal.clicked.connect(self.button_reciprocal_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_square_root.clicked.connect(self.button_square_root_clicked)

        ### 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("÷")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation="+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation="-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation="*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation="/": self.button_operation_clicked(operation))

        ### layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_product)
        layout_operation.addWidget(button_minus)
        layout_operation.addWidget(button_plus)
        layout_operation.addWidget(button_equal)
        
        layout_operation2.addWidget(button_modulo)
        layout_operation2.addWidget(button_clear2)
        layout_operation2.addWidget(button_clear)
        layout_operation2.addWidget(button_backspace)

        layout_operation3.addWidget(button_reciprocal)
        layout_operation3.addWidget(button_square)
        layout_operation3.addWidget(button_square_root)
        layout_operation3.addWidget(button_division)
        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_operation2)
        main_layout.addLayout(layout_operation3)
        
        # 새로운 레이아웃 추가: layout_number와 layout_operation을 수평으로 정렬
        
        layout_sub.addLayout(layout_number)
        layout_sub.addLayout(layout_operation)

        main_layout.addLayout(layout_sub)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        if self.equal_pressed:
            self.equation.setText(str(num))
            self.expression = [num]
            self.equal_pressed = False
        else:
            equation = self.equation.text()
            equation += str(num)
            self.expression.append(num)
            self.equation.setText(equation)


    def button_operation_clicked(self, operation):
        self.equal_pressed = False
        self.equation.setText("")
        self.expression.append(operation)
        

    def button_equal_clicked(self):
        self.equal_pressed = True
        try:
            solution = eval(''.join(map(str, self.expression)))
            self.equation.setText(str(solution))
            self.expression = [solution]
        except Exception as e:
            self.equation.setText("Error")

    def button_clear_clicked(self):
        self.equal_pressed = False
        self.expression.clear()
        self.equation.setText("")

    def button_backspace_clicked(self):
        self.equal_pressed = False
        if self.expression:
            if isinstance(self.expression[-1], (int, float)):
                self.expression[-1] = str(self.expression[-1])[:-1]
                if not self.expression[-1]:
                    self.expression.pop()
            elif isinstance(self.expression[-1], str):
                self.expression[-1] = self.expression[-1][:-1]
                if not self.expression[-1]:
                    self.expression.pop()

        equation = ''.join(map(str, self.expression))
        self.equation.setText(equation)


    def button_modulo_clicked(self):
        self.equal_pressed = False
        self.equation.setText("")
        self.expression.append("%")
        

    def calculate_expression(self):
        try:
            result = eval(''.join(map(str, self.expression)))
            self.equation.setText(str(result))
            self.expression = [result]
        except Exception as e:
            self.equation.setText("Error")

    def button_square_clicked(self):
        self.equal_pressed = True
        if self.expression:
            self.expression.append('**2')
            equation = ''.join(map(str, self.expression))
            self.equation.setText(equation)
            self.calculate_expression()

    def button_square_root_clicked(self):
        self.equal_pressed = True
        if self.expression:
            self.expression.append('**(1/2)')
            equation = ''.join(map(str, self.expression))
            self.equation.setText(equation)
            self.calculate_expression()

    def button_reciprocal_clicked(self):
        self.equal_pressed = True
        if self.expression:
            try:
                reciprocal = 1 / eval(''.join(map(str, self.expression)))
                self.expression = [reciprocal]
                self.equation.setText(str(reciprocal))
            except ZeroDivisionError:
                self.equation.setText("Error: Division by zero")
            except Exception as e:
                self.equation.setText("Error")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())