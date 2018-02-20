#include <iostream>
#define DIMENSION 3

int main() {
	
	int A[DIMENSION][DIMENSION] = 
				  { {1, -1, 0},
	                {0, 1, 0},
					{0, 0, 1} };
					
	int inverse_A[DIMENSION][DIMENSION] =
						  { {1, 1, 0},
	                		{0, 1, 0},
							{0, 0, 1} };
							  
	int x[DIMENSION] = {1, 0, 1};
	int i;
	
	std::cout << "i = ";
	std::cin >> i;
	
	int roof_A[DIMENSION][DIMENSION] = {0};
	
	for(int j = 0; j < DIMENSION; j++) {
		for(int k = 0; k < DIMENSION; k++) {
			if (k == i - 1)
				roof_A[j][k] = x[j];
			else
				roof_A[j][k] = A[j][k];
		}
	}
	
	for(int j = 0; j < DIMENSION; j++) {
		for(int k = 0; k < DIMENSION; k++) {
			std::cout << roof_A[j][k] << " ";
		}
		std::cout << std::endl;
	}
	
	int l[DIMENSION] = {0};
	for(int j = 0; j < DIMENSION; j++) {
		int res = 0;
		for(int k = 0; k < DIMENSION; k++) {
			res += inverse_A[j][k] * x[k];
		}
		l[j] = res;
	}
	
	std::cout << "l: " << std::endl;
	for(int k = 0; k < DIMENSION; k++)
		std::cout << l[k] << " ";
	std::cout << std::endl;
		
	if(l[i] == 0) {
		std::cout << "Матрица необратима" << std::endl;
		return 0;
	}
	
	int roof_l[DIMENSION] = {0};
	for(int j = 0; j < DIMENSION; j++)
		roof_l[j] = l[j];
	roof_l[i - 1] = -1;
	
	std::cout << "roof l: " << std::endl;
	for(int k = 0; k < DIMENSION; k++)
		std::cout << roof_l[k] << " ";
	std::cout << std::endl;
	std::cout << std::endl;
	
	
	int roof_l2[DIMENSION] = {0};
	for(int j = 0; j < DIMENSION; j++)
		roof_l2[j] = (-1 / l[i - 1]) * roof_l[j];
		
	std::cout << "roof l2: " << std::endl;
	for(int k = 0; k < DIMENSION; k++)
		std::cout << roof_l2[k] << " ";
	std::cout << std::endl;
					
	int E[DIMENSION][DIMENSION] = {0};
	for(int j = 0; j < DIMENSION; j++) {
		for(int k = 0; k < DIMENSION; k++) {
			if(j == k)
				E[j][k] = 1;
			if (k == i - 1)
				E[j][k] = roof_l2[j];
		}
	}
	
	for(int j = 0; j < DIMENSION; j++) {
		for(int k = 0; k < DIMENSION; k++) {
			std::cout << E[j][k] << " ";
		}
		std::cout << std::endl;
	}
	
	int roof_inverse_A[DIMENSION][DIMENSION] = {0};
	
	for(int ii = 0; ii < DIMENSION; ii++) 
		for(int j = 0; j < DIMENSION; j++) 
			for(int k = 0;k < DIMENSION; k++) 
				roof_inverse_A[ii][j] += inverse_A[ii][k] * E[k][j];
	std::cout << "inverse_roof_A: " <<  std::endl;
	for(int j = 0; j < DIMENSION; j++) {
		for(int k = 0; k < DIMENSION; k++) {
			std::cout << roof_inverse_A[j][k] << " ";
		}
		std::cout << std::endl;
	}
	
	int proof[DIMENSION][DIMENSION] = {0};
	for(int ii = 0; ii < DIMENSION; ii++) 
		for(int j = 0; j < DIMENSION; j++) 
			for(int k = 0;k < DIMENSION; k++) 
				proof[ii][j] += roof_inverse_A[ii][k] * roof_A[k][j];
	std::cout << "E: " <<  std::endl;
	for(int j = 0; j < DIMENSION; j++) {
		for(int k = 0; k < DIMENSION; k++) {
			std::cout << proof[j][k] << " ";
		}
		std::cout << std::endl;
	}
	
	return 0;
}
