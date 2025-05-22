from sparse_matrix import SparseMatrix

def load_matrix(prompt):
    path = input(f"Enter path for {prompt} matrix file: ").strip()
    return SparseMatrix(file_path=path)

def main():
    print("Sparse Matrix Operations")
    print("1. Addition")
    print("2. Subtraction") 
    print("3. Multiplication")
    
    choice = input("Choose an operation (1/2/3): ").strip()
    
    try:
        matrix1 = load_matrix("first")
        matrix2 = load_matrix("second")
        
        if choice == '1':
            result = matrix1.add(matrix2)
            print("Result of addition:")
        elif choice == '2':
            result = matrix1.subtract(matrix2)
            print("Result of subtraction:")
        elif choice == '3':
            result = matrix1.multiply(matrix2)
            print("Result of multiplication:")
        else:
            print("Invalid choice.")
            return
            
        print(result)
        
    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == "__main__":
    main()

