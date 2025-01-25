#include <iostream>
#include <cctype>
#include <sstream>  // For std::stringstream
#include <vector>   // For std::vector
#include <string>   // For std::string

using namespace std;



/* format for problem 
One line prompt for input format
read from cin
send output to cout
*/

class problem{
    public:
    string prompt;
    void (*prob)(string s);
    problem(string _prompt,void f(string s)){
        prompt = _prompt;
        prob = f;
    }
};

int numify(char16_t letter) {
    // Check if the character is a valid alphabet letter
    if (std::isalpha(letter)) {
        // Convert to lowercase and calculate position
        return std::tolower(letter) - 'a' + 1;
    }
    // Return -1 for non-alphabet characters
    return -1;
}

bool isVowel(char c) {
    // Convert to lowercase for case-insensitivity
    c = std::tolower(c);
    // Check if the character is a vowel
    return (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u');
}

vector<int> get_ints(string s){
    stringstream stream(s);
    int number;
    vector<int> numbers;
    while (stream >> number) {
        numbers.push_back(number); // Add each extracted integer to the vector
    }
    return numbers;
}


problem p1("Enter a string",[](string s){
    int res = 0;
    for(auto x:s){
        int n = numify(x);
        res += (isVowel(x)?-1:1)*n*n;
    }
    cout << res << endl;
});

problem p2("Enter 3 space seperated integers from 1 to 1000",[](string s){
    vector<int> nums = get_ints(s);
    int a = nums[0],b = nums[1],c = nums[2];
    double mean = (a+b+c)/3;
    int var = 100*((a*a + b*b + c*c)/3 - mean*mean);
    double res = var/100;
    cout << res << "\n";
});

int main() {
    problem problems[] = {p1,p2};
    int state = 0;
    string s;
    while(true){
        if(state == 0){
            cout << "Main Menu" << endl;
        }
        else{
            cout << problems[state-1].prompt << endl;
        }
        try {
            getline(cin,s);
            if (s == "-1") {
                state = 0;
            } else if (state == 0) {
                state = stoi(s);
                cout << "Entered problem " << s << endl;
            } 
            else{
                problems[state-1].prob(s);
            }
        } catch (const exception& e) {
            cout << "EOF or invalid input" << endl;
            state = 0;
        }
    }
    return 0;
}
