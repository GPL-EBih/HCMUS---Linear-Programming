
import numpy as np
import pandas as pd
import re

def preprocessing_problem(numVariables, numConstraints, isMin, Target, Constraints, Variables):
    # Target 
    target = np.array([])
    for i in range(numVariables):
        if len(re.findall("x"+str(i+1), Target)) != 0:
            pattern = "(\d*)\s*x" + str(i+1)
            pattern_sign = "(\+|\-)\s*\d*x" + str(i+1)
            if (len(re.findall(pattern_sign, Target)) == 0) or (re.findall(pattern_sign, Target)[0] == "+"):
                if re.findall(pattern, Target)[0] == "":
                    target = np.append(target, 1)
                else:
                    target = np.append(target, int(re.findall(pattern, Target)[0]))
            else:
                if re.findall(pattern, Target)[0] == "":
                    target = np.append(target, -1)
                else:
                    target = np.append(target, -int(re.findall(pattern, Target)[0]))
        else:
            target = np.append(target, 0)

    # Constraints    
    constraints = np.empty((numConstraints, numVariables + 1))
    sign_constraints = np.array([])
    for row, Constraint in enumerate(Constraints.split("\n")):
        # A
        A_i = np.array([])
        for i in range(numVariables):
            if len(re.findall("x" + str(i+1), Constraint)) != 0:
                pattern = "(\d*)\s*x" + str(i+1)
                pattern_sign = "(\+|\-)\s*\d*x" + str(i+1)
                if (len(re.findall(pattern_sign, Constraint)) == 0) or (re.findall(pattern_sign, Constraint)[0] == "+"): 
                    if re.findall(pattern, Constraint)[0] == "":
                        A_i = np.append(A_i, 1)  # Sửa đổi thành 1 nếu không có số được tìm thấy
                    else:
                        A_i = np.append(A_i, int(re.findall(pattern, Constraint)[0]))
                else:
                    if re.findall(pattern, Constraint)[0] == "":
                        A_i = np.append(A_i, -1)  # Sửa đổi thành -1 nếu không có số được tìm thấy
                    else:
                        A_i = np.append(A_i, -int(re.findall(pattern, Constraint)[0]))
            else:
                A_i = np.append(A_i, 0)

        # Sign
        sig = re.findall("=|\<=|\>=", Constraint)[0]
        if sig == "=":
            sign_constraints = np.append(sign_constraints, 0)
        elif sig == ">=":
            sign_constraints = np.append(sign_constraints, 1)
        else:
            sign_constraints = np.append(sign_constraints, -1)


        # b
        b_value = 0  # Giá trị mặc định cho b
        print('Constraint: ', Constraint)
        matches = re.findall(r'[-+]?\d+(?:\.\d+)?(?=\s*$)', Constraint)  # Tìm các số ở cuối chuỗi
        print('matches: ',matches)
        if matches:  # Kiểm tra xem có giá trị nào được tìm thấy hay không
            b_value = int(matches[0])  # Lấy giá trị đầu tiên nếu có

        # Thêm giá trị mặc định của biến b vào A_i nếu không tìm thấy giá trị b trong ràng buộc
        if len(matches) == 0:
            A_i = np.append(A_i, b_value)
        elif (len(re.findall("(\+|\-)\d+$", Constraint)) == 0) or (re.findall("(\+|\-)\d+$", Constraint)[0] == "+"):
            A_i = np.append(A_i, b_value)
        else:
            A_i = np.append(A_i, -b_value)

        constraints[row] = A_i


    # Variables
    sign_variables = np.zeros(numVariables)
    for Variable in Variables.split("\n"):
        num = int(re.findall("x(\d+)", Variable)[0])
        sig = re.findall("tự do|\>=|\<=", Variable)[0]
        if sig == ">=":
            sign_variables[num-1] = 1
        elif sig == "<=":
            sign_variables[num-1] = -1
        else:
            sign_variables[num-1] = 0

    return numVariables, numConstraints, isMin, target, constraints[:,:-1], constraints[:,-1], sign_constraints, sign_variables  
    