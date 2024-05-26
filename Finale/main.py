# from flask import Flask, render_template, request
# from solver import *
# from preprocessing import *




# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         numVariables = int(request.form['numVariables'])
#         numConstraints = int(request.form['numConstraints'])

#         isMin = request.form['isMin']
#         if isMin == 'Min':
#             isMin = True
#         else:
#             isMin = False

#         Target = request.form['Target']
#         Constraints = request.form['Constraints']
#         Variables = request.form['Variables']

#         # in các biến và ràng buộc của bài toán
#         print("Number of Variables:", numVariables)
#         print("Number of Constraints:", numConstraints)
#         print("Is Minimization:", isMin)
#         print("Target Function:", Target)
#         print("Constraints:", Constraints)
#         print("Variables:", Variables)
        
        
#         num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables = preprocessing_problem(numVariables, numConstraints, isMin, Target, Constraints, Variables)
#         print("b là: ", b)
#         p = Problem(num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables)
#         result = p.solve_problem()

#         return render_template('./templates/website/', result=result)

#     return render_template('./templates/website/index.html')

# if __name__ == "__main__":
#     app.run(debug=True)





# python -m venv .venv
# Cài thư viện trong requirement
#  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .venv\Scripts\Activate
from flask import Flask, render_template, request, jsonify
from solver import *

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
    # num_variables = data['numVariables']
    # num_constraints = data['numConstraints']
    
    # print('num_variables: ', num_variables)
    # print('num_constraints: ', num_constraints)
    print('target_function: ', target_function)
    print('optimization_type: ', optimization_type)
    print('variable_constraints: ', variable_constraints)
    print('constraint_matrix: ', constraint_matrix)
    print('constraint_b_rule: ', constraint_b_rule)
    print("=====================================")

    print("Xu ly")

    # in ra kiểu dữ liệu 
    # print(type(num_variables))
    # print(type(num_constraints))
    print(type(optimization_type))
    print(type(target_function))
    print(type(optimization_type))
    print(type(variable_constraints))
    print(type(constraint_matrix))
    print(type(constraint_b_rule))
    print("=====================================")
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

    # sign_constraints = convert_sign(sign_constraints)

    # kiểm tra sign_constraints từng phần tử rồi gắn giá trị bằng hàm convert_sign
    for i in range(len(sign_constraints)):
        sign_constraints[i] = convert_sign(sign_constraints[i])

    P = []
    variable_constraints, P = split_data(variable_constraints)
    
    for i in range(len(variable_constraints)):
        variable_constraints[i] = convert_sign(variable_constraints[i])



    num_variables = int(num_variables)
    num_constraints = int(num_constraints)

    # def convert_list_to_int(input_list):
    #     """
    #     Chuyển đổi các giá trị trong danh sách lồng nhau thành số nguyên.
        
    #     Args:
    #         input_list (list): Danh sách chứa các giá trị hoặc danh sách lồng nhau.
            
    #     Returns:
    #         list: Danh sách mới sau khi đã chuyển đổi các giá trị thành số nguyên.
    #     """
    #     result = []
        
    #     for item in input_list:
    #         # Nếu phần tử là một danh sách, gọi đệ quy để chuyển đổi nó thành số
    #         if isinstance(item, list):
    #             result.append(convert_list_to_int(item))
    #         else:
    #             # Nếu không phải là một danh sách, chuyển đổi giá trị thành số nguyên
    #             try:
    #                 int_value = int(item)
    #                 result.append(int_value)
    #             except ValueError:
    #                 # Nếu không thể chuyển đổi thành số, giữ nguyên giá trị
    #                 result.append(item)
        
    #     return result
    
    # # Chuyển đổi các giá trị trong biến trừ is_min thành số nguyên
    # num_variables = int(num_variables)
    # num_constraints = int(num_constraints)
    # target = convert_list_to_int(target)
    # A = convert_list_to_int(A)
    # b = convert_list_to_int(b)
    # sign_constraints = convert_list_to_int(sign_constraints)
    # variable_constraints = convert_list_to_int(variable_constraints)


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

    # Đảm bảo các giá trị trong biến trừ is_min là kiểu float hết
    
    


    p = Problem(num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables)
    result = p.solve_problem()

    # result = "Dữ liệu đã được nhận và xử lý thành công! <br>"
    
    # Trả về kết quả dưới dạng JSON
    return jsonify(answer=result)

if __name__ == '__main__':
    app.run(debug=True)
