class SparseMatrix:
    def __init__(self, file_path=None, num_rows=0, num_cols=0):
        self.data = {}  # key: (row, col), value: value
        self.rows = num_rows
        self.cols = num_cols
        if file_path:
            self._read_from_file(file_path)
    
    def _read_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Parse dimensions
            self.rows = int(lines[0].strip().split('=')[1])
            self.cols = int(lines[1].strip().split('=')[1])
            
            # Parse matrix elements
            for line in lines[2:]:
                line = line.strip()
                if not line:
                    continue
                
                if not (line.startswith("(") and line.endswith(")")):
                    raise ValueError("Input file has wrong format")
                
                parts = line[1:-1].split(',')
                if len(parts) != 3:
                    raise ValueError("Input file has wrong format")
                
                row, col, val = map(int, parts)
                
                # Add bounds checking
                if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                    raise ValueError(f"Index ({row}, {col}) out of bounds for matrix {self.rows}x{self.cols}")
                
                self.set_element(row, col, val)
                
        except Exception as e:
            raise ValueError("Input file has wrong format") from e
    
    def get_element(self, row, col):
        return self.data.get((row, col), 0)
    
    def set_element(self, row, col, value):
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]
    
    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition.")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        keys = set(self.data.keys()).union(other.data.keys())
        
        for key in keys:
            result.set_element(*key, self.get_element(*key) + other.get_element(*key))
        
        return result
    
    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        keys = set(self.data.keys()).union(other.data.keys())
        
        for key in keys:
            result.set_element(*key, self.get_element(*key) - other.get_element(*key))
        
        return result
    
    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions are incompatible for multiplication.")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        
        # More efficient multiplication - only iterate over non-zero elements
        for (i, k), v1 in self.data.items():
            for (k2, j), v2 in other.data.items():
                if k == k2:  # Only multiply when indices align
                    value = v1 * v2
                    if value != 0:
                        current = result.get_element(i, j)
                        result.set_element(i, j, current + value)
        
        return result
    
    def __str__(self):
        output = [f"rows={self.rows}", f"cols={self.cols}"]
        for (i, j), v in sorted(self.data.items()):
            output.append(f"({i}, {j}, {v})")
        return "\n".join(output)
