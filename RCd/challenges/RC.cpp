#include <iostream>
#include <cctype>
#include <sstream>  // For std::stringstream
#include <vector>   // For std::vector
#include <string>   // For std::string

using namespace std;



/* format for problem 
One line prompt for input format
read from the input string s
send output to cout in a single line
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
    string reversed;
    for(int i = s.length()-1; i >= 0; i--) {
        reversed += s[i];
    }
    cout << reversed << endl;
});

problem p2("Enter 3 space seperated integers",[](string s){
    vector<int> nums = get_ints(s);
    int sum = nums[0] + nums[1] + nums[2];
    cout << sum << "\n";
});

bool isVowel(char c) {
    // Convert to lowercase for case-insensitivity
    c = std::tolower(c);
    // Check if the character is a vowel
    return (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u');
}



int main() {
    problem problems[] = {p1,p2};
    int state = 0;
    string s;
    int n_probs = sizeof(problems)/sizeof(problem);
    while(true){
        if(state == 0){
            cout << "Enter question number: (1 to " << n_probs << "): " << endl;
        }
        else{
            cout << problems[state-1].prompt << endl;
        }
        try {
            getline(cin,s);
            if (s == "-1") {
                state = 0;
                cout << "Exiting to Main Menu" << endl;
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
