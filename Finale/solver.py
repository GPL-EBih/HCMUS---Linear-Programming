import numpy as np
import pandas as pd
import re

class Problem:
    def __init__(self, num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables):
        # Number of variables and constraints
        self.num_variables = num_variables
        self.num_constraints = num_constraints
        # Objective Function
        self.is_min = is_min
        self.target = target
        # Constraints
        self.A = A
        self.b = b
        self.sign_constraints = sign_constraints
        # Sign Variables
        self.sign_variables = sign_variables
        # Others
        self.num_new_variable = 0
    
    def printProblem(self):
        Objective = ""
        if self.is_min:
            Objective = "Min z = "
        else: 
            Objective = "Max z = "
        for j in range(self.num_variables):
            if (self.target[j] >= 0) and (j != 0):
                Objective += " + " + str(self.target[j]) + "x" + str(j+1) + " "
            else:
                Objective += str(self.target[j]) + "x" + str(j+1) + " "
        print(Objective)
        for i in range(self.num_constraints):
            Cons = ""
            for j in range(self.num_variables):
                if (self.A[i, j] >= 0) and (j != 0):
                    Cons += " + " + str(self.A[i, j]) + "x" + str(j+1) + " "
                else:
                    Cons += str(self.A[i, j]) + "x" + str(j+1) + " "
            if self.sign_constraints[i] == 1:
                Cons += ">= "
            elif self.sign_constraints[i] == 0:
                Cons += "= "
            else:
                Cons += "<= "
            Cons += str(self.b[i])
            print(Cons)
        for j in range(self.num_variables):
            Vars = "x" + str(j+1)
            if self.sign_variables[j] == 1:
                Vars += " >= 0"
            elif self.sign_variables[j] == -1:
                Vars += " <= 0"
            else:
                break
            print(Vars)

    def convert_into_normal_form(self):
        # Objective Function
        if self.is_min == False:
            self.target = - self.target
        
        # Sign Variables
        for i in range(self.num_variables-self.num_new_variable):
            if self.sign_variables[i] == -1: # xi <= 0
                self.target[i] = - self.target[i]
                self.A[:, i] = - self.A[:, i]
            elif self.sign_variables[i] == 0: # xi tu do
                self.num_variables += 1
                self.num_new_variable += 1
                self.sign_variables = np.append(self.sign_variables, 0)
                self.target = np.append(self.target, - self.target[i])
                self.A = np.concatenate((self.A, - np.array([self.A[:, i]]).T), axis = 1) 

        # Sign Constraints
        for i in range(self.num_constraints):
            if self.sign_constraints[i] == 1:
                self.A[i] = - self.A[i]
                self.b[i] = - self.b[i]
                self.sign_constraints[i] = -1
            elif self.sign_constraints[i] == 0:
                self.num_constraints += 1
                self.sign_constraints[i] = -1   
                self.sign_constraints = np.append(self.sign_constraints, -1)
                self.A = np.concatenate((self.A, - np.array([self.A[i]])), axis = 0)
                self.b = np.append(self.b, -self.b[i])

    def convert_into_table_form(self, Table):
        Table[0, :self.num_variables] = np.array([self.target])
        Table[0, -1] = 0
        Table[1:, :self.num_variables] = self.A
        Table[1:, self.num_variables:-1] = np.identity(self.num_constraints)
        Table[1:, -1] = self.b

        self.sign_variables = np.append(self.sign_variables, np.ones((1, self.num_constraints)))
        return Table

    def print_table(self, Table):
        print(Table)

    def choose_algorithm(self):
        bland = False

        for i in range(self.num_constraints):
            if self.b[i] < 0:
                return 2
            if self.b[i] == 0:
                bland = True

        return bland

    def rotate_pivot(self, Table, xPivot, yPivot):
        for i in range(Table.shape[0]):
            if i != xPivot:
                coef = - Table[i, yPivot] / Table[xPivot, yPivot]
                Table[i,:] += coef * Table[xPivot,:]
            else:
                coef = Table[xPivot, yPivot]
                Table[xPivot,:] /= coef
        return Table, xPivot, yPivot

    def find_arg_min_ratio(self, Table, yPivot, phase1):
        i = 0
        xPivot = -1
        minRatio = -1
        ratio = 0
        for i in range(Table.shape[0]):
            if Table[i, yPivot] > 0:
                minRatio = Table[i, -1] / Table[i, yPivot]
                xPivot = i
                break
        if xPivot == -1:
            return -1
        for i in range(1, Table.shape[0]):
            if Table[i, yPivot] > 0:
                ratio = Table[i, -1] / Table[i, yPivot]
                if ratio < minRatio:
                    minRatio = ratio
                    xPivot = i
                if phase1 == True:
                    if (ratio == minRatio) and (Table[i, -2] == 1):
                        xPivot = i
        return xPivot

    def choose_pivot_dantzig(self, Table, xPivot, yPivot, phase1):
        minC = 0
        yPivot = -1
        for i in range(Table.shape[1]-1):
            if (Table[0, i] < 0) and (Table[0, i] < minC):
                minC = Table[0, i]
                yPivot = i
        if yPivot == -1:
            return xPivot, yPivot, 0
        xPivot = self.find_arg_min_ratio(Table, yPivot, phase1)
        if xPivot == -1:
            return xPivot, yPivot, -1
        return xPivot, yPivot, 1

    def dantzig(self, Table, phase1 = False):
        xPivot, yPivot = -1, -1
        while True:
            xPivot, yPivot, check = self.choose_pivot_dantzig(Table, xPivot, yPivot, phase1)
            if check == 1:
                Table, xPivot, yPivot = self.rotate_pivot(Table, xPivot, yPivot)
            else:
                return Table, - check

    def choose_pivot_bland(self, Table, xPivot, yPivot):
        yPivot = -1
        for i in range(Table.shape[1]-1):
            if Table[0, i] < 0:
                yPivot = i
                break
        if yPivot == -1:
            return xPivot, yPivot, 0
        xPivot = self.find_arg_min_ratio(Table, yPivot, False)
        if xPivot == -1:
            return xPivot, yPivot, -1
        return xPivot, yPivot, 1
    
    def bland(self, Table):
        xPivot, yPivot = -1, -1
        while True:
            xPivot, yPivot, check = self.choose_pivot_bland(Table, xPivot, yPivot)
            if check != 1:
                return Table, - check
            else:
                Table, xPivot, yPivot = self.rotate_pivot(Table, xPivot, yPivot)
        return Table, 0

    def find_pivot_of_column(self, Table, col):
        xPivot = -1
        flag = False
        for i in range(1, Table.shape[0]):
            if Table[i, col] == 0:
                continue

            if Table[i, col] == 1:
                if flag == False:
                    xPivot = i
                    flag = True
                else:
                    return -1
            else:
                return -1
            
        return xPivot
    
    def twophase(self, Table):
        # Add x0
        TableP1 = np.zeros((Table.shape[0], Table.shape[1]+1))
        TableP1[0, -2] = 1
        TableP1[1:, -2] = -np.ones((Table.shape[0]-1,1)).ravel()   
        TableP1[1:,:Table.shape[1]-1] = Table[1:, :Table.shape[1]-1]
        TableP1[1:, -1] = Table[1:, -1]
        
        xPivot, yPivot = -1, TableP1.shape[1]-2
        minB = 0
        for i in range(TableP1.shape[0]):
            if Table[i, yPivot] < minB:
                minB = Table[i, yPivot]
                xPivot = i
        TableP1, xPivot, yPivot = self.rotate_pivot(TableP1, xPivot, yPivot)
        TableP1, check = self.dantzig(TableP1, 1)
        
        for j in range(TableP1.shape[1]-2):
            if TableP1[0, j] != 0:
                return Table, -1 # Vo nghiem
        
        # Phase 2
        Table[1:, :Table.shape[1]-1] = TableP1[1:, :Table.shape[1]-1]
        Table[1:, -1] = TableP1[1:, -1]

        for j in range(Table.shape[1]):
            xPivot = self.find_pivot_of_column(Table, j)
            if xPivot == -1:
                continue
            Table, xPivot, j = self.rotate_pivot(Table, xPivot, j)

        Table, check = self.dantzig(Table)
        return Table, check

    def check_one_root(self, Table, pivots):
        for i in range(Table.shape[1]-1):
            if (i >= self.num_variables - self.num_new_variable) and (i < self.num_variables):
                continue
            if ((pivots[i] == -1) and (abs(Table[0, i]) < 1e-6)) and (self.sign_variables[i] != 0):
                return False
        return True

    

    def find_name_variable(self, Table, index):
        name = ""
        if index < self.num_variables - self.num_new_variable:
            name = "x" + str(index + 1)
            return 1, name
        elif (index + 1 > self.num_variables) and (index + 1 < Table.shape[1]):
            name = "w" + str(index + 1 - self.num_variables)
            return 1, name
        return 0, name
            

   
    def output_problem(self, Table, result):
        print("Table: ", Table)
        print("Result: ", result)
        output = "   KẾT QUẢ BÀI TOÁN   <br>"
        if result == 1: 
            if self.is_min == True:
                output += "Bài toán không giới nội. Tức là Min z = -" + str(np.inf) + "<br>"
            else:
                output += "Bài toán không giới nội. Tức là Max z = +" + str(np.inf) + "<br>"
        elif result == 0:
            if self.is_min == True:
                output += "Min z = " + str(-Table[0,-1]) + "<br>"
            else:
                output += "Max z = " + str(Table[0,-1]) + "<br>"
            
            pivots = np.array([self.find_pivot_of_column(Table, i) for i in range(Table.shape[1]-1)])
            if self.check_one_root(Table, pivots) == True:
                output += 'Bài toán có nghiệm duy nhất. Nghiệm tối ưu là: <br>'
                for j in range(self.num_variables - self.num_new_variable):
                    if Table[0, j] != 0:
                        root = "x" + str(j+1) + " = 0<br>"
                        output += f"x{j+1} = 0<br>"
                        continue
                    count = 0
                    index = 0
                    for i in range(1, Table.shape[0]):
                        if Table[i, j] != 0:
                            count += 1
                            index = i
                    if self.sign_variables[j] == -1:
                        output += f"x{j+1} = {-Table[index, -1]}<br>"
                    else:
                        output += f"x{j+1} = {Table[index, -1]}<br>"
            else:
                output += "Bài toán có vô số nghiệm.<br>"
                output += "Nghiệm tối ưu có dạng: <br>"
                sign = np.array([-1 if ((self.sign_variables[i] < 0) and (i < self.num_variables - self.num_new_variable)) else 1 for i in range(Table.shape[1]-1)])
                for i in range(self.num_variables - self.num_new_variable):
                    if pivots[i] == -1:
                        if abs(Table[0,i]) > 1e-4:
                            output += f"x{i+1} = 0<br>"
                        else:
                            if self.sign_variables[i] == 0:
                                output += f"x{i+1} tự do<br>"
                            elif self.sign_variables[i] == 1:
                                output += f"x{i+1} >= 0<br>"
                            else:
                                output += f"x{i+1} <= 0<br>"
                    else:
                        root = f"x{i+1} = {sign[i] * Table[pivots[i],-1]} <br>"
                        for j in range(Table.shape[1]-1):
                            if ((abs(Table[0,j]) > 1e-4) or (pivots[j] != -1)) or (j == i):
                                continue
                            check_root, name = self.find_name_variable(Table, j)
                            if check_root == 0:
                                continue
                            else:
                                if -sign[i] * sign[j] * Table[pivots[i], j] == 0:
                                    continue
                                if -sign[i] * sign[j] * Table[pivots[i], j] > 0:
                                    root += f"+ {-sign[i] * sign[j] * Table[pivots[i], j]}{name} <br>"
                                else:
                                    root += f"{-sign[i] * sign[j] * Table[pivots[i], j]}{name} <br>"
                        output += root
                output += "Thỏa (các) điều kiện:<br>"
                for i in range(Table.shape[1]-1):
                    if (i >= self.num_variables - self.num_new_variable) and (i < self.num_variables):
                        continue
                    if (i < self.num_variables - self.num_new_variable) and (self.sign_variables[i] == 0):
                        continue
                    if pivots[i] == -1:
                        if i < self.num_variables - self.num_new_variable:
                            continue
                        if abs(Table[0,i]) < 1e-4:
                            check_root, name = self.find_name_variable(Table, i)
                            if check_root == 1:
                                if i >= self.num_variables - self.num_new_variable:
                                    output += f"{name} >= 0<br>"
                                else:
                                    if self.sign_variables[i] == 0:
                                        output += f"{name} tự do<br>"
                                    elif self.sign_variables[i] < 0:
                                        output += f"{name} <= 0<br>"
                                    else:
                                        output += f"{name} >= 0<br>"
                    else:
                        root = f"{sign[i]*Table[pivots[i], -1]}"
                        for j in range(Table.shape[1]-1):
                            if (abs(Table[0,j])> 1e-4) or (pivots[j] != -1):
                                continue
                            check_root, name = self.find_name_variable(Table, j)
                            if check_root == 0:
                                continue
                            else:
                                if -sign[i]*sign[j]*Table[pivots[i], j] == 0:
                                    continue
                                if -sign[i]*sign[j]*Table[pivots[i], j] > 0:
                                    root += f"+ {-sign[i]*sign[j]*Table[pivots[i], j]}{name} <br>"
                                else:
                                    root += f"{-sign[i]*sign[j]*Table[pivots[i], j]}{name} <br>"
                        root += " >= 0<br>"
                        output += root
                                
        else:
            output += "Bài toán vô nghiệm.<br>"
        print(output)

        return output


    def solve_problem(self):
        self.convert_into_normal_form()
        Table = np.zeros((self.num_constraints + 1, self.num_variables + self.num_constraints + 1))
        Table = self.convert_into_table_form(Table)

        check = 0

        if self.choose_algorithm() == 0: # Don hinh
            Table, check = self.dantzig(Table)
        elif self.choose_algorithm() == 1:
            Table, check = self.bland(Table)
        else:
            Table, check = self.twophase(Table)
        


        return self.output_problem(Table, check)


