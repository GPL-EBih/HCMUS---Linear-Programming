import numpy as np
import pandas as pd
class LinearProgrammingProblem:
    def __init__(self, num_vars, num_cons, is_min, obj_coeffs, constraint_matrix, constraint_rhs, constraint_signs, variable_signs):
        self.num_vars = num_vars
        self.num_cons = num_cons
        self.is_min = is_min
        self.obj_coeffs = obj_coeffs
        self.constraint_matrix = constraint_matrix
        self.constraint_rhs = constraint_rhs
        self.constraint_signs = constraint_signs
        self.variable_signs = variable_signs
        self.num_new_vars = 0

    def solve(self):
        self.convert_to_standard_form()
        tableau = np.zeros((self.num_cons + 1, self.num_vars + self.num_cons + 1))
        tableau = self.initialize_tableau(tableau)

        check = 0

        algorithm_choice = self.choose_algorithm()
        if algorithm_choice == 0:
            tableau, check = self.dantzig_method(tableau)
        elif algorithm_choice == 1:
            tableau, check = self.bland_method(tableau)
        else:
            tableau, check = self.two_phase_method(tableau)

        return self.process_output(tableau, check)

    def display(self):
        objective_function = ""
        if self.is_min:
            objective_function = "Min z = "
        else:
            objective_function = "Max z = "

        for j in range(self.num_vars):
            coefficient = self.obj_coeffs[j]
            if coefficient >= 0 and j != 0:
                objective_function += " + " + str(coefficient) + "x" + str(j + 1)
            else:
                objective_function += str(coefficient) + "x" + str(j + 1)

        print(objective_function)

        for i in range(self.num_cons):
            constraint = ""
            for j in range(self.num_vars):
                coefficient = self.constraint_matrix[i, j]
                if coefficient >= 0 and j != 0:
                    constraint += " + " + str(coefficient) + "x" + str(j + 1)
                else:
                    constraint += str(coefficient) + "x" + str(j + 1)

            if self.constraint_signs[i] == 1:
                constraint += ">= "
            elif self.constraint_signs[i] == 0:
                constraint += "= "
            else:
                constraint += "<= "

            constraint += str(self.constraint_rhs[i])
            print(constraint)

        for j in range(self.num_vars):
            variable = "x" + str(j + 1)
            if self.variable_signs[j] == 1:
                variable += " >= 0"
            elif self.variable_signs[j] == -1:
                variable += " <= 0"
            else:
                break
            print(variable)

    def convert_to_standard_form(self):
        # Objective Function
        if not self.is_min:
            self.obj_coeffs = -self.obj_coeffs

        # Variable Signs
        for i in range(self.num_vars - self.num_new_vars):
            if self.variable_signs[i] == -1:
                self.obj_coeffs[i] = -self.obj_coeffs[i]
                self.constraint_matrix[:, i] = -self.constraint_matrix[:, i]
            elif self.variable_signs[i] == 0:
                self.num_vars += 1
                self.num_new_vars += 1
                self.variable_signs = np.append(self.variable_signs, 0)
                self.obj_coeffs = np.append(self.obj_coeffs, -self.obj_coeffs[i])
                self.constraint_matrix = np.concatenate((self.constraint_matrix, -np.array([self.constraint_matrix[:, i]]).T), axis=1)

        # Constraint Signs
        for i in range(self.num_cons):
            if self.constraint_signs[i] == 1:
                self.constraint_matrix[i] = -self.constraint_matrix[i]
                self.constraint_rhs[i] = -self.constraint_rhs[i]
                self.constraint_signs[i] = -1
            elif self.constraint_signs[i] == 0:
                self.num_cons += 1
                self.constraint_signs[i] = -1
                self.constraint_signs = np.append(self.constraint_signs, -1)
                self.constraint_matrix = np.concatenate((self.constraint_matrix, -np.array([self.constraint_matrix[i]])), axis=0)
                self.constraint_rhs = np.append(self.constraint_rhs, -self.constraint_rhs[i])

    def print_table(self, tableau):
        print(tableau)

    def choose_pivot_dantzig(self, tableau, xPivot, yPivot, phase1):
        minC = 0
        yPivot = -1
        for i in range(tableau.shape[1] - 1):
            if (tableau[0, i] < 0) and (tableau[0, i] < minC):
                minC = tableau[0, i]
                yPivot = i
        if yPivot == -1:
            return xPivot, yPivot, 0
        xPivot = self.find_arg_min_ratio(tableau, yPivot, phase1)
        if xPivot == -1:
            return xPivot, yPivot, -1
        return xPivot, yPivot, 1

    def dantzig_method(self, tableau, phase1=False):
        xPivot, yPivot = -1, -1
        while True:
            xPivot, yPivot, check = self.choose_pivot_dantzig(tableau, xPivot, yPivot, phase1)
            if check == 1:
                tableau, xPivot, yPivot = self.rotate_pivot(tableau, xPivot, yPivot)
            else:
                return tableau, -check

    def choose_pivot_bland(self, tableau, xPivot, yPivot):
        yPivot = -1
        for i in range(tableau.shape[1] - 1):
            if tableau[0, i] < 0:
                yPivot = i
                break
        if yPivot == -1:
            return xPivot, yPivot, 0
        xPivot = self.find_arg_min_ratio(tableau, yPivot, False)
        if xPivot == -1:
            return xPivot, yPivot, -1
        return xPivot, yPivot, 1
                    
    def bland_method(self, tableau):
        xPivot, yPivot = -1, -1
        while True:
            xPivot, yPivot, check = self.choose_pivot_bland(tableau, xPivot, yPivot)
            if check != 1:
                return tableau, -check
            else:
                tableau, xPivot, yPivot = self.rotate_pivot(tableau, xPivot, yPivot)
        return tableau, 0        

    def find_pivot_column(self, tableau, col):
        xPivot = -1
        flag = False
        for i in range(1, tableau.shape[0]):
            if tableau[i, col] == 0:
                continue

            if tableau[i, col] == 1:
                if flag is False:
                    xPivot = i
                    flag = True
                else:
                    return -1
            else:
                return -1

        return xPivot

    def two_phase_method(self, tableau):
        # Add x0
        tableauP1 = np.zeros((tableau.shape[0], tableau.shape[1] + 1))
        tableauP1[0, -2] = 1
        tableauP1[1:, -2] = -np.ones((tableau.shape[0] - 1, 1)).ravel()
        tableauP1[1:, :tableau.shape[1] - 1] = tableau[1:, :tableau.shape[1] - 1]
        tableauP1[1:, -1] = tableau[1:, -1]

        xPivot, yPivot = -1, tableauP1.shape[1] - 2
        minB = 0
        for i in range(tableauP1.shape[0]):
            if tableau[i, yPivot] < minB:
                minB = tableau[i, yPivot]
                xPivot = i
        tableauP1, xPivot, yPivot = self.rotate_pivot(tableauP1, xPivot, yPivot)
        tableauP1, check = self.dantzig_method(tableauP1, 1)

        for j in range(tableauP1.shape[1] - 2):
            if tableauP1[0, j] != 0:
                return tableau, -1  # No solution

        # Phase 2
        tableau[1:, :tableau.shape[1] - 1] = tableauP1[1:, :tableau.shape[1] - 1]
        tableau[1:, -1] = tableauP1[1:, -1]

        for j in range(tableau.shape[1]):
            xPivot = self.find_pivot_column(tableau, j)
            if xPivot == -1:
                continue
            tableau, xPivot, j = self.rotate_pivot(tableau, xPivot, j)

        tableau, check = self.dantzig_method(tableau)
        return tableau, check
    
    def check_unique_solution(self, tableau, pivots):
        for i in range(tableau.shape[1] - 1):
            if (i >= self.num_vars - self.num_new_vars) and (i < self.num_vars):
                continue
            if ((pivots[i] == -1) and (abs(tableau[0, i]) < 1e-6)) and (self.variable_signs[i] != 0):
                return False
        return True
        
    def find_variable_name(self, tableau, index):
        name = ""
        if index < self.num_vars - self.num_new_vars:
            name = "x" + str(index + 1)
            return 1, name
        elif (index + 1 > self.num_vars) and (index + 1 < tableau.shape[1]):
            name = "w" + str(index + 1 - self.num_vars)
            return 1, name
        return 0, name
    
    def initialize_tableau(self, tableau):
        tableau[0, :self.num_vars] = self.obj_coeffs
        tableau[0, -1] = 0
        tableau[1:, :self.num_vars] = self.constraint_matrix
        tableau[1:, self.num_vars:-1] = np.identity(self.num_cons)
        tableau[1:, -1] = self.constraint_rhs

        self.variable_signs = np.append(self.variable_signs, np.ones(self.num_cons))
        return tableau

    def process_output(self, tableau, result):
        print("Tableau:", tableau)
        print("Result:", result)
        output = "<hr><h1>RESULT</h1><hr>"

        if result == 1:
            if self.is_min:
                output += " => The problem is <b>UNBOUNDED</b>. <br> MIN z = - <b>" + str(np.inf) + "</b> <br>"
            else:
                output += " => The problem is <b>UNBOUNDED</b>. <br> MAX z = + <b>" + str(np.inf) + "</b> <br>"
        elif result == 0:
            if self.is_min:
                output += "<u>MIN z = <b>" + str(-tableau[0, -1]) + "</b></u> <br>"
            else:
                output += "<u>MAX z = <b>" + str(tableau[0, -1]) + "</b></u> <br>"

            pivots = np.array([self.find_pivot_column(tableau, i) for i in range(tableau.shape[1] - 1)])
            if self.check_unique_solution(tableau, pivots):
                output += '<b> => UNIQUE SOLUTION.</b> The optimal solution is: <br>'
                for j in range(self.num_vars - self.num_new_vars):
                    if tableau[0, j] != 0:
                        output += f"x<sub>{j + 1}</sub> = 0<br>"
                        continue
                    count = 0
                    index = 0
                    for i in range(1, tableau.shape[0]):
                        if tableau[i, j] != 0:
                            count += 1
                            index = i
                    if self.variable_signs[j] == -1:
                        output += f"x<sub>{j + 1}</sub> = {-tableau[index, -1]}<br>"
                    else:
                        output += f"x<sub>{j + 1}</sub> = {tableau[index, -1]}<br>"
            else:
                output += "<b> => MULTIPLE SOLUTIONS.</b> <br>"
                output += "The optimal solution set is: <br>"
                sign = np.array([-1 if ((self.variable_signs[i] < 0) & (i < self.num_vars - self.num_new_vars)) else 1 for i in range(tableau.shape[1] - 1)])
                for i in range(self.num_vars - self.num_new_vars):
                    if pivots[i] == -1:
                        if abs(tableau[0, i]) > 1e-4:
                            output += f"x<sub>{i + 1}</sub> = 0<br>"
                        else:
                            if self.variable_signs[i] == 0:
                                output += f"x<sub>{i + 1}</sub> is free<br>"
                            elif self.variable_signs[i] == 1:
                                output += f"x<sub>{i + 1}</sub> >= 0<br>"
                            else:
                                output += f"x<sub>{i + 1}</sub> <= 0<br>"
                    else:
                        root = f"x<sub>{i + 1}</sub> = {sign[i] * tableau[pivots[i], -1]} <br>"
                        for j in range(tableau.shape[1] - 1):
                            if ((abs(tableau[0, j]) > 1e-4) | (pivots[j] != -1)) | (j == i):
                                continue
                            check_root, name = self.find_variable_name(tableau, j)
                            if check_root == 0:
                                continue
                            else:
                                if -sign[i] * sign[j] * tableau[pivots[i], j] == 0:
                                    continue
                                if -sign[i] * sign[j] * tableau[pivots[i], j] > 0:
                                    root += f"+ {-sign[i] * sign[j] * tableau[pivots[i], j]}{name} <br>"
                                else:
                                    root += f"{-sign[i] * sign[j] * tableau[pivots[i], j]}{name} <br>"
                        output += root
                output += "With:<br>"
                for i in range(tableau.shape[1] - 1):
                    if (i >= self.num_vars - self.num_new_vars) & (i < self.num_vars):
                        continue
                    if (i < self.num_vars - self.num_new_vars) & (self.variable_signs[i] == 0):
                        continue
                    if pivots[i] == -1:
                        if i < self.num_vars - self.num_new_vars:
                            continue
                        if abs(tableau[0, i]) < 1e-4:
                            check_root, name = self.find_variable_name(tableau, i)
                            if check_root == 1:
                                if i >= self.num_vars - self.num_new_vars:
                                    output += f"{name} >= 0<br>"
                                else:
                                    if self.variable_signs[i] == 0:
                                        output += f"{name} is free<br>"
                                    elif self.variable_signs[i] < 0:
                                        output += f"{name} <= 0<br>"
                                    else:
                                        output += f"{name} >= 0<br>"
                    else:
                        root = f"{sign[i] * tableau[pivots[i], -1]}"
                        for j in range(tableau.shape[1] - 1):
                            if (abs(tableau[0, j]) > 1e-4) | (pivots[j] != -1):
                                continue
                            check_root, name = self.find_variable_name(tableau, j)
                            if check_root == 0:
                                continue
                            else:
                                if -sign[i] * sign[j] * tableau[pivots[i], j] == 0:
                                    continue
                                if -sign[i] * sign[j] * tableau[pivots[i], j] > 0:
                                    root += f"+ {-sign[i] * sign[j] * tableau[pivots[i], j]}{name}<br>"
                                else:
                                    root += f"{-sign[i] * sign[j] * tableau[pivots[i], j]}{name}<br>"
                        root += " >= 0<br>"
                        output += root
        else:
            output += "<b> => NO SOLUTION</b>.<br>"
        print(output)
        return output
    
    def choose_algorithm(self):
        flag = 0
        for i in range(self.num_cons):
            if self.constraint_rhs[i] == 0:  # Bland
                flag = 1
            if self.constraint_rhs[i] < 0:  # Two-phase
                return 2
        return flag

    def rotate_pivot(self, tableau, xPivot, yPivot):
        for i in range(tableau.shape[0]):
            if i != xPivot:
                coef = -tableau[i, yPivot] / tableau[xPivot, yPivot]
                tableau[i, :] += coef * tableau[xPivot, :]
            else:
                coef = tableau[xPivot, yPivot]
                tableau[xPivot, :] /= coef
        return tableau, xPivot, yPivot

    def find_arg_min_ratio(self, tableau, yPivot, phase1):
        i = 0
        xPivot = -1
        minRatio = -1
        ratio = 0
        for i in range(tableau.shape[0]):
            if tableau[i, yPivot] > 0:
                minRatio = tableau[i, -1] / tableau[i, yPivot]
                xPivot = i
                break
        if xPivot == -1:
            return -1
        for i in range(1, tableau.shape[0]):
            if tableau[i, yPivot] > 0:
                ratio = tableau[i, -1] / tableau[i, yPivot]
                if ratio < minRatio:
                    minRatio = ratio
                    xPivot = i
                if phase1 is True:
                    if (ratio == minRatio) and (tableau[i, -2] == 1):
                        xPivot = i
        return xPivot