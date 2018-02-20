#include <iostream>
#include <fstream>
#define ALPHABET_SIZE 26

std::string encrypt(std::string input_text, int key);
std::string decrypt(std::string encrypted_text, int key);

int main() {
	int key;
	std::string input_text;
	std::string encrypted_text;
	std::string decrypted_text;
	std::ifstream input_file("input.txt");
	std::ofstream encrypted_file("encrypted.txt");
	std::ofstream decrypted_file("decrypted.txt");
	
	std::cout << "Enter the key: ";
	std::cin >> key;
	
	getline(input_file, input_text);
	
	encrypted_text = encrypt(input_text, key);
	encrypted_file << encrypted_text;
	encrypted_file.close();
	
	decrypted_text = decrypt(encrypted_text, key);
	decrypted_file << decrypted_text;
	decrypted_file.close();
	
	return 0;
}

std::string encrypt(std::string input_text, int key) {
	std::string encrypted_text(input_text.length(), 'a');
	for (int i = 0; i < input_text.length(); i++) {
		int code = input_text[i];
		if (input_text[i] >= 'a' && input_text[i] <= 'z') {
			encrypted_text[i] = 'a' + ((code + key - 'a') % ALPHABET_SIZE);
		} else if (input_text[i] >= 'A' && input_text[i] <= 'Z') {
			encrypted_text[i] = 'A' + ((code + key - 'A') % ALPHABET_SIZE);
		} else {
			encrypted_text[i] = input_text[i];
		}	
	}
	return encrypted_text;
}

std::string decrypt(std::string encrypted_text, int key) {
	std::string decrypted_text(encrypted_text.length(), 'a');
	for (int i = 0; i < encrypted_text.length(); i++) {
		int code = encrypted_text[i];
		if (encrypted_text[i] >= 'a' && encrypted_text[i] <= 'z') {
			decrypted_text[i] = 'a' + ((code - key - 'a' + ALPHABET_SIZE) % ALPHABET_SIZE);
		} else if (encrypted_text[i] >= 'A' && encrypted_text[i] <= 'Z') {
			decrypted_text[i] = 'A' + ((code - key - 'A' + ALPHABET_SIZE) % ALPHABET_SIZE);
		} else {
			decrypted_text[i] = encrypted_text[i];
		}	
	}
	return decrypted_text;
}
