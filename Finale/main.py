from flask import Flask, render_template, request
from solver import *
from preprocessing import *




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numVariables = int(request.form['numVariables'])
        numConstraints = int(request.form['numConstraints'])

        isMin = request.form['isMin']
        if isMin == 'Min':
            isMin = True
        else:
            isMin = False

        Target = request.form['Target']
        Constraints = request.form['Constraints']
        Variables = request.form['Variables']

        # in các biến và ràng buộc của bài toán
        print("Number of Variables:", numVariables)
        print("Number of Constraints:", numConstraints)
        print("Is Minimization:", isMin)
        print("Target Function:", Target)
        print("Constraints:", Constraints)
        print("Variables:", Variables)
        
        
        num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables = preprocessing_problem(numVariables, numConstraints, isMin, Target, Constraints, Variables)
        print("b là: ", b)
        p = Problem(num_variables, num_constraints, is_min, target, A, b, sign_constraints, sign_variables)
        result = p.solve_problem()

        return render_template('./website/result.html', result=result)

    return render_template('./website/index.html')

if __name__ == "__main__":
    app.run(debug=True)






#  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .venv\Scripts\Activate

