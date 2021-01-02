from Minimum.PSO import Solution

if __name__ == "__main__":
    solution = Solution()
    print("Minimum value of f(x1,x2) = (x1)^2 - (x2)^2 is", solution.solve(5000))
