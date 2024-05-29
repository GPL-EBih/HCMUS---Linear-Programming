
#  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .venv\Scripts\Activate
from flask import Flask, render_template, request, jsonify
from solver import *
import os 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('website/system.html')

@app.route('/submit', methods=['POST'])

def submit():
    data = request.json

    # Nhận dữ liệu từ request
    target_function = data['targetFunction']
    optimization_type = data['optimizationType']
    variable_constraints = data['variableConstraints']
    constraint_matrix = data['constraintMatrix']
    constraint_b_rule = data['constraintB_Rule']
   


    num_variables = len(variable_constraints)
    num_constraints = len(constraint_matrix)
    target = target_function
    is_min = optimization_type
    A = constraint_matrix
    b = constraint_b_rule

    def convert_sign(sign):
        if sign == 's':
            return -1
        elif sign == 'e':
            return 0
        else:
            return 1
    
    
    def split_data(data):
        # Khởi tạo hai danh sách rỗng
        b = []
        sign_constraints = []

        # Lặp qua từng phần tử trong danh sách ban đầu
        for item in data:
            b.append(item[0])  # Thêm giá trị số vào danh sách b
            sign_constraints.append(item[1])  # Thêm chuỗi vào danh sách sign_constraints

        # Trả về kết quả dưới dạng một tuple
        return b, sign_constraints

    b, sign_constraints = split_data(b)

    for i in range(len(sign_constraints)):
        sign_constraints[i] = convert_sign(sign_constraints[i])

    P = []
    variable_constraints, P = split_data(variable_constraints)
    
    for i in range(len(variable_constraints)):
        variable_constraints[i] = convert_sign(variable_constraints[i])



    num_variables = int(num_variables)
    num_constraints = int(num_constraints)



    target = np.array(target)
    A = np.array(A)
    b = np.array(b)
    sign_constraints = np.array(sign_constraints)
    variable_constraints = np.array(variable_constraints)

    
    print("num_variables: ", num_variables)
    print("num_constraints: ", num_constraints)
    print("target: ", target)
    print("is_min: ", is_min)
    print("A: ", A)
    print("b: ", b)
    print("sign_constraints: ", sign_constraints)
    print("variable_constraints: ", variable_constraints)
    sign_variables = variable_constraints

    if is_min == 'True':
        is_min = True
    if is_min == 'False':
        is_min = False
    
    
    p = LinearProgrammingProblem(num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables)
    result = p.solve()

    return jsonify(answer=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
